#!/usr/bin/env python3
"""Test B sonrasi log raporu (Extended Timeline).

Canli oyun loglarini (debug.log, error.log) kosum klasorune kopyalar,
"moda ait" hatalari ayiklar, UPDATE 19 beklenenlerini ve sinif-1 gizem
anahtarlarini siniflandirir, report.md uretir.

Kullanim:
  python et-history-data/scripts/test-b-report.py
  python et-history-data/scripts/test-b-report.py --dir et-history-data/tests/2026-10-19_1400_test_b
  python et-history-data/scripts/test-b-report.py --vanilla "C:\\...\\game"

Cikis kodu: 0 temiz, 1 inceleme gerekiyor (regresyon ya da yeni bulgu).
"""

import argparse
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TESTS_DIR = REPO / "et-history-data" / "tests"
MOD = REPO / "Extended Timeline"
DEFAULT_LOGS = (Path.home() / "Documents" / "Paradox Interactive"
                / "Europa Universalis V" / "logs")
FALLBACK_VANILLA = Path(r"C:\Users\samet\Desktop\Europa Universalis V\game")

FIXED_FIVE = [
    "proto_germanic_language",
    "old_church_slavonic_language",
    "ancient_greek_language",
    "berber_language",
    "farsi_language",
]

CLASS1_STEMS = [
    "latin_language",
    "occitan_language",
    "mandarin_language",
    "brythonic_language",
    "arabic_language",
    "baltic_language",
    "phoenician_language",
]

