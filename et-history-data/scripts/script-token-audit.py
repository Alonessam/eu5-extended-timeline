#!/usr/bin/env python3
"""Offline EU5 script token audit for the Extended Timeline mod.

The audit reads every .txt file under the mod's in_game and main_menu trees and
checks the tokens against the installed vanilla EU5 data. It does not launch the
game and makes no changes.

Checks:
  * prefixed references: location:, culture:, religion:, pop_type:, area:,
    language:
  * country tags used by tag =, has_or_had_tag = and from_tag =
  * script-value constants on the right side of add_* effects
  * outcome enum values (neutral/negative/positive)
  * illustration_tags values
  * define_pop type/culture/religion keys
  * change_language scope and dialect key
  * religion groups, culture groups and definition_modifier keys
  * field names in event and on_action logic files

Field-name checking is corpus-based: a token is accepted when it appears
anywhere in the vanilla or mod data, so the audit catches typos and unknown
tokens rather than every semantic misuse.

Vanilla path resolution, in order: --vanilla, EU5_VANILLA, a few standard
install paths. The mod path defaults to <repo>/Extended Timeline.

Usage:
    python et-history-data/scripts/script-token-audit.py
    python et-history-data/scripts/script-token-audit.py --vanilla "D:/EU5/game"
    python et-history-data/scripts/script-token-audit.py --mod "path/to/Extended Timeline"

Exit code: 0 when no problems are found, 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

FIELD_LOW = re.compile(r"^\s*([a-z_][a-z0-9_]*)\s*=", re.M)
FIELD_UP = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=", re.M)
BARE = re.compile(r"^\s*([a-z_][a-z0-9_]*)\s*$", re.M)
REF = re.compile(r"\b(location|culture|religion|pop_type|area|language):([a-z0-9_]+)")
TAG_USE = re.compile(
    r"(?:^\s*tag\s*=\s*|has_or_had_tag\s*=\s*|from_tag\s*=\s*)"
    r"([A-Z][A-Z0-9]{1,4})\b",
    re.M,
)
TAG_DEF = re.compile(r"\btag\s*=\s*([A-Z][A-Z0-9]{1,4})\b")
CONST = re.compile(
    r"^\s*(add_prestige|add_stability|add_legitimacy|add_army_tradition|"
    r"add_republican_tradition)\s*=\s*([a-z_][a-z0-9_]*)\s*$",
    re.M,
)
CONST_NEG = re.compile(
    r"^\s*(add_prestige|add_stability|add_legitimacy|add_army_tradition|"
    r"add_republican_tradition)\s*=\s*-([a-z_][a-z0-9_]*)\s*$",
    re.M,
)
OUTCOME = re.compile(r"^\s*outcome\s*=\s*([a-z_]+)\s*$", re.M)
ILLUSTRATION = re.compile(r"illustration_tags\s*=\s*\{([^}]*)\}", re.S)
ILL_PAIR = re.compile(r"([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)")
DEFINE_POP = re.compile(r"define_pop\s*=\s*\{([^}]*)\}", re.S)
CULTURE_TAGS = re.compile(r"^\s*tags\s*=\s*\{([^}]*)\}", re.M)
CHANGE_LANGUAGE = re.compile(r"change_language\s*=\s*([a-z_]+):([a-z0-9_]+)")
CHANGE_LANGUAGE_BARE = re.compile(
    r"change_language\s*=\s*([a-z_][a-z0-9_]*)\s*$", re.M
)
CULTURE_GROUPS = re.compile(r"culture_groups\s*=\s*\{([^}]*)\}")
RELIGION_GROUP = re.compile(r"^\s*group\s*=\s*([a-z_][a-z0-9_]*)\s*$", re.M)
DEFINITION_MODIFIER = re.compile(r"definition_modifier\s*=\s*\{([^}]*)\}", re.S)
GROUP_KEY = re.compile(r"^([a-z_][a-z0-9_]*)\s*=\s*\{", re.M)

OUTCOME_VALUES = {"neutral", "negative", "positive"}
SKIP_ILLUSTRATION = {"10", "20"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def strip_comments(text: str) -> str:
    """Blank out # comments while preserving every offset and line break."""
    return re.sub(r"#[^\n]*", lambda m: " " * len(m.group(0)), text)


def iter_txt(root: Path):
    if not root.is_dir():
        return
    for path in sorted(root.rglob("*.txt")):
        yield path, read_text(path)


