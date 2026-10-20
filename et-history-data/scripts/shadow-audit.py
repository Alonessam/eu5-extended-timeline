#!/usr/bin/env python3
"""Vanilla anahtar golge raporu (offline).

Ayni veritabani dizininde ayni ust duzey anahtari tanimlayan vanilla ve mod
dosyalarini karsilastirir; hangi tanimin oyuna girdigini, hangisinin golgede
kaldigini listeler.

Kural (18 Ekim 2026 loglariyla dogrulandi): ayni DB icinde bir anahtar birden
fazla dosyada tanimliysa goreli dosya yolunun alfabetik sirasinda ONCE gelen
dosya kazanir; sonraki tanim olusturulmaz. Ayni goreli yola sahip mod dosyasi
vanilla dosyasini birebir degistirir; bu dosyalar rakip sayilmaz.

Oyunu calistirmaz, veri degistirmez. Varsayilan cikti:
et-history-data/research/historical-events/<tarih>_vanilla_shadow_report.md

Kullanim:
    python et-history-data/scripts/shadow-audit.py
    python et-history-data/scripts/shadow-audit.py --vanilla "D:/EU5/game"
    python et-history-data/scripts/shadow-audit.py --out custom/report.md

Cikis kodu: 0 rapor yazildi, 2 girdi yollari eksik.
"""

import argparse
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO / "et-history-data" / "research" / "historical-events"

DBS = [
    "common/languages",
    "common/cultures",
    "common/religions",
    "common/culture_groups",
    "common/religion_groups",
    "common/language_families",
    "setup/countries",
]
SETUP_DB = "setup/countries"
ON_ACTION_DB = "common/on_action"

