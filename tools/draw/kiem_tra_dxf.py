#!/usr/bin/env python3
"""Kiem tra chat luong hinh hoc & layer cua file AutoCAD DXF truoc khi render/nop.

Chay:
  python tools/draw/kiem_tra_dxf.py "./out/ban-ve.dxf" [--json]
"""
import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import ezdxf
    from ezdxf import bbox
except ImportError:
    sys.exit("Thieu thu vien ezdxf. Chay: python -m pip install ezdxf")


def kiem_tra(dxf_path: Path) -> dict:
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    findings = []

    entities = list(msp)
    layers_used = sorted({e.dxf.layer for e in entities})
    layer0_count = sum(1 for e in entities if e.dxf.layer == "0" and e.dxftype() != "INSERT")
    if layer0_count > 0:
        findings.append(("WARN", "LAYER_0", f"Co {layer0_count} doi tuong nam tren layer mac dinh '0' — nen dua vao layer nghiep vu."))

    # Kiem tra chieu cao chu va trung vi tri text
    tiny_texts = []
    text_positions = []
    for e in entities:
        if e.dxftype() in ("TEXT", "MTEXT"):
            h = getattr(e.dxf, "height", getattr(e.dxf, "char_height", 2.5))
            if h < 1.8:
                tiny_texts.append((e.dxf.text if e.dxftype() == "TEXT" else e.text)[:30])
            ins = getattr(e.dxf, "insert", None)
            if ins is not None:
                text_positions.append((round(ins.x, 1), round(ins.y, 1), e.dxftype()))

    if tiny_texts:
        findings.append(("WARN", "CHU_NHO", f"Co {len(tiny_texts)} doan chu cao < 1.8mm (kho doc khi in A3/A4): {tiny_texts[:3]}"))

    # Kiem tra bounding box tong the
    ext = bbox.extents(msp)
    bounds = None
    if ext.has_data:
        w = ext.extmax.x - ext.extmin.x
        h = ext.extmax.y - ext.extmin.y
        bounds = {
            "x_min": round(ext.extmin.x, 2),
            "y_min": round(ext.extmin.y, 2),
            "x_max": round(ext.extmax.x, 2),
            "y_max": round(ext.extmax.y, 2),
            "width": round(w, 2),
            "height": round(h, 2),
        }
        if ext.extmin.x < -1.0 or ext.extmin.y < -1.0:
            findings.append(("WARN", "TOA_DO_AM", f"Co doi tuong nam o toa do am ({bounds['x_min']}, {bounds['y_min']})."))
        if w > 500 or h > 400:
            findings.append(("INFO", "KHO_LON", f"Kich thuoc tong the {w:.1f}x{h:.1f} mm lon hon kho A3 — kiem tra lai ty le ve."))
    else:
        findings.append(("FAIL", "BAN_VE_RONG", "Modelspace khong co doi tuong hinh hoc nao."))

    # Kiem tra trung lap text cung toa do
    seen = {}
    dup_pos = 0
    for x, y, _ in text_positions:
        k = (round(x, 0), round(y, 0))
        seen[k] = seen.get(k, 0) + 1
    dup_pos = sum(1 for v in seen.values() if v > 1)
    if dup_pos:
        findings.append(("WARN", "TEXT_DE_NHAU", f"Co {dup_pos} vi tri co >= 2 nhan text trung toa do gan nhau — can mo PNG kiem tra de chu."))

    fail_cnt = sum(1 for lvl, _, _ in findings if lvl == "FAIL")
    warn_cnt = sum(1 for lvl, _, _ in findings if lvl == "WARN")
    diem = max(0, 100 - fail_cnt * 30 - warn_cnt * 10)

    return {
        "file": str(dxf_path),
        "dxfversion": doc.dxfversion,
        "entities": len(entities),
        "layers_used": layers_used,
        "bounds_mm": bounds,
        "diem": diem,
        "findings": [{"muc": l, "ma": c, "chi_tiet": m} for l, c, m in findings],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Kiem tra chat luong DXF")
    ap.add_argument("dxf")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    p = Path(a.dxf)
    if not p.exists():
        sys.exit(f"Khong thay file: {p}")

    res = kiem_tra(p)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    print(f"=== {res['file']} ({res['dxfversion']}) ===")
    print(f"Doi tuong: {res['entities']} | Layers: {', '.join(res['layers_used'])}")
    if res["bounds_mm"]:
        b = res["bounds_mm"]
        print(f"Pham vi  : {b['width']} x {b['height']} mm  [({b['x_min']}, {b['y_min']}) -> ({b['x_max']}, {b['y_max']})]")
    if not res["findings"]:
        print("  ✓ Khong phat hien loi hinh hoc / layer.")
    for f in res["findings"]:
        print(f"  [{f['muc']}] {f['ma']}: {f['chi_tiet']}")
    print(f"DIEM DXF : {res['diem']}/100")


if __name__ == "__main__":
    main()