def keys_of(root: Path) -> set[str]:
    keys: set[str] = set()
    for _, text in iter_txt(root):
        keys.update(m.group(1) for m in FIELD_LOW.finditer(strip_comments(text)))
    return keys


def union_keys(*roots: Path) -> set[str]:
    keys: set[str] = set()
    for root in roots:
        keys |= keys_of(root)
    return keys


def collect_fields(root: Path) -> tuple[set[str], set[str]]:
    low: set[str] = set()
    up: set[str] = set()
    for _, text in iter_txt(root):
        clean = strip_comments(text)
        low.update(m.group(1) for m in FIELD_LOW.finditer(clean))
        up.update(m.group(1) for m in FIELD_UP.finditer(clean))
    return low, up


def collect_tags(root: Path) -> set[str]:
    tags: set[str] = set()
    for _, text in iter_txt(root):
        clean = strip_comments(text)
        tags.update(m.group(1) for m in FIELD_UP.finditer(clean))
        tags.update(m.group(1) for m in TAG_DEF.finditer(clean))
    return tags


def collect_gfx(vanilla: Path, mod: Path) -> set[str]:
    defined: set[str] = set()
    for base in (
        vanilla / "in_game" / "gfx" / "graphical_culture_types",
        mod / "in_game" / "gfx" / "graphical_culture_types",
    ):
        for _, text in iter_txt(base):
            clean = strip_comments(text)
            defined.update(m.group(1) for m in FIELD_LOW.finditer(clean))
            defined.update(
                re.findall(r"^\s*culture_tag\s*=\s*([a-z0-9_]+)", clean, re.M)
            )

    # Vanilla treats tags in culture tags = { ... } lists as asset-lookup
    # fallbacks; a token vanilla itself uses is valid even without a type.
    used: set[str] = set()
    for _, text in iter_txt(vanilla / "in_game" / "common" / "cultures"):
        used.update(re.findall(r"\b([a-z0-9_]+_gfx)\b", strip_comments(text)))
    return defined | used


def collect_illustration_values(vanilla: Path) -> set[str]:
    values: set[str] = set()
    for _, text in iter_txt(vanilla / "in_game" / "events"):
        clean = strip_comments(text)
        for block in ILLUSTRATION.finditer(clean):
            for left, right in ILL_PAIR.findall(block.group(1)):
                for token in (left, right):
                    if not token.isdigit():
                        values.add(token)
    return values


def collect_areas(vanilla: Path, mod: Path) -> set[str]:
    areas: set[str] = set()
    for base in (vanilla / "in_game", mod / "in_game"):
        definitions = base / "map_data" / "definitions.txt"
        if definitions.is_file():
            areas.update(
                m.group(1)
                for m in FIELD_LOW.finditer(strip_comments(read_text(definitions)))
            )
        for _, text in iter_txt(base / "common" / "scripted_geography"):
            areas.update(m.group(1) for m in BARE.finditer(strip_comments(text)))
    return areas


def collect_group_keys(*roots: Path) -> set[str]:
    keys: set[str] = set()
    for root in roots:
        for _, text in iter_txt(root):
            keys.update(m.group(1) for m in GROUP_KEY.finditer(strip_comments(text)))
    return keys


def collect_modifier_keys(vanilla: Path, van_data: Path, mod: Path) -> set[str]:
    keys: set[str] = set()
    for base in (
        vanilla / "main_menu" / "common" / "modifier_type_definitions",
        mod / "main_menu" / "common" / "modifier_type_definitions",
        vanilla / "main_menu" / "common" / "modifier_icons",
        mod / "main_menu" / "common" / "modifier_icons",
    ):
        for _, text in iter_txt(base):
            keys.update(m.group(1) for m in GROUP_KEY.finditer(strip_comments(text)))
    for root in (van_data / "common", vanilla / "main_menu"):
        for _, text in iter_txt(root):
            clean = strip_comments(text)
            for block in DEFINITION_MODIFIER.finditer(clean):
                keys.update(m.group(1) for m in FIELD_LOW.finditer(block.group(1)))
    return keys


def resolve_vanilla(argument: str | None) -> Path | None:
    candidates: list[Path] = []
    if argument:
        candidates.append(Path(argument))
    if os.environ.get("EU5_VANILLA"):
        candidates.append(Path(os.environ["EU5_VANILLA"]))
    candidates.extend(
        [
            Path.home() / "Desktop" / "Europa Universalis V" / "game",
            Path("C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game"),
            Path("C:/Program Files/Steam/steamapps/common/Europa Universalis V/game"),
        ]
    )
    for candidate in candidates:
        if (candidate / "in_game" / "common").is_dir():
            return candidate
    return None