KEYREF_RE = re.compile(r"Failed to read key reference:\s*([A-Za-z0-9_]+)")
FILEREF_RE = re.compile(r'in file:\s*"([^"]+)"')
EVENT_RE = re.compile(r"et_culture\.(\d{1,4})")
DEF_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)\s*=\s*\{")
TS_RE = re.compile(r"^\[[^\]]*\]\s*")


def mod_line(line: str) -> bool:
    """Satir moda mi ait: et_ onekli anahtar ya da mod yolu geciyor mu."""
    return bool(re.search(r"(?<![A-Za-z0-9_])(et_[a-z_]+|00_et_[a-z_]+)", line)) \
        or "Extended Timeline" in line


def collect_defs(root: Path) -> set:
    defs = set()
    if not root.exists():
        return defs
    for p in root.rglob("*.txt"):
        try:
            t = p.read_bytes().decode("utf-8-sig", errors="ignore")
        except OSError:
            continue
        defs.update(DEF_RE.findall(t))
    return defs


def read_log(path: Path) -> tuple:
    if not path.exists():
        return None, "", ""
    data = path.read_bytes()
    text = data.decode("utf-8", errors="ignore")
    status = (f"{len(data)} B | "
              f"{time.strftime('%d.%m.%Y %H:%M', time.localtime(path.stat().st_mtime))}")
    return path, text, status


def main() -> int:
    ap = argparse.ArgumentParser(description="Test B sonrasi log raporu")
    ap.add_argument("--logs", type=Path, default=DEFAULT_LOGS)
    ap.add_argument("--dir", type=Path, default=None,
                    help="kosum klasoru (varsayilan: en yeni *_test_b)")
    ap.add_argument("--vanilla", type=Path, default=None,
                    help="vanilla oyun kok dizini (anahtar tanim taramasi icin)")
    args = ap.parse_args()

    if args.dir:
        art = args.dir
    else:
        candidates = sorted(TESTS_DIR.glob("*_test_b")) if TESTS_DIR.exists() else []
        if candidates:
            art = candidates[-1]
        else:
            art = TESTS_DIR / f"{time.strftime('%Y-%m-%d_%H%M')}_test_b_late"
    after = art / "after"
    after.mkdir(parents=True, exist_ok=True)

    vanilla = args.vanilla or FALLBACK_VANILLA
    if not (vanilla / "in_game").exists():
        print(f"UYARI: vanilla dizini bulunamadi: {vanilla}")
        print("  (anahtar tanim siniflamasi sinirli calisacak; --vanilla ile verin)")
        vanilla = None

    print("Test B rapor")
    print(f"  kosum klasoru: {art}")

    # loglari kopyala
    fresh = {}
    for name in ["debug.log", "error.log"]:
        src = args.logs / name
        if src.exists():
            shutil.copy2(src, after / name)
            fresh[name] = True
        else:
            fresh[name] = False
    print("  kopyalandi: " + ", ".join(
        n for n, ok in fresh.items() if ok) if any(fresh.values())
        else "  kopyalanan yok")

    debug_p, debug_t, debug_s = read_log(after / "debug.log")
    err_p, err_t, err_s = read_log(after / "error.log")

    all_lines = []
    for t in (debug_t, err_t):
        all_lines.extend(t.splitlines())

    # ---- ayiklama ----
    scope_all = [l for l in all_lines if "Invalid scope types" in l]
    scope_lines = [l for l in scope_all if "et_culture_events" in l]
    scope_other = [l for l in scope_all if "et_culture_events" not in l]
    german_lines = [l for l in all_lines if "et_german.txt" in l]
    enum_lines = [l for l in all_lines if "EAudioEventOutcome" in l]
    modifier_lines = [l for l in all_lines if "Unknown modifier type" in l]
    keyref_lines = [l for l in all_lines if "Failed to read key reference" in l]
    noise_loc = [l for l in all_lines if "defined in multiple files" in l]
    noise_mount = [l for l in all_lines if "Mounted Data:" in l]
    dupe_lines = [l for l in all_lines
                  if "Duplicated key" in l and l not in german_lines]
    unused_lines = [l for l in all_lines if "is set but is never used" in l]
    notfound_lines = [l for l in all_lines if "could not be found in the database" in l]
    mod_other = [l for l in all_lines
                 if mod_line(l) and l not in scope_all
                 and l not in german_lines and l not in keyref_lines
                 and l not in enum_lines and l not in modifier_lines
                 and l not in noise_loc and l not in noise_mount
                 and l not in dupe_lines and l not in unused_lines
                 and l not in notfound_lines]

    # anahtar ref siniflandirma
    fixed_hits, class1_hits, jewish_hits, mod_file_refs, vanilla_side = [], [], [], [], []
    defs = None
    for l in keyref_lines:
        m = KEYREF_RE.search(l)
        key = m.group(1) if m else "?"
        fm = FILEREF_RE.search(l)
        f = fm.group(1) if fm else ""
        if key in FIXED_FIVE:
            fixed_hits.append(l)
        elif any(key.startswith(s) for s in CLASS1_STEMS):
            class1_hits.append(l)
        elif key == "jewish":
            jewish_hits.append(l)
        elif re.search(r"(?<![A-Za-z0-9_])(et_|00_et_)", f):
            mod_file_refs.append(l)
        else:
            vanilla_side.append(l)

    # tanimsiz anahtar kontrolu (mod dosyali ref'ler icin)
    unknown = []
    if mod_file_refs:
        if defs is None:
            defs = set()
            if vanilla:
                defs |= collect_defs(vanilla / "in_game" / "common" / "languages")
                defs |= collect_defs(vanilla / "in_game" / "common" / "cultures")
            defs |= collect_defs(MOD / "in_game" / "common" / "languages")
            defs |= collect_defs(MOD / "in_game" / "common" / "cultures")
        for l in mod_file_refs:
            m = KEYREF_RE.search(l)
            key = m.group(1) if m else "?"
            if defs and key not in defs:
                unknown.append(l)

    # olay izleri
    events = Counter()
    event_examples = {}
    for l in all_lines:
        for m in EVENT_RE.finditer(l):
            eid = m.group(1)
            events[eid] += 1
            event_examples.setdefault(eid, l.strip()[:160])

    # gruplu diger mod satirlari
    groups = {}
    for l in mod_other:
        sig = TS_RE.sub("", l)
        sig = re.sub(r":\d+", ":N", sig)
        sig = re.sub(r"near line: \d+", "near line: N", sig)
        sig = sig[:110]
        g = groups.setdefault(sig, {"count": 0, "example": l.strip()[:220]})
        g["count"] += 1

    # ---- regresyon degerlendirmesi ----
    regressions = []
    if scope_lines:
        regressions.append(f"kapsam hatasi hala var: {len(scope_lines)} satir")
    if scope_other:
        regressions.append(f"diger dosyalarda kapsam hatasi: {len(scope_other)} satir")
    if german_lines:
        regressions.append(f"et_german.txt satirlari: {len(german_lines)}")
    if enum_lines:
        regressions.append(f"outcome enum (good) satiri: {len(enum_lines)}")
    if modifier_lines:
        regressions.append(f"bilinmeyen modifier satiri: {len(modifier_lines)}")
    if fixed_hits:
        regressions.append(f"duzeltilen 5 dil anahtari ref'i: {len(fixed_hits)}")
    if jewish_hits:
        regressions.append(f"jewish ref'i: {len(jewish_hits)}")
    if unknown:
        regressions.append(f"tanimsiz anahtar ref'i: {len(unknown)}")
    if len(dupe_lines) > 670:
        regressions.append(f"yeni `Duplicated key` satiri: {len(dupe_lines)} (taban 670)")
    if len(unused_lines) > 8:
        regressions.append(f"yeni kullanilmayan degisken uyarisi: {len(unused_lines)} (taban 8)")
    if len(notfound_lines) > 1:
        regressions.append(f"yeni `could not be found` satiri: {len(notfound_lines)} (taban 1)")

    run_info = art / "run_info.txt"
    run_rev = ""
    if run_info.exists():
        for l in run_info.read_text(encoding="utf-8", errors="ignore").splitlines():
            if l.startswith("git rev:"):
                run_rev = l

    # ---- rapor ----
    md = []
    md.append(f"# Test B raporu - {art.name}")
    md.append("")
    md.append(f"- Rapor zamani: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    if run_rev:
        md.append(f"- Kosum bilgisi: {run_rev}")
    md.append(f"- debug.log: {debug_s or 'YOK'}")
    md.append(f"- error.log: {err_s or 'YOK'}")
    md.append("")
    md.append("## 1. Ozet (UPDATE 19 hedefleri)")
    md.append("")
    md.append("| Sinif | 18 Ekim tabani | Simdi | Durum |")
    md.append("|---|---:|---:|---|")
    rows = [
        ("`Invalid scope types ... et_culture_events.txt`", 103, len(scope_lines), "zero"),
        ("Diger dosyalarda kapsam hatasi", 0, len(scope_other), "zero"),
        ("`et_german.txt` hata satiri (40 Duplicated + 29 Unexpected token)",
         69, len(german_lines), "zero"),
        ("`EAudioEventOutcome` `Val \"good\"` (outcome enum)", 13, len(enum_lines),
         "zero"),
        ("`Unknown modifier type` (UPDATE 17 fixleri)", 9, len(modifier_lines), "zero"),
        ("Duzeltilen 5 dil anahtari ref'i", 5, len(fixed_hits), "zero"),
        ("`jewish` ref'i", 4, len(jewish_hits), "zero"),
        ("Sinif-1 anahtar ref'i (gozlem)", "7 anahtar", len(class1_hits), "observe"),
        ("Mod dosyali diger anahtar ref'i", 4, len(mod_file_refs), "zero"),
        ("Tanimsiz anahtar ref'i (yeni eksik)", 4, len(unknown), "zero"),
        ("`Duplicated key` golge satiri (bilgi; et_german haric)", 670,
         len(dupe_lines), "info"),
        ("Kullanilmayan degisken uyarisi (bilgi)", 8, len(unused_lines), "info"),
        ("`could not be found in the database` (bilgi)", 1,
         len(notfound_lines), "info"),
    ]
    for name, base, now, kind in rows:
        if kind == "observe":
            durum = "gozlem"
        elif kind == "info":
            durum = "bilgi" if now <= base else "INCELE"
        else:
            durum = "OK" if now == 0 else "INCELE"
        md.append(f"| {name} | {base} | {now} | {durum} |")
    md.append("")
    md.append(f"- Toplam mod ilgili ayriklanan satir: "
              f"{len(scope_all) + len(german_lines) + len(keyref_lines) + len(enum_lines) + len(modifier_lines) + len(dupe_lines) + len(unused_lines) + len(notfound_lines) + len(mod_other)}")
    md.append(f"- Bilinen gurultu (regresyon sayilmaz): localize coklu-tanim "
              f"{len(noise_loc)} satir, mount bilgisi {len(noise_mount)} satir")
    md.append(f"- Vanilla tarafindaki anahtar ref'leri (bilgi): {len(vanilla_side)}")
    md.append("")
    md.append("## 2. Sinif-1 gozlemi (7 `*_language` anahtari)")
    md.append("")
    if class1_hits:
        md.append(f"{len(class1_hits)} satir bulundu:")
        md.append("")
        md.append("```")
        for l in class1_hits[:40]:
            md.append(l.strip()[:300])
        md.append("```")
    else:
        md.append("Temiz - bu oturumda hicbir sinif-1 anahtari referans hatasi "
                  "vermedi. (18 Ekim'de 7 anahtar basarisizdi; gizemin kapandigi "
                  "yonunde guclu veri.)")
    md.append("")
    regression_lines = (scope_lines + scope_other + german_lines
                        + enum_lines + modifier_lines)
    if regression_lines:
        md.append("### Beklenen-sifir sinif satirlari")
        md.append("")
        md.append("```")
        for l in regression_lines[:40]:
            md.append(l.strip()[:300])
        md.append("```")
        md.append("")
    if jewish_hits:
        md.append("### `jewish` ref'leri")
        md.append("")
        md.append("```")
        for l in jewish_hits[:40]:
            md.append(l.strip()[:300])
        md.append("```")
        md.append("")
    if unknown:
        md.append("### Tanimsiz anahtar ref'leri (yeni eksik)")
        md.append("")
        md.append("```")
        for l in unknown[:30]:
            md.append(l.strip()[:300])
        md.append("```")
        md.append("")
    if mod_file_refs:
        md.append("### Mod dosyali diger anahtar ref'leri")
        md.append("")
        md.append("```")
        for l in mod_file_refs[:30]:
            md.append(l.strip()[:300])
        md.append("```")
        md.append("")
    if dupe_lines:
        md.append("### `Duplicated key` golge satirlari (bilgi)")
        md.append("")
        dupe_files = Counter()
        for l in dupe_lines:
            m = re.search(r"from file:\s*([^:\s]+)", l)
            dupe_files[m.group(1) if m else "?"] += 1
        md.append(f"{len(dupe_lines)} satir (et_german haric); kaybeden dosya "
                  "dagitimi (ilk 8):")
        md.append("")
        for f, c in dupe_files.most_common(8):
            md.append(f"- `{f}`: {c}")
        md.append("")
    if unused_lines:
        var_names = re.findall(r"Variable '([^']+)' is set but is never used",
                               "\n".join(unused_lines))
        md.append("### Kullanilmayan degiskenler (bilgi)")
        md.append("")
        md.append(f"{len(unused_lines)} uyari: "
                  + ", ".join(f"`{n}`" for n in var_names))
        md.append("")
    if notfound_lines:
        md.append("### `could not be found in the database` (bilgi)")
        md.append("")
        md.append("```")
        for l in notfound_lines[:10]:
            md.append(l.strip()[:300])
        md.append("```")
        md.append("")
    md.append("## 3. Diger mod satirlari (gruplu)")
    md.append("")
    if groups:
        for sig, g in sorted(groups.items(), key=lambda kv: -kv[1]["count"]):
            md.append(f"- x{g['count']} - `{sig}`")
            md.append(f"  - ornek: `{g['example']}`")
    else:
        md.append("Mod kaynakli diger hata satiri yok.")
    md.append("")
    md.append("## 4. `et_culture` olay izleri")
    md.append("")
    if events:
        for eid, cnt in sorted(events.items(), key=lambda kv: (len(kv[0]), kv[0])):
            md.append(f"- `et_culture.{eid}`: {cnt} satir")
            md.append(f"  - ornek: `{event_examples[eid]}`")
    else:
        md.append("Loglarda `et_culture.N` biciminde olay izi yok "
                  "(ateşleme kaniti panolar/konsol ciktilariyla).")
    md.append("")
    md.append("## 5. Sonuc")
    md.append("")
    if regressions:
        md.append("**INCELEME GEREKIYOR:**")
        for r in regressions:
            md.append(f"- {r}")
    else:
        md.append("**TEMIZ:** UPDATE 19 hedeflerinin tamami dogrulandi; "
                  "yeni mod kaynakli hata yok.")
    md.append("")

    report = art / "report.md"
    report.write_text("\n".join(md) + "\n", encoding="utf-8")

    print()
    for l in md:
        if l.startswith("|") or l.startswith("#") or l.startswith("**"):
            print("  " + l)
    print()
    print(f"  rapor: {report}")
    print("  SONUC: " + ("INCELEME GEREKIYOR" if regressions else "TEMIZ"))
    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
