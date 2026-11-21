#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hoan tat bao cao bang chinh Microsoft Word (COM automation).

Viec tool nay lam ma python-docx / LibreOffice khong lam dung duoc:
  1. cap nhat moi field (PAGE, PAGEREF, TOC, danh muc bang/hinh),
  2. cap nhat MUC LUC bang chinh Word (so trang dung layout Word),
  3. repaginate lai toan bo,
  4. luu .docx va xuat .pdf (wdFormatPDF = 17).

Can: Windows + Microsoft Word (ban desktop) + pywin32
    python -m pip install pywin32

Chay:
    python tools/word/word-hoan-tat.py "bao-cao.docx"                 # cap nhat + xuat PDF cung thu muc
    python tools/word/word-hoan-tat.py "bao-cao.docx" --pdf "x.pdf"   # xuat PDF duong dan khac
    python tools/word/word-hoan-tat.py "bao-cao.docx" --no-save-docx  # chi xuat PDF, khong luu docx

Luu y:
  - Dung tren BAN COPY khi moi thu chua chac: Word luu de len file goc neu --no-save-docx khong bat.
  - Neu Word dang mo file do -> tool se bao loi; dong file trong Word roi chay lai.
  - Khong dung duoc tren may khong co Word (dung `soffice --convert-to pdf` thay the).
"""
import argparse
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

WD_FORMAT_PDF = 17


def export_pdf_word(docx_path: Path, pdf_path: Path = None, save_docx: bool = True, timeout_s: int = 600):
    """Mo file bang Word, cap nhat field/TOC, repaginate, luu docx + xuat PDF."""
    try:
        import win32com.client as win32
    except ImportError:
        sys.exit(
            "Chua co pywin32. Chay:\n"
            "    python -m pip install pywin32\n"
            "roi thu lai. (Neu khong cai duoc, dung LibreOffice: "
            "soffice --headless --convert-to pdf <file>)"
        )

    docx_path = Path(docx_path).resolve()
    if not docx_path.exists():
        sys.exit(f"Khong thay file: {docx_path}")
    pdf_path = Path(pdf_path).resolve() if pdf_path else docx_path.with_suffix(".pdf")

    word = None
    doc = None
    try:
        word = win32.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0          # wdAlertsNone: khong hien hop thoai
        try:
            word.Options.UpdateFieldsAtPrint = True
        except Exception:
            pass
        # word.ScreenUpdating = False

        doc = word.Documents.Open(
            str(docx_path),
            ConfirmConversions=False,
            ReadOnly=False,
            AddToRecentFiles=False,
        )

        # 1) field trong than + header/footer cua moi section
        doc.Fields.Update()
        for sec in doc.Sections:
            for hfs in (sec.Headers, sec.Footers):
                for hf in hfs:
                    try:
                        if hf.Exists:
                            hf.Range.Fields.Update()
                    except Exception:
                        pass

        # 2) MUC LUC (TOC field) va danh muc bang/hinh
        for i in range(1, doc.TablesOfContents.Count + 1):
            doc.TablesOfContents(i).Update()
        try:
            for i in range(1, doc.TablesOfFigures.Count + 1):
                doc.TablesOfFigures(i).Update()
        except Exception:
            pass

        # 3) repaginate + cap nhat lai lan nua (so trang co the doi sau khi TOC dai ra)
        doc.Repaginate()
        doc.Fields.Update()
        for i in range(1, doc.TablesOfContents.Count + 1):
            doc.TablesOfContents(i).Update()
        doc.Repaginate()

        so_trang = int(doc.ComputeStatistics(2)) if hasattr(doc, "ComputeStatistics") else -1  # 2 = wdStatisticPages

        if save_docx:
            doc.Save()
        doc.SaveAs2(str(pdf_path), FileFormat=WD_FORMAT_PDF)
        print(f"OK docx: {docx_path}")
        print(f"OK pdf : {pdf_path}")
        print(f"So trang Word bao: {so_trang}")
        return so_trang
    finally:
        if doc is not None:
            try:
                doc.Close(SaveChanges=False)
            except Exception:
                pass
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass


def main():
    ap = argparse.ArgumentParser(description="Cap nhat field/TOC va xuat PDF bang Microsoft Word")
    ap.add_argument("file", help="file .docx")
    ap.add_argument("--pdf", help="duong dan PDF xuat ra (mac dinh: cung ten .pdf)")
    ap.add_argument("--no-save-docx", action="store_true", help="khong luu lai .docx, chi xuat PDF")
    a = ap.parse_args()
    export_pdf_word(Path(a.file), Path(a.pdf) if a.pdf else None, save_docx=not a.no_save_docx)
    return 0


if __name__ == "__main__":
    sys.exit(main())
