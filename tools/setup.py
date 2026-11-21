#!/usr/bin/env python3
"""Bo khoi tao nhanh ("Phong Thoi Gian") cho Second Brain Starter + CTUT Report Kit.

Chay duoc tren Windows, macOS va Linux:
  python tools/setup.py          # tao .venv, cai requirements, bat git hooks, kiem tra he thong
  python tools/setup.py --check  # chi kiem tra moi truong & vault (khong sua/cai gi)
  python tools/setup.py --venv   # chi tao .venv + cai thu vien Python
  python tools/setup.py --hooks  # chi bat .githooks (pre-commit chong lo bi mat)
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = ROOT / ".venv"


def _venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _find_cmd(*names: str):
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def _find_soffice():
    found = _find_cmd("soffice", "libreoffice")
    if found:
        return found
    for cand in (
        r"C:\Program Files\LibreOffice\program\soffice.com",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.com",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ):
        if Path(cand).exists():
            return cand
    return None


def setup_venv() -> Path:
    vpy = _venv_python()
    if not vpy.exists():
        print(f"[+] Dang tao moi truong ao: {VENV_DIR}")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    else:
        print(f"[=] Da co .venv: {VENV_DIR}")

    req = ROOT / "requirements.txt"
    if req.exists():
        print("[+] Dang cai thu vien tu requirements.txt ...")
        subprocess.run([str(vpy), "-m", "pip", "install", "--upgrade", "pip"], check=False)
        subprocess.run([str(vpy), "-m", "pip", "install", "-r", str(req)], check=True)
    return vpy


def setup_hooks() -> None:
    if not (ROOT / ".git").exists():
        print("[!] Chua khoi tao Git (khong thay .git), bo qua bat git hooks.")
        return
    hooks_dir = ROOT / ".githooks"
    if not hooks_dir.exists():
        print("[!] Khong thay thu muc .githooks.")
        return
    subprocess.run(["git", "-C", str(ROOT), "config", "core.hooksPath", ".githooks"], check=True)
    pre_commit = hooks_dir / "pre-commit"
    if os.name != "nt" and pre_commit.exists():
        pre_commit.chmod(0o755)
    print("[+] Da bat git hooks (.githooks/pre-commit).")


def check_environment(py_exec: Path) -> bool:
    print("\n=== 1. KIEM TRA CONG CU HE THONG ===")
    print(f"  He dieu hanh : {platform.system()} {platform.release()}")
    print(f"  Thu muc vault: {ROOT}")
    print(f"  Python       : {py_exec}")

    for label, cmd in (
        ("Git", _find_cmd("git")),
        ("GitHub CLI (gh)", _find_cmd("gh")),
        ("PowerShell", _find_cmd("pwsh", "powershell")),
        ("LibreOffice", _find_soffice()),
    ):
        status = cmd if cmd else "CHUA CO (tuy chon)"
        print(f"  {label:<16}: {status}")

    print("\n=== 2. KIEM TRA THU VIEN PYTHON ===", flush=True)
    check_code = (
        "import importlib\n"
        "mods = [('docx','python-docx (BAT BUOC)'), ('PIL','pillow'), "
        "('pymupdf','pymupdf (tuy chon render PDF)'), ('win32com.client','pywin32 (Windows Word COM)')]\n"
        "for m, label in mods:\n"
        "    try:\n"
        "        importlib.import_module(m)\n"
        "        print(f'  [OK]   {label}', flush=True)\n"
        "    except ImportError:\n"
        "        print(f'  [MISS] {label}', flush=True)\n"
    )
    subprocess.run([str(py_exec), "-c", check_code], check=False)

    print("\n=== 3. KIEM TRA SUC KHOE VAULT ===", flush=True)
    ps = _find_cmd("pwsh", "powershell")
    hc = ROOT / "tools" / "health-check.ps1"
    vault_ok = True
    if ps and hc.exists():
        cmd = [ps]
        if Path(ps).stem.lower() == "powershell":
            cmd += ["-ExecutionPolicy", "Bypass"]
        cmd += ["-File", str(hc)]
        res = subprocess.run(cmd, cwd=str(ROOT), check=False)
        vault_ok = res.returncode == 0
    else:
        print("  [!] Khong thay PowerShell, bo qua health-check.ps1.", flush=True)

    print("\n=== 4. KIEM TRA BO MAU WORD (cham-loat.py) ===", flush=True)
    cham = ROOT / "tools" / "word" / "cham-loat.py"
    tpl = ROOT / "templates" / "word"
    tpl_ok = True
    if cham.exists() and tpl.exists():
        res = subprocess.run([str(py_exec), str(cham), str(tpl)], cwd=str(ROOT), check=False)
        tpl_ok = res.returncode == 0

    return vault_ok and tpl_ok


def print_global_prompt() -> None:
    vpath = ROOT.as_posix()
    print("\n=== 5. PROMPT TOAN CUC SAN DUONG DAN MAY NAY ===", flush=True)
    print("Neu muon agent o CAC REPO KHAC cung dung duoc vault nay, dan khoi sau vao")
    print("~/.claude/CLAUDE.md, ~/.codex/AGENTS.md, hoac Global Rules cua Antigravity/Cursor:\n")
    print("-" * 72)
    print(f"""# Second Brain & Quy trinh Bao cao CTUT (Con tro toan cuc)

Vault goc: `{vpath}`

1. Khi bat dau du an hoac task moi: doc `{vpath}/AGENTS.md` va `{vpath}/index.md` truoc (chi mo 1-3 note lien quan, khong quet ca vault).
2. Khi cham toi: bao cao, do an, NCKH, luan van, KLTN, TTTN, bia, Word, format, in an, so lieu, viet chuong:
   - Doc theo thu tu: `{vpath}/skills/bao-cao-ctut/SKILL.md` -> `{vpath}/wiki/quy-trinh/quy-trinh-bao-cao-ctut.md` -> `{vpath}/wiki/quy-trinh/luat-viet-noi-dung.md` -> `{vpath}/wiki/quy-trinh/quy-uoc-viet-van-khoa-hoc.md`.
   - Khong bia so lieu, khong bia nguon; thieu so ghi `[CAN SO LIEU: ...]`.
   - Khi phan bien/ra soat truoc khi nop: doc `{vpath}/skills/phan-bien-bao-cao/SKILL.md`.""")
    print("-" * 72)


def main() -> None:
    ap = argparse.ArgumentParser(description="Setup nhanh Second Brain Starter + CTUT Report Kit")
    ap.add_argument("--check", action="store_true", help="Chi kiem tra moi truong va vault, khong cai dat")
    ap.add_argument("--venv", action="store_true", help="Tao .venv va cai requirements.txt")
    ap.add_argument("--hooks", action="store_true", help="Bat git pre-commit hook (.githooks)")
    ap.add_argument("--all", action="store_true", help="Chay day du venv + hooks + kiem tra")
    a = ap.parse_args()

    do_all = a.all or (not a.check and not a.venv and not a.hooks)
    py_exec = _venv_python() if _venv_python().exists() else Path(sys.executable)

    if do_all or a.venv:
        py_exec = setup_venv()
    if do_all or a.hooks:
        setup_hooks()

    ok = check_environment(py_exec)
    print_global_prompt()

    if not ok:
        print("\n[!] Co canh bao o buoc kiem tra. Xem chi tiet phia tren.")
        sys.exit(1)
    print("\n[OK] Setup va kiem tra hoan tat.")


if __name__ == "__main__":
    main()
