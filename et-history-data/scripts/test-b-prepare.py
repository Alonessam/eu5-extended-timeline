#!/usr/bin/env python3
"""Test B oncesi hazirlik araci (Extended Timeline).

Yaptiklari:
  1. et-history-data/tests/<zaman>_test_b/ kosum klasoru acar.
  2. Canli oyun loglarini (debug.log, error.log, code_revisions.log)
     <klasor>/before/ altina yedekler.
  3. debug.log ve error.log'u siler; oyun bir sonraki oturumda tertemiz
     dosyalar yazar (Test B kanit izi).
  4. run_info.txt: git revizyonu, kirli dosyalar, duzeltilmis mod
     dosyalarinin sha256 ozetleri, log durumu, oyun surumu.
  5. Sirada yapilacaklari ekrana yazar.

Kullanim:
  python et-history-data/scripts/test-b-prepare.py
  python et-history-data/scripts/test-b-prepare.py --logs "D:\\...\\logs"
  python et-history-data/scripts/test-b-prepare.py --keep   (yalniz yedekle)

Not: Oyun kapaliyken calistirin (log dosyalari kilitli olabilir).
Protokol: et-history-data/research/historical-events/2026-10-19_test_b_protocol.md
"""

import argparse
import hashlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TESTS_DIR = REPO / "et-history-data" / "tests"
DEFAULT_LOGS = (Path.home() / "Documents" / "Paradox Interactive"
                / "Europa Universalis V" / "logs")

BACKUP_FILES = ["debug.log", "error.log", "code_revisions.log"]
CLEAR_FILES = ["debug.log", "error.log"]

MOD_FILES = [
    "Extended Timeline/in_game/events/et_culture_events.txt",
    "Extended Timeline/in_game/common/on_action/et_history_pulses.txt",
    "Extended Timeline/in_game/common/cultures/et_german.txt",
    "Extended Timeline/in_game/common/cultures/et_arabia.txt",
    "Extended Timeline/in_game/common/languages/00_et_germany.txt",
    "Extended Timeline/in_game/common/languages/00_et_balkan.txt",
    "Extended Timeline/in_game/common/languages/00_et_african.txt",
    "Extended Timeline/in_game/common/languages/00_et_central_asia.txt",
    "Extended Timeline/in_game/localization/turkish/et_cultural_and_languages_l_turkish.yml",
    "Extended Timeline/in_game/localization/turkish/replace/et_replace_l_turkish.yml",
    "Extended Timeline/main_menu/localization/turkish/et_cultural_and_languages_l_turkish.yml",
    "Extended Timeline/main_menu/localization/turkish/replace/et_replace_l_turkish.yml",
]


def git(*args: str) -> str:
    res = subprocess.run(["git", "-C", str(REPO), *args],
                         capture_output=True, text=True)
    return res.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_status(path: Path) -> str:
    if not path.exists():
        return "yok"
    st = path.stat()
    return (f"{st.st_size} B | "
            f"{time.strftime('%d.%m.%Y %H:%M', time.localtime(st.st_mtime))}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Test B oncesi log yedegi + temizligi")
    ap.add_argument("--logs", type=Path, default=DEFAULT_LOGS,
                    help="oyun log dizini (varsayilan: Belgeler/Paradox .../logs)")
    ap.add_argument("--keep", action="store_true",
                    help="loglari silme, yalniz yedekle")
    args = ap.parse_args()

    stamp = time.strftime("%Y-%m-%d_%H%M")
    art = TESTS_DIR / f"{stamp}_test_b"
    before = art / "before"
    before.mkdir(parents=True, exist_ok=True)

    print("Test B hazirlik")
    print(f"  kosum klasoru: {art}")
    print()

    status_before = {name: file_status(args.logs / name) for name in BACKUP_FILES}

    copied = 0
    for name in BACKUP_FILES:
        src = args.logs / name
        if src.exists():
            shutil.copy2(src, before / name)
            copied += 1
    print(f"  yedek: {copied} dosya -> {before}")

    if args.keep:
        print("  temizlik: --keep verildi, atlandi")
    else:
        blocked = False
        for name in CLEAR_FILES:
            src = args.logs / name
            if not src.exists():
                print(f"  temizlik: {name} zaten yok")
                continue
            try:
                src.unlink()
                print(f"  temizlik: {name} silindi")
            except PermissionError:
                print(f"  HATA: {name} kilitli - oyunu kapatin ve tekrar deneyin")
                blocked = True
        if blocked:
            return 1

    build = "(yok)"
    rev_backup = before / "code_revisions.log"
    if rev_backup.exists():
        try:
            build = "\n".join(
                rev_backup.read_text(encoding="utf-8", errors="ignore")
                .splitlines()[:12])
        except OSError:
            build = "(okunamadi)"

    lines = []
    lines.append("Test B kosum bilgisi")
    lines.append(f"zaman: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"git rev: {git('rev-parse', 'HEAD')}")
    lines.append(f"git branch: {git('rev-parse', '--abbrev-ref', 'HEAD')}")
    dirty = [l for l in git("status", "--porcelain").splitlines() if l.strip()]
    lines.append(f"kirli dosya: {len(dirty)}")
    lines.extend(f"  {l}" for l in dirty)
    lines.append("")
    lines.append("mod dosya ozetleri (sha256):")
    for rel in MOD_FILES:
        p = REPO / rel
        h = sha256(p) if p.exists() else "YOK"
        lines.append(f"  {h}  {rel}")
    lines.append("")
    lines.append("log durumu (temizlik oncesi):")
    for name in BACKUP_FILES:
        lines.append(f"  {name}: {status_before[name]}")
    lines.append("")
    lines.append("oyun surumu (code_revisions.log):")
    lines.append(build)
    (art / "run_info.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  run_info.txt yazildi")

    print()
    print("Sirada:")
    print("  1) Oyunu console+debug ile baslatin:")
    print('     "C:\\Users\\samet\\Desktop\\Europa Universalis V\\binaries\\eu5.exe"'
          " -debug_mode -console")
    print("     (veya Steam baslatma seceneklerine -debug_mode -console ekleyin)")
    print("  2) Protokolu uygulayin:")
    print("     et-history-data/research/historical-events/2026-10-19_test_b_protocol.md")
    print("  3) Oturum bitince raporu uretin:")
    print("     python et-history-data/scripts/test-b-report.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