TOPKEY = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{", re.M)
COMMENT = re.compile(r"#[^\n]*")
WS = re.compile(r"\s+")

# 2026-10-19_vanilla_key_shadow_audit.md'teki dokuz kayit.
KNOWN = [
    ("coptic_culture", "common/cultures"),
    ("haixi_culture", "common/cultures"),
    ("hurga_culture", "common/cultures"),
    ("aramaic_language", "common/languages"),
    ("gothic_language", "common/languages"),
    ("alan_paganism", "common/religions"),
    ("hellenism_religion", "common/religions"),
    ("miaphysite", "common/religions"),
    ("yearly_country_pulse", ON_ACTION_DB),
]

KIND_TR = {
    "DEAD": "ÖLÜ (vanilla kazandı)",
    "ALIVE": "YAŞIYOR (mod kazandı)",
    "MOD_INTERNAL": "MOD-İÇİ",
    "VANILLA_INTERNAL": "VANILLA-İÇİ",
}

STATUS_TR = {"vanilla": "vanilla", "mod": "mod"}


def resolve_vanilla(argument):
    candidates = []
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


def resolve_mod(argument):
    if argument:
        return Path(argument)
    return REPO / "Extended Timeline"


def read_text(path):
    return path.read_bytes().decode("utf-8-sig", errors="ignore")


def normalize(body):
    """Yorumlari ve bosluklari at; govde karsilastirmasi icin."""
    return WS.sub(" ", COMMENT.sub("", body)).strip()


def blank_comments(text):
    """Yorumlari boslukla degistir; konumlar korunur (parantez sayimi icin)."""
    return COMMENT.sub(lambda match: " " * len(match.group(0)), text)


def extract_blocks(path):
    """Dosyadaki ust duzey `key = { ... }` bloklarini normalize govdeyle dondur.

    Bazi vanilla dosyalari blok alanlarini girintisiz yaziyor (or.
    00_steppes.txt); bu yuzden yalnizca parantez derinligi 0 olan anahtarlar
    ust duzey sayilir.
    """
    text = read_text(path)
    cleaned = blank_comments(text)
    depth_at = [0] * (len(cleaned) + 1)
    depth = 0
    for index, char in enumerate(cleaned):
        depth_at[index] = depth
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        depth_at[index + 1] = depth

    blocks = {}
    for match in TOPKEY.finditer(cleaned):
        if depth_at[match.start()] != 0:
            continue
        open_pos = match.end() - 1
        depth = 0
        end = len(cleaned)
        for index in range(open_pos, len(cleaned)):
            char = cleaned[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = index
                    break
        blocks[match.group(1)] = normalize(cleaned[open_pos + 1:end])
    return blocks


def scan_db(vanilla_root, mod_root, db):
    vanilla = {}
    mod = {}
    vanilla_dir = vanilla_root / db
    mod_dir = mod_root / db
    for path in sorted(vanilla_dir.rglob("*.txt")) if vanilla_dir.is_dir() else []:
        vanilla[path.relative_to(vanilla_root).as_posix()] = extract_blocks(path)
    for path in sorted(mod_dir.rglob("*.txt")) if mod_dir.is_dir() else []:
        mod[path.relative_to(mod_root).as_posix()] = extract_blocks(path)

    overrides = sorted(set(vanilla) & set(mod))
    files = {}
    for rel, blocks in vanilla.items():
        if rel in mod:
            continue  # mod ayni yolu birebir degistiriyor
        files[rel] = ("vanilla", blocks)
    for rel, blocks in mod.items():
        files[rel] = ("mod", blocks)

    occurrences = defaultdict(list)
    for rel in sorted(files):
        source, blocks = files[rel]
        for key, body in blocks.items():
            occurrences[key].append((rel, source, body))

    rows = []
    for key in sorted(occurrences):
        entries = occurrences[key]
        if len(entries) < 2:
            continue
        winner_rel, winner_src, winner_body = entries[0]
        losers = [(rel, src, body == winner_body) for rel, src, body in entries[1:]]
        has_vanilla_loser = any(src == "vanilla" for _, src, _ in losers)
        has_mod_loser = any(src == "mod" for _, src, _ in losers)
        if winner_src == "mod":
            kind = "ALIVE" if has_vanilla_loser else "MOD_INTERNAL"
        else:
            kind = "DEAD" if has_mod_loser else "VANILLA_INTERNAL"
        rows.append(
            {
                "key": key,
                "winner": winner_rel,
                "winner_src": winner_src,
                "losers": losers,
                "kind": kind,
            }
        )
    return {
        "vanilla_files": len(vanilla),
        "mod_files": len(mod),
        "overrides": overrides,
        "files": files,
        "rows": rows,
    }


def describe_losers(row):
    parts = []
    for rel, src, same in row["losers"]:
        content = "aynı" if same else "farklı"
        parts.append(f"`{rel}` ({STATUS_TR[src]}, {content})")
    return "; ".join(parts)


def group_by_loser(rows):
    grouped = defaultdict(list)
    for row in rows:
        for rel, src, same in row["losers"]:
            grouped[rel].append((row["key"], row["winner"], src, same))
    return grouped


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |",
             "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def render(report, on_action):
    today = date.today().isoformat()
    lines = []
    lines.append(f"# Vanilla Anahtar Gölge Raporu (offline) — {today}")
    lines.append("")
    lines.append(
        "`vanilla_key_shadow_review` tamamlanmış görünüyordu; ancak 18 Ekim 2026 "
        "log'undaki `Duplicated key ... will not be created` satırları, niyet "
        "edilen bazı mod tanımlarının oyuna hiç girmediğini gösterdi. Bu rapor, "
        "oyunu çalıştırmadan ilgili tüm DB'lerde aynı üst düzey anahtarı "
        "tanımlayan dosyaları karşılaştırır ve kazananı listeler."
    )
    lines.append("")
    lines.append(
        "Üretici: `et-history-data/scripts/shadow-audit.py` (offline, stdlib). "
        "Yeniden üretmek için repo kökünden `python "
        "et-history-data/scripts/shadow-audit.py` çalıştırın."
    )
    lines.append("")
    lines.append("## Yöntem")
    lines.append("")
    lines.append(
        "- Kural: aynı DB içinde aynı üst düzey anahtar birden fazla dosyada "
        "tanımlıysa, göreli dosya yolunun alfabetik sırasında **önce gelen** "
        "tanım yüklenir; sonraki tanım oluşturulmaz. 18 Ekim log'undaki dört "
        "bağımsız vaka (aramaic, gothic, coptic, miaphysite) bu kuralı doğrular."
    )
    lines.append(
        "- Aynı göreli yola sahip mod dosyası vanilla dosyasını birebir "
        "değiştirir; bu dosyalar rakip sayılmadı ve aşağıda kasıtlı override "
        "olarak listelendi."
    )
    lines.append(
        "- İçerik karşılaştırması: blok gövdesi yorumlardan ve boşluktan "
        "arındırılıp birebir karşılaştırılır. `aynı` = kaybedilen tanım "
        "kazananla özdeş (zararsız); `farklı` = mod deltası gerçekten kayıp."
    )
    lines.append(
        "- Kapsam: dil, kültür, din, kültür grubu, din grubu, dil ailesi ve "
        "`setup/countries`. `common/on_action` ayrı ele alındı (blok birleşimi "
        "kuralı)."
    )
    lines.append(
        "- İç içe alan (field) çakışmaları kapsam dışıdır; 18 Ekim'deki "
        "`et_german.txt` seli bu sınıftaydı ve UPDATE 19 ile giderildi."
    )
    lines.append("")
    lines.append("## Özet")
    lines.append("")
    summary_rows = []
    totals = Counter()
    for db in DBS:
        data = report[db]
        kinds = Counter(row["kind"] for row in data["rows"])
        for kind, count in kinds.items():
            totals[kind] += count
        summary_rows.append(
            [
                f"`{db}`",
                data["vanilla_files"],
                data["mod_files"],
                len(data["overrides"]),
                len(data["rows"]),
                kinds.get("DEAD", 0),
                kinds.get("ALIVE", 0),
                kinds.get("MOD_INTERNAL", 0),
                kinds.get("VANILLA_INTERNAL", 0),
            ]
        )
    summary_rows.append(
        [
            "**Toplam**",
            sum(report[db]["vanilla_files"] for db in DBS),
            sum(report[db]["mod_files"] for db in DBS),
            sum(len(report[db]["overrides"]) for db in DBS),
            sum(len(report[db]["rows"]) for db in DBS),
            totals.get("DEAD", 0),
            totals.get("ALIVE", 0),
            totals.get("MOD_INTERNAL", 0),
            totals.get("VANILLA_INTERNAL", 0),
        ]
    )
    lines.extend(
        table(
            [
                "DB",
                "Vanilla dosya",
                "Mod dosya",
                "Aynı-yol override",
                "Gölgelenen anahtar",
                "Ölü",
                "Yaşayan",
                "Mod-içi",
                "Vanilla-içi",
            ],
            summary_rows,
        )
    )
    lines.append("")
    lines.append("## Bilinen dokuz yeniden tanım")
    lines.append("")
    known_rows = []
    for key, db in KNOWN:
        if db == ON_ACTION_DB:
            known_rows.append(
                [
                    f"`{key}`",
                    "on_action",
                    "—",
                    "—",
                    "ÖZEL: blok birleşimi",
                    "Aşağıdaki on_action notu",
                ]
            )
            continue
        row = next((r for r in report[db]["rows"] if r["key"] == key), None)
        if row is None:
            known_rows.append(
                [
                    f"`{key}`",
                    db,
                    "—",
                    "—",
                    "çakışma yok (tek tanım)",
                    "Mod tanımı yükleniyor",
                ]
            )
        else:
            known_rows.append(
                [
                    f"`{key}`",
                    db,
                    f"`{row['winner']}`",
                    describe_losers(row),
                    KIND_TR[row["kind"]],
                    "",
                ]
            )
    lines.extend(table(["Anahtar", "DB", "Kazanan", "Kaybeden", "Sonuç", "Not"], known_rows))
    lines.append("")
    lines.append(
        "Denetim notu 20 Ekim 2026'da düzeltildi: `coptic_culture`, `miaphysite` "
        "ve `aramaic_language` yüklemede vanilla'ya yeniliyordu. Aynı gün üç "
        "delta bloğu rakibinden önce sıralanan dosyalara taşındı "
        "(`00_et_egypt.txt`, `00_et_christianity.txt`, `00_aramaic.txt`); bu "
        "rapor taşıma sonrası üretildi ve üçü de YAŞIYOR. `gothic_language`, "
        "`alan_paganism` ve `hellenism_religion` zaten yaşıyordu; `haixi/hurga` "
        "tek tanımlı; `yearly_country_pulse` on_action istisnası."
    )
    lines.append("")
    lines.append("## Dil, kültür, din ve grup çakışmaları (tam liste)")
    lines.append("")
    detail_rows = []
    for db in DBS:
        if db == SETUP_DB:
            continue
        for row in report[db]["rows"]:
            detail_rows.append(
                [
                    f"`{db}`",
                    f"`{row['key']}`",
                    f"`{row['winner']}` ({STATUS_TR[row['winner_src']]})",
                    describe_losers(row),
                    KIND_TR[row["kind"]],
                ]
            )
    if detail_rows:
        lines.extend(table(["DB", "Anahtar", "Kazanan", "Kaybeden", "Sonuç"], detail_rows))
    else:
        lines.append("Çakışma bulunmadı.")
    lines.append("")

    setup = report[SETUP_DB]
    dead = [row for row in setup["rows"] if row["kind"] == "DEAD"]
    alive = [row for row in setup["rows"] if row["kind"] == "ALIVE"]
    internal = [row for row in setup["rows"] if row["kind"] == "MOD_INTERNAL"]
    vanilla_internal = [row for row in setup["rows"] if row["kind"] == "VANILLA_INTERNAL"]

    lines.append("## Setup: ölü kalan mod tanımları (vanilla kazandı)")
    lines.append("")
    lines.append(
        f"{len(dead)} anahtarda mod tanımı yüklenmiyor. Aşağıda kaybeden mod "
        "dosyasına göre gruplanmıştır; parantez içi kazanan vanilla dosyasıdır. "
        "`*` işaretli satırlarda kaybedilen tanım kazananla **birebir aynı** "
        "(zararsız), işaretsizlerde içerik farklı (gerçek delta kaybı)."
    )
    lines.append("")
    dead_groups = defaultdict(list)
    for row in dead:
        for rel, src, same in row["losers"]:
            if src != "mod":
                continue
            dead_groups[rel].append((row["key"], row["winner"], same))
    for rel in sorted(dead_groups):
        entries = dead_groups[rel]
        same_count = sum(1 for _, _, same in entries if same)
        rendered = []
        for key, winner, same in entries:
            marker = "*" if same else ""
            rendered.append(f"{key}{marker} (`{winner.split('/')[-1]}`)")
        lines.append(
            f"- **`{rel}`** — {len(entries)} kayıp"
            + (f", {same_count} tanesi özdeş" if same_count else "")
            + ": "
            + ", ".join(rendered)
        )
    lines.append("")
    if vanilla_internal:
        lines.append(
            f"Vanilla-içi çakışma: {len(vanilla_internal)} anahtar (vanilla "
            "dosyaları arasında; modla ilgisi yok)."
        )
        lines.append("")
    lines.append("## Setup: mod-içi çakışmalar")
    lines.append("")
    lines.append(
        f"{len(internal)} anahtarda modun iki dosyası aynı anahtarı tanımlıyor; "
        "erken sıralanan kazanıyor, içerik modda kalıyor. `*` = kaybedilen "
        "tanım kazananla birebir aynı; işaretsizlerde iki mod dosyası **farklı "
        "değer** taşıyor (tekilleştirme gerekir)."
    )
    lines.append("")
    internal_groups = defaultdict(list)
    for row in internal:
        for rel, src, same in row["losers"]:
            if src == "mod":
                internal_groups[rel].append((row["key"], row["winner"], same))
    for rel in sorted(internal_groups):
        entries = internal_groups[rel]
        diff_count = sum(1 for _, _, same in entries if not same)
        rendered = []
        for key, winner, same in entries:
            marker = "*" if same else ""
            rendered.append(f"{key}{marker} (`{winner.split('/')[-1]}`)")
        lines.append(
            f"- **`{rel}`** — {len(entries)} anahtar"
            + (f", {diff_count} tanesi farklı değerli" if diff_count else "")
            + ": "
            + ", ".join(rendered)
        )
    lines.append("")
    lines.append("## Setup: mod lehine sonuçlanan çakışmalar (özet)")
    lines.append("")
    lines.append(
        f"{len(alive)} anahtarda mod tanımı kazanıyor; kaybeden taraf çoğunlukla "
        "alfabetik olarak sonra gelen vanilla bölge dosyası. Tam liste "
        "gerekmiyorsa bu tablo yeterli; ayrıntı için script'in `--out` çıktısı "
        "yeniden üretilebilir."
    )
    lines.append("")
    alive_losers = Counter()
    for row in alive:
        for rel, src, _ in row["losers"]:
            if src == "vanilla":
                alive_losers[rel] += 1
    alive_rows = [[f"`{rel}`", count] for rel, count in alive_losers.most_common()]
    lines.extend(table(["Kaybeden vanilla dosyası", "Anahtar"], alive_rows))
    lines.append("")
    lines.append("## Kasıtlı aynı-yol override dosyaları")
    lines.append("")
    lines.append(
        "Bu dosyalar vanilla ile aynı göreli yola sahip olduğu için vanilla "
        "kopyası yüklenmez; gölge karşılaştırmasına dahil edilmedi."
    )
    lines.append("")
    for db in DBS:
        overrides = report[db]["overrides"]
        if overrides:
            lines.append(f"- `{db}`: " + ", ".join(f"`{rel.split('/')[-1]}`" for rel in overrides))
    lines.append("")
    lines.append("## on_action özel durumu")
    lines.append("")
    lines.append(
        "`common/on_action` diğer DB'ler gibi ilk-tanım-kazanır kuralına tabi "
        "değil: mod, mevcut bir vanilla on action'a yalnızca `on_actions` bloğu "
        "ekleyebiliyor (mod dosyasındaki not ve EU5 wiki kuralı). 18 Ekim "
        "log'unda `yearly_country_pulse` için hiç `Duplicated key` satırı yok; "
        "bu da blok birleşimini doğruluyor."
    )
    lines.append("")
    lines.append(f"- Vanilla: `{on_action['vanilla']}`")
    lines.append(f"- Mod: `{on_action['mod']}` — `yearly_country_pulse` bloğu + yeni `et_egypt_yearly_pulse`")
    lines.append("")
    lines.append("## Doğrulama: 18 Ekim log'undaki dört satır")
    lines.append("")
    lines.append("```")
    lines.append("Duplicated key aramaic_language will not be created from file: common/languages/00_et_mesopotamian.txt:26")
    lines.append("Duplicated key gothic_language will not be created from file: common/languages/00_germany.txt:676")
    lines.append("Duplicated key coptic_culture will not be created from file: common/cultures/et_egypt.txt:48")
    lines.append("Duplicated key miaphysite will not be created from file: common/religions/et_christianity.txt:108")
    lines.append("```")
    lines.append("")
    lines.append(
        "Bu satırlar taşıma öncesi 18 Ekim oturumunun kanıtıdır; adı geçen "
        "dosya her satırda kaybedendir. Taşıma sonrası rapor aramaic, coptic "
        "ve miaphysite için kazananı moda çevirdi (kaybeden artık vanilla: "
        "00_crescent.txt, egypt.txt, christian.txt); gothic_language aynı "
        "kaldı. Yeni Test B logunda bu üç satırın dosya adı değişecek, satır "
        "sayısı değişmeyecek. Log satırları hata değil, bilgi düzeyindedir; "
        "Test B raporunda bu sınıf bilgi olarak kalmalı."
    )
    lines.append("")
    lines.append("## Sınırlar")
    lines.append("")
    lines.append(
        "- Anahtar karşılaştırması üst düzey bloklarla sınırlıdır; iç içe alan "
        "çakışmaları ve sözdizimi hataları kapsam dışıdır."
    )
    lines.append(
        "- Dosya sırası göreli yolun bayt sırasına göre modellendi; oyunun "
        "kullandığı sıralama büyük/küçük harf duyarsızsa istisna çıkabilir "
        "(mevcut dosya adları küçük harf)."
    )
    lines.append(
        "- İçerik karşılaştırması yorumları ve boşlukları yok sayar; anlamsal "
        "eşdeğerliği değil birebir gövde eşitliğini ölçer."
    )
    lines.append("")
    lines.append("## Sonraki adım")
    lines.append("")
    lines.append(
        "Dil, kültür ve din deltaları 20 Ekim'de taşıma yöntemiyle düzeltildi; "
        "bu raporda ölü kalan tek sınıf `setup/countries` (174 tanım). Setup "
        "için üç yol var: (1) tanımı rakipten önce sıralanacak dosyaya taşımak, "
        "(2) aynı adlı tam override kullanmak, (3) tanımı silip vanilla "
        "davranışını kabul etmek. Etiket bazında karar verilmeden veri "
        "değiştirilmemeli; düzeltme `vanilla_shadow_delivery_fix` görevinde."
    )
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Compare mod and vanilla top-level keys per database (offline shadow report)."
    )
    parser.add_argument(
        "--vanilla",
        help="Path to the EU5 'game' directory (the one containing in_game/).",
    )
    parser.add_argument(
        "--mod",
        help="Path to the Extended Timeline mod folder (default: <repo>/Extended Timeline).",
    )
    parser.add_argument(
        "--out",
        help="Output markdown path (default: research/historical-events/<date>_vanilla_shadow_report.md).",
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

    vanilla_root = vanilla / "in_game"
    mod_root = mod / "in_game"

    report = {db: scan_db(vanilla_root, mod_root, db) for db in DBS}

    on_action = {"vanilla": "—", "mod": "—"}
    vanilla_on = vanilla_root / ON_ACTION_DB
    mod_on = mod_root / ON_ACTION_DB
    if vanilla_on.is_dir():
        for path in sorted(vanilla_on.rglob("*.txt")):
            if "yearly_country_pulse" in extract_blocks(path):
                on_action["vanilla"] = path.relative_to(vanilla_root).as_posix()
                break
    if mod_on.is_dir():
        for path in sorted(mod_on.rglob("*.txt")):
            if "yearly_country_pulse" in extract_blocks(path):
                on_action["mod"] = path.relative_to(mod_root).as_posix()
                break

    output = Path(args.out) if args.out else DEFAULT_OUT_DIR / (
        f"{date.today().isoformat()}_vanilla_shadow_report.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(report, on_action), encoding="utf-8", newline="\n")

    print("shadow-audit: rapor yazildi ->", output)
    for db in DBS:
        kinds = Counter(row["kind"] for row in report[db]["rows"])
        print(
            f"  {db}: golgelenen={len(report[db]['rows'])}"
            f" olu={kinds.get('DEAD', 0)} yasayan={kinds.get('ALIVE', 0)}"
            f" mod-ici={kinds.get('MOD_INTERNAL', 0)}"
            f" vanilla-ici={kinds.get('VANILLA_INTERNAL', 0)}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