def resolve_mod(argument: str | None) -> Path:
    if argument:
        return Path(argument)
    return Path(__file__).resolve().parents[2] / "Extended Timeline"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Extended Timeline script tokens against vanilla EU5 data."
    )
    parser.add_argument(
        "--vanilla",
        help="Path to the EU5 'game' directory (the one containing in_game/).",
    )
    parser.add_argument(
        "--mod",
        help="Path to the Extended Timeline mod folder (default: <repo>/Extended Timeline).",
    )
    args = parser.parse_args()

    vanilla = resolve_vanilla(args.vanilla)
    if vanilla is None:
        print(
            "Could not find the vanilla EU5 game directory. "
            "Pass --vanilla or set EU5_VANILLA.",
            file=sys.stderr,
        )
        return 2
    mod = resolve_mod(args.mod)
    if not (mod / "in_game").is_dir():
        print(f"Not an Extended Timeline mod folder: {mod}", file=sys.stderr)
        return 2

    van_data = vanilla / "in_game"
    mod_data = mod / "in_game"

    locations = union_keys(
        van_data / "map_data" / "named_locations",
        mod_data / "map_data" / "named_locations",
    )
    cultures = union_keys(
        van_data / "common" / "cultures", mod_data / "common" / "cultures"
    )
    religions = union_keys(
        van_data / "common" / "religions", mod_data / "common" / "religions"
    )
    pop_types = union_keys(
        van_data / "common" / "pop_types", mod_data / "common" / "pop_types"
    )
    languages = union_keys(
        van_data / "common" / "languages", mod_data / "common" / "languages"
    )
    script_values = union_keys(
        van_data / "common" / "script_values",
        vanilla / "main_menu" / "common" / "script_values",
        mod_data / "common" / "script_values",
        mod / "main_menu" / "common" / "script_values",
    )
    tags = (
        collect_tags(van_data / "setup" / "countries")
        | collect_tags(van_data / "common" / "formable_countries")
        | collect_tags(mod_data / "setup" / "countries")
        | collect_tags(mod / "main_menu" / "setup")
    )
    areas = collect_areas(vanilla, mod)
    gfx_tags = collect_gfx(vanilla, mod)
    illustration_values = collect_illustration_values(vanilla)
    religion_groups = collect_group_keys(
        van_data / "common" / "religion_groups",
        mod_data / "common" / "religion_groups",
    )
    culture_groups = collect_group_keys(
        van_data / "common" / "culture_groups",
        mod_data / "common" / "culture_groups",
    )
    modifier_keys = collect_modifier_keys(vanilla, van_data, mod)

    van_low, van_up = collect_fields(van_data / "events")
    for root in (
        van_data / "common",
        van_data / "setup",
        vanilla / "main_menu",
    ):
        low, up = collect_fields(root)
        van_low |= low
        van_up |= up

    mod_low: set[str] = set()
    mod_up: set[str] = set()
    targets: list[tuple[Path, str]] = []
    for base in (mod_data, mod / "main_menu"):
        for path, text in iter_txt(base):
            targets.append((path, text))
            clean = strip_comments(text)
            mod_low.update(m.group(1) for m in FIELD_LOW.finditer(clean))
            mod_up.update(m.group(1) for m in FIELD_UP.finditer(clean))

    resolvers = {
        "location": locations,
        "culture": cultures,
        "religion": religions,
        "pop_type": pop_types,
        "area": areas,
        "language": languages,
    }

    problems: dict[str, list[str]] = defaultdict(list)

    def add(group: str, path: Path, text: str, pos: int, message: str) -> None:
        rel = path.relative_to(mod).as_posix()
        line = text.count("\n", 0, pos) + 1
        problems[group].append(f"{rel}:{line}: {message}")

    for path, raw in targets:
        text = strip_comments(raw)
        parts = set(path.parts)

        for match in REF.finditer(text):
            kind, value = match.group(1), match.group(2)
            if value not in resolvers[kind]:
                add("unresolved reference", path, text, match.start(), f"{kind}:{value}")

        for match in TAG_USE.finditer(text):
            tag = match.group(1)
            if tag not in tags:
                add("unknown country tag", path, text, match.start(), tag)

        for match in CONST.finditer(text):
            if match.group(2) not in script_values:
                add(
                    "unresolved script value",
                    path,
                    text,
                    match.start(),
                    f"{match.group(1)} = {match.group(2)}",
                )
        for match in CONST_NEG.finditer(text):
            add(
                "negated named constant",
                path,
                text,
                match.start(),
                f"{match.group(1)} = -{match.group(2)}",
            )

        for match in OUTCOME.finditer(text):
            if match.group(1) not in OUTCOME_VALUES:
                add(
                    "invalid outcome",
                    path,
                    text,
                    match.start(),
                    f"outcome = {match.group(1)}",
                )

        for block in ILLUSTRATION.finditer(text):
            for pair in ILL_PAIR.finditer(block.group(1)):
                for token in pair.groups():
                    if token in SKIP_ILLUSTRATION or token.isdigit():
                        continue
                    if token not in illustration_values:
                        add(
                            "unknown illustration tag",
                            path,
                            text,
                            block.start(1) + pair.start(),
                            token,
                        )

        for block in DEFINE_POP.finditer(text):
            body = block.group(1)
            for key, allowed in (
                ("culture", cultures),
                ("religion", religions),
                ("type", pop_types),
            ):
                found = re.search(rf"\b{key}\s*=\s*([a-z_][a-z0-9_]*)\b", body)
                if found and found.group(1) not in allowed:
                    add(
                        "unknown define_pop key",
                        path,
                        text,
                        block.start(),
                        f"{key} = {found.group(1)}",
                    )

        for match in CHANGE_LANGUAGE.finditer(text):
            prefix, value = match.group(1), match.group(2)
            if prefix != "dialect" or value not in languages:
                add(
                    "invalid change_language",
                    path,
                    text,
                    match.start(),
                    f"change_language = {prefix}:{value}",
                )
        for match in CHANGE_LANGUAGE_BARE.finditer(text):
            add(
                "invalid change_language",
                path,
                text,
                match.start(),
                f"change_language = {match.group(1)} (expected dialect:<language>)",
            )

        if "religions" in parts:
            for match in RELIGION_GROUP.finditer(text):
                if match.group(1) not in religion_groups:
                    add(
                        "unknown religion group",
                        path,
                        text,
                        match.start(),
                        match.group(1),
                    )
        if "cultures" in parts:
            for match in CULTURE_GROUPS.finditer(text):
                for token in re.findall(r"[a-z_][a-z0-9_]*", match.group(1)):
                    if token not in culture_groups:
                        add(
                            "unknown culture group",
                            path,
                            text,
                            match.start(),
                            token,
                        )
        for match in DEFINITION_MODIFIER.finditer(text):
            for inner in FIELD_LOW.finditer(match.group(1)):
                if inner.group(1) not in modifier_keys:
                    add(
                        "unknown modifier",
                        path,
                        text,
                        match.start(1) + inner.start(),
                        inner.group(1),
                    )

        if "events" in parts or "on_action" in parts:
            for match in FIELD_LOW.finditer(text):
                word = match.group(1)
                if word not in van_low and word not in mod_low:
                    add("unknown field", path, text, match.start(), f"{word} =")
            for match in FIELD_UP.finditer(text):
                word = match.group(1)
                if word not in van_up and word not in mod_up:
                    add("unknown block", path, text, match.start(), f"{word} =")

    for path, raw in iter_txt(mod_data / "common" / "cultures"):
        text = strip_comments(raw)
        for block in CULTURE_TAGS.finditer(text):
            for token in re.findall(r"[a-z0-9_]+", block.group(1)):
                if token.endswith("_gfx") and token not in gfx_tags:
                    add(
                        "undefined gfx tag",
                        path,
                        text,
                        block.start(),
                        token,
                    )

    print("Script token audit")
    print(f"  mod:     {mod}")
    print(f"  vanilla: {vanilla}")
    print(f"  targets: {len(targets)}")
    print(
        "  tokens:  "
        f"locations={len(locations)} cultures={len(cultures)} "
        f"religions={len(religions)} pop_types={len(pop_types)} "
        f"areas={len(areas)} languages={len(languages)} tags={len(tags)} "
        f"script_values={len(script_values)} gfx={len(gfx_tags)} "
        f"illustrations={len(illustration_values)} "
        f"religion_groups={len(religion_groups)} "
        f"culture_groups={len(culture_groups)} "
        f"modifiers={len(modifier_keys)}"
    )

    if not problems:
        print("No unresolved tokens found.")
        return 0

    print(f"Problem groups: {len(problems)}")
    for group in sorted(problems):
        items = sorted(problems[group])
        print(f"  {group} ({len(items)})")
        for item in items[:100]:
            print(f"    {item}")
        if len(items) > 100:
            print(f"    ... and {len(items) - 100} more")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
