#!/usr/bin/env python3
"""Tao khung ban ve ky thuat chuan A3/A4 (.dxf) kem layer IEC/TCVN va khung ten.

Vi du:
  python tools/draw/tao_khung_a3_dxf.py --kho A3 --ten "SO DO MACH DONG LUC" --ma-so "E-01" --out "./out/mau-a3.dxf"
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
    from ezdxf import units
    from ezdxf.enums import TextEntityAlignment
except ImportError:
    sys.exit("Thieu thu vien ezdxf. Chay: python -m pip install ezdxf")


KHO_GIAY = {
    "A3": (420.0, 297.0),
    "A4N": (297.0, 210.0),  # A4 ngang
    "A4D": (210.0, 297.0),  # A4 dung
}

CHUAN_LAYERS = {
    "KHUNG_TEN": {"color": 7, "lineweight": 50, "linetype": "Continuous"},
    "THIET_BI": {"color": 5, "lineweight": 35, "linetype": "Continuous"},
    "DONG_LUC_L1": {"color": 1, "lineweight": 35, "linetype": "Continuous"},
    "DONG_LUC_L2": {"color": 40, "lineweight": 35, "linetype": "Continuous"},
    "DONG_LUC_L3": {"color": 5, "lineweight": 35, "linetype": "Continuous"},
    "TRUNG_TINH_N": {"color": 8, "lineweight": 25, "linetype": "Continuous"},
    "TIEP_DIA_PE": {"color": 3, "lineweight": 25, "linetype": "DASHDOT"},
    "DIEU_KHIEN": {"color": 1, "lineweight": 25, "linetype": "Continuous"},
    "CHU_THICH": {"color": 7, "lineweight": 18, "linetype": "Continuous"},
    "KICH_THUOC": {"color": 3, "lineweight": 18, "linetype": "Continuous"},
}


def dam_bao_linetype(doc) -> None:
    """Them cac kieu net co ban (DASHED, CENTER, DASHDOT) neu DXF chua co."""
    defs = {
        "DASHED": ("Dashed __ __ __", [6.0, 4.0, -2.0]),
        "CENTER": ("Center ____ _ ____", [14.0, 10.0, -2.0, 1.0, -1.0]),
        "DASHDOT": ("Dash dot __ . __", [10.0, 6.0, -1.5, 0.5, -2.0]),
    }
    for name, (desc, pat) in defs.items():
        if name not in doc.linetypes:
            doc.linetypes.add(name, pattern=pat, description=desc)


def dam_bao_layer_va_style(doc) -> None:
    """Khoi tao layer chuan va TextStyle Unicode ARIAL_VN de khong vo dau tieng Viet."""
    dam_bao_linetype(doc)
    for name, cfg in CHUAN_LAYERS.items():
        lt = cfg["linetype"] if cfg["linetype"] in doc.linetypes else "Continuous"
        if name not in doc.layers:
            doc.layers.new(
                name=name,
                dxfattribs={"color": cfg["color"], "lineweight": cfg["lineweight"], "linetype": lt},
            )
    if "ARIAL_VN" not in doc.styles:
        doc.styles.add("ARIAL_VN", font="arial.ttf")


def tao_khung_chuan(
    kho: str = "A3",
    ten: str = "[TEN BAN VE]",
    ma_so: str = "BV-01",
    nguoi_ve: str = "[Ho va ten]",
    gvhd: str = "[Giang vien / Nguoi duyet]",
    don_vi: str = "KHOA DIEN - DIEN TU",
    ty_le: str = "1:1",
    ngay: str = "2026",
):
    """Tao tai lieu ezdxf co khung TCVN, layer chuan va vung ve an toan.

    Tra ve (doc, msp, vung_ve) voi vung_ve = (x_min, y_min, x_max, y_max).
    """
    if kho not in KHO_GIAY:
        raise ValueError(f"Kho giay khong hop le: {kho}. Chon: {list(KHO_GIAY)}")
    w, h = KHO_GIAY[kho]

    doc = ezdxf.new(dxfversion="AC1024", setup=True)
    doc.units = units.MM
    dam_bao_layer_va_style(doc)
    msp = doc.modelspace()

    # Vien ngoai to giay (net manh tham chieu)
    msp.add_lwpolyline([(0, 0), (w, 0), (w, h), (0, h), (0, 0)], dxfattribs={"layer": "KHUNG_TEN", "lineweight": 18})

    # Khung ban ve TCVN: le trai 20 mm (dong tap), 3 le con lai 10 mm
    x0, y0 = 20.0, 10.0
    x1, y1 = w - 10.0, h - 10.0
    msp.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
        dxfattribs={"layer": "KHUNG_TEN", "lineweight": 50},
    )

    # Khung ten o goc phai duoi (140 x 36 mm cho A3/A4N, 120 x 36 mm cho A4D)
    tb_w = 140.0 if w >= 290 else 120.0
    tb_h = 36.0
    tx0, ty0 = x1 - tb_w, y0
    tx1, ty1 = x1, y0 + tb_h
    msp.add_lwpolyline([(tx0, ty0), (tx1, ty0), (tx1, ty1), (tx0, ty1), (tx0, ty0)], dxfattribs={"layer": "KHUNG_TEN"})

    # Chia cac o trong khung ten
    msp.add_line((tx0, ty0 + 24.0), (tx1, ty0 + 24.0), dxfattribs={"layer": "KHUNG_TEN"})
    msp.add_line((tx0, ty0 + 12.0), (tx1, ty0 + 12.0), dxfattribs={"layer": "KHUNG_TEN"})
    mid_x = tx0 + tb_w * 0.62
    msp.add_line((mid_x, ty0), (mid_x, ty0 + 24.0), dxfattribs={"layer": "KHUNG_TEN"})

    def put_txt(txt: str, pos: tuple[float, float], height: float, align=TextEntityAlignment.MIDDLE_CENTER):
        msp.add_text(
            txt,
            height=height,
            dxfattribs={"layer": "CHU_THICH", "style": "ARIAL_VN"},
        ).set_placement(pos, align=align)

    put_txt(don_vi, ((tx0 + tx1) / 2, ty0 + 32.5), 2.5)
    put_txt(ten, ((tx0 + tx1) / 2, ty0 + 27.5), 3.2)
    put_txt(f"Thuc hien: {nguoi_ve}", (tx0 + 2.5, ty0 + 18.0), 2.3, TextEntityAlignment.MIDDLE_LEFT)
    put_txt(f"Duyet: {gvhd}", (tx0 + 2.5, ty0 + 6.0), 2.3, TextEntityAlignment.MIDDLE_LEFT)
    put_txt(f"Ban ve: {ma_so}", ((mid_x + tx1) / 2, ty0 + 18.0), 2.5)
    put_txt(f"Ty le {ty_le} | {ngay}", ((mid_x + tx1) / 2, ty0 + 6.0), 2.3)

    # Vung ve an toan cho noi dung (chua cach le khung & tranh khung ten)
    vung_ve = (x0 + 10.0, y0 + tb_h + 8.0, x1 - 10.0, y1 - 10.0)
    return doc, msp, vung_ve


def main() -> None:
    ap = argparse.ArgumentParser(description="Tao file DXF khung ban ve chuan TCVN/IEC")
    ap.add_argument("--kho", default="A3", choices=list(KHO_GIAY), help="Kho giay A3 | A4N | A4D")
    ap.add_argument("--ten", default="SO DO NGUYEN LY HE THONG")
    ap.add_argument("--ma-so", default="BV-01")
    ap.add_argument("--nguoi-ve", default="[Ho va ten]")
    ap.add_argument("--gvhd", default="[Giang vien huong dan]")
    ap.add_argument("--don-vi", default="KHOA DIEN - DIEN TU")
    ap.add_argument("--ty-le", default="1:1")
    ap.add_argument("--ngay", default="11/2026")
    ap.add_argument("--out", required=True, help="Duong dan file .dxf dau ra")
    a = ap.parse_args()

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc, _, vung_ve = tao_khung_chuan(
        kho=a.kho,
        ten=a.ten,
        ma_so=a.ma_so,
        nguoi_ve=a.nguoi_ve,
        gvhd=a.gvhd,
        don_vi=a.don_vi,
        ty_le=a.ty_le,
        ngay=a.ngay,
    )
    doc.saveas(str(out))
    print(f"SAVED {out} | kho={a.kho} | vung_ve_an_toan={vung_ve}")


if __name__ == "__main__":
    main()
