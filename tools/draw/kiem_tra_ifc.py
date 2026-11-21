#!/usr/bin/env python3
"""Kiem tra nhanh file openBIM IFC (.ifc) cho quy trinh Revit <-> BIMvision.

Chay:
  python tools/draw/kiem_tra_ifc.py "./model.ifc" [--json]
Can (tuy chon cho BIM/IFC):
  python -m pip install ifcopenshell
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import ifcopenshell
except ImportError:
    ifcopenshell = None


def kiem_tra_ifc(ifc_path: Path) -> dict:
    if ifcopenshell is None:
        sys.exit(
            "Chua cai thu vien ifcopenshell (tuy chon cho Revit/BIMvision).\n"
            "Chay: python -m pip install ifcopenshell"
        )
    model = ifcopenshell.open(str(ifc_path))
    projects = model.by_type("IfcProject")
    storeys = model.by_type("IfcBuildingStorey")
    products = model.by_type("IfcProduct")

    by_type = Counter(p.is_a() for p in products)
    no_name = sum(1 for p in products if not getattr(p, "Name", None))
    no_guid = sum(1 for p in products if not getattr(p, "GlobalId", None))

    findings = []
    if not projects:
        findings.append(("FAIL", "NO_PROJECT", "Thieu IfcProject goc trong file IFC."))
    if not storeys:
        findings.append(("WARN", "NO_STOREY", "Khong thay IfcBuildingStorey nao — khi mo BIMvision/Revit se kho loc theo tang."))
    if no_guid:
        findings.append(("FAIL", "MISSING_GUID", f"Co {no_guid} doi tuong thieu GlobalId (khong dung duoc cho BCF/BIMvision API)."))
    if no_name:
        findings.append(("WARN", "MISSING_NAME", f"Co {no_name}/{len(products)} doi tuong thieu thuoc tinh Name."))

    return {
        "file": str(ifc_path),
        "schema": model.schema,
        "projects": [p.Name for p in projects],
        "storeys": [s.Name or "(chua dat ten)" for s in storeys],
        "total_products": len(products),
        "top_types": by_type.most_common(12),
        "findings": [{"muc": l, "ma": c, "chi_tiet": m} for l, c, m in findings],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Kiem tra nhanh file IFC cho Revit / BIMvision")
    ap.add_argument("ifc")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    p = Path(a.ifc)
    if not p.exists():
        sys.exit(f"Khong thay file: {p}")

    res = kiem_tra_ifc(p)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    print(f"=== {res['file']} (schema {res['schema']}) ===")
    print(f"Project: {res['projects']} | Tang (Storeys): {len(res['storeys'])} -> {res['storeys']}")
    print(f"Tong doi tuong IfcProduct: {res['total_products']}")
    for t, cnt in res["top_types"]:
        print(f"  - {t}: {cnt}")
    if not res["findings"]:
        print("  ✓ Cau truc IFC co ban sach cho Revit & BIMvision.")
    for f in res["findings"]:
        print(f"  [{f['muc']}] {f['ma']}: {f['chi_tiet']}")


if __name__ == "__main__":
    main()
