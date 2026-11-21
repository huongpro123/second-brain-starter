#!/usr/bin/env python3
"""Render file AutoCAD DXF ra anh PNG (khong can cai AutoCAD) de AI va nguoi nhin kiem tra.

Chay:
  python tools/draw/dxf_to_png.py "./out/ban-ve.dxf" [--out "./out/preview.png"] [--dpi 200] [--dark]
"""
import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import ezdxf
    from ezdxf.addons.drawing.matplotlib import qsave
except ImportError:
    sys.exit("Thieu thu vien ezdxf. Chay: python -m pip install ezdxf")


def render_dxf(dxf_path: Path, out_png: Path, dpi: int = 200, dark: bool = False) -> Path:
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()

    bg = "#141418" if dark else "#FFFFFF"
    fg = "#FFFFFF" if dark else "#000000"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    qsave(msp, str(out_png), bg=bg, fg=fg, dpi=dpi)
    return out_png


def main() -> None:
    ap = argparse.ArgumentParser(description="Render DXF sang PNG de kiem tra truc quan")
    ap.add_argument("dxf")
    ap.add_argument("--out", help="Duong dan file PNG dau ra (mac dinh cung ten .png)")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--dark", action="store_true", help="Nen toi giong AutoCAD Modelspace (mac dinh nen trang)")
    a = ap.parse_args()

    dxf_path = Path(a.dxf)
    if not dxf_path.exists():
        sys.exit(f"Khong thay file: {dxf_path}")
    out_png = Path(a.out) if a.out else dxf_path.with_suffix(".png")

    render_dxf(dxf_path, out_png, dpi=a.dpi, dark=a.dark)
    print(f"RENDERED {out_png}")


if __name__ == "__main__":
    main()
