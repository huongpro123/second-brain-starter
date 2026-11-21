#!/usr/bin/env python3
"""Cham diem dinh dang nhieu file .docx cung luc (goi kiem-tra.py --json).

Vi du:
  python cham-loat.py "D:\\du-an"                  # quet ca thu muc
  python cham-loat.py file1.docx file2.docx --md bao-cao-cham.md
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIEM_TRA = HERE / "kiem-tra.py"


def quet(paths):
    files = []
    for p in paths:
        q = Path(p)
        if q.is_dir():
            files += [f for f in q.rglob("*.docx") if not f.name.startswith("~$")]
        elif q.suffix.lower() == ".docx" and q.exists():
            files.append(q)
    return sorted(set(files), key=lambda f: str(f).lower())


def cham(f):
    r = subprocess.run([sys.executable, str(KIEM_TRA), str(f), "--json"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        data = json.loads(r.stdout)
        return data[0] if data else {"file": str(f), "diem": 0, "muc_loi": ["không đọc được kết quả"]}
    except json.JSONDecodeError:
        return {"file": str(f), "diem": 0, "muc_loi": ["lỗi chấm: " + (r.stderr or "")[:80]]}


def main():
    ap = argparse.ArgumentParser(description="Cham diem dinh dang hang loat")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--md", help="ghi bang markdown ra file")
    ap.add_argument("--duoi", type=int, default=0, help="chi in file co diem < N")
    a = ap.parse_args()

    files = quet(a.paths)
    if not files:
        sys.exit("Không tìm thấy file .docx nào.")
    rows = [cham(f) for f in files]
    rows.sort(key=lambda r: (r.get("diem", 0), str(r.get("file", ""))))

    print(f"{'ĐIỂM':>5}  FILE")
    print("-" * 72)
    for r in rows:
        d = r.get("diem", 0)
        if a.duoi and d >= a.duoi:
            continue
        print(f"{d:>5}  {r.get('file')}")
        for m in (r.get("muc_loi") or [])[:2]:
            print(f"       ✗ {m}")
        for w in (r.get("canh_bao") or [])[:1]:
            print(f"       ! {w}")

    if a.md:
        lines = ["| Điểm | File | Lỗi chính |", "|---:|---|---|"]
        for r in rows:
            loi = "; ".join((r.get("muc_loi") or [])[:2]) or "—"
            lines.append(f"| {r.get('diem', 0)} | `{Path(r.get('file','')).name}` | {loi} |")
        Path(a.md).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nĐã ghi {a.md}")

    tb = sum(r.get("diem", 0) for r in rows) / len(rows)
    print(f"\n{len(rows)} file · điểm trung bình {tb:.0f}/100 · "
          f"{(sum(1 for r in rows if r.get('diem',0)>=90))} file ≥ 90")


if __name__ == "__main__":
    main()
