#!/usr/bin/env python3
"""Offline localization key audit for the Extended Timeline mod.

The audit checks the mod's event localization against the scripts that
reference it. It does not launch the game and makes no changes.

Checks:
  * every localization key referenced by a mod script exists in English and
    in Turkish (the event namespace et_culture.*)
  * every key defined in the event localization files is referenced by a
    script (no orphan keys left behind after a rename or a removal)
  * the English and Turkish event files define exactly the same key set
  * the mod's localization files are valid YAML (catches unescaped quotes
    inside double-quoted values)

Content files (country, province, holy site and culture names) are not
compared key by key: the mod ships a Turkish name for more tags than the
English file, which is a content decision, not a script defect.

Usage:
  python et-history-data/scripts/loc-key-audit.py
  python et-history-data/scripts/loc-key-audit.py --mod "C:\\...\\Extended Timeline"

Exit code: 0 clean, 1 findings.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_MOD = REPO / "Extended Timeline"

LOCALIZATION_DIR = "in_game/localization"
EVENT_LOC_STEM = "et_culture_events_l_"
LANGUAGES = ("english", "turkish")

# et_culture.105.title, et_culture.1.a.tt (the bare event id is not a key)
KEY_REF = re.compile(r"\bet_culture\.\d+\.[a-z0-9_]+(?:\.[a-z0-9_]+)*\b")
# a localization key definition: " et_culture.105.title: "..."
KEY_DEF = re.compile(r"(?m)^\s*([A-Za-z0-9_.]+)\s*:")
# the language header line (l_english / l_turkish) is not a key
LANGUAGE_HEADER = re.compile(r"^l_[a-z_]+$")


def collect_script_refs(mod: Path) -> set[str]:
    """Return every et_culture.* key the mod scripts refer to."""
    refs: set[str] = set()
    for path in sorted((mod / "in_game").rglob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        refs.update(KEY_REF.findall(text))
    return refs


def collect_loc_keys(mod: Path, language: str) -> tuple[set[str], list[str]]:
    """Return the event localization keys of a language and the files read."""
    directory = mod / LOCALIZATION_DIR / language
    keys: set[str] = set()
    files: list[str] = []
    for path in sorted(directory.glob(f"{EVENT_LOC_STEM}*.yml")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for key in KEY_DEF.findall(text):
            if LANGUAGE_HEADER.match(key):
                continue
            keys.add(key)
        files.append(path.name)
    return keys, files


def check_yaml(mod: Path) -> list[str]:
    """Return a list of localization files that are not valid YAML."""
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover - environment guard
        return []
    broken: list[str] = []
    for path in sorted((mod / LOCALIZATION_DIR).rglob("*.yml")):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # yaml.YAMLError and decoding problems
            broken.append(f"{path.relative_to(mod)}: {exc}")
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description="Extended Timeline localization audit")
    parser.add_argument("--mod", type=Path, default=DEFAULT_MOD,
                        help="mod kok dizini (varsayilan: repo icindeki Extended Timeline)")
    args = parser.parse_args()
    mod: Path = args.mod
    if not (mod / "in_game").is_dir():
        print(f"HATA: mod dizini bulunamadi: {mod}")
        return 1

    refs = collect_script_refs(mod)
    loc: dict[str, set[str]] = {}
    for language in LANGUAGES:
        keys, files = collect_loc_keys(mod, language)
        loc[language] = keys
        print(f"  {language:9} {len(keys):4} anahtar ({', '.join(files)})")

    findings: list[str] = []
    for language in LANGUAGES:
        keys = loc[language]
        for key in sorted(refs - keys):
            findings.append(f"[{language}] scriptte aniliyor ama tanimli degil: {key}")
        for key in sorted(keys - refs):
            findings.append(f"[{language}] yetim anahtar (scriptte kullanilmiyor): {key}")
    for key in sorted(loc["english"] ^ loc["turkish"]):
        side = "yalnizca EN" if key in loc["english"] else "yalnizca TR"
        findings.append(f"[EN/TR] {side} tanimli: {key}")

    broken = check_yaml(mod)
    for item in broken:
        findings.append(f"[yaml] gecersiz: {item}")

    print(f"Script referansi: {len(refs)}")
    if not findings:
        print("Localization denetimi temiz: eksik, yetim veya cift dilli fark yok.")
        return 0
    print(f"BULGU: {len(findings)}")
    for item in findings:
        print(f"  {item}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
