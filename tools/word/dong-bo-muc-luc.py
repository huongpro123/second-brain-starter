#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dong bo so trang MUC LUC (TOC field dang cache) theo bo cuc that trong PDF.

Cach dung:
    python dong-bo-muc-luc.py "bao-cao.docx"            # tu convert docx -> pdf bang soffice
    python dong-bo-muc-luc.py "bao-cao.docx" --pdf "x.pdf"

Canh bao: TOC la ket qua cache cua field; tool nay chi ghi lai SO TRANG,
khong tao lai danh sach muc. Neu ban them/bot heading, hay cap nhat TOC trong Word.
"""
import argparse, re, shutil, subprocess, sys, tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        pymupdf = None

from docx import Document


def _find_soffice():
    """Tim LibreOffice (soffice) trong PATH hoac vi tri mac dinh."""
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
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


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").lower().strip()


def to_pdf(docx: Path) -> Path:
    soffice = _find_soffice()
    if not soffice:
        sys.exit("Khong tim thay LibreOffice (soffice). Hay cai LibreOffice hoac truyen --pdf <file.pdf>.")
    out = Path(tempfile.mkdtemp(prefix="toc-"))
    subprocess.run([soffice, "--headless", "--norestore", "--convert-to", "pdf",
                    "--outdir", str(out), str(docx)], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf = out / (docx.stem + ".pdf")
    if not pdf.exists():
        sys.exit(f"Khong convert duoc PDF tu {docx}")
    return pdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--pdf")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if pymupdf is None:
        sys.exit("Thieu thu vien pymupdf. Chay: python -m pip install pymupdf")

    docx = Path(a.docx)
    if not docx.exists():
        sys.exit(f"Khong thay file: {docx}")
    pdf = Path(a.pdf) if a.pdf else to_pdf(docx)

    doc = Document(str(docx))
    paras = doc.paragraphs
    texts = [p.text.strip() for p in paras]
    upper = [t.upper() for t in texts]

    def find_heading(key):
        for i, t in enumerate(upper):
            if t.startswith(key):
                return i
        return -1

    i_toc = find_heading("MỤC LỤC")
    i_next = find_heading("DANH MỤC BẢNG BIỂU")
    if i_toc < 0:
        sys.exit("Khong tim thay heading MUC LUC")
    if i_next <= i_toc:
        i_next = len(paras)

    # heading de doi chieu: Heading 1..3 nam sau MUC LUC
    heads = [(i, texts[i]) for i, p in enumerate(paras)
             if i > i_toc and p.style.name.startswith("Heading") and texts[i]]

    # dong TOC: co tab + so trang o cuoi
    toc = []
    for i in range(i_toc + 1, i_next):
        t = texts[i]
        if "\t" not in t:
            continue
        label, num = t.rsplit("\t", 1)
        if num.strip().isdigit() and label.strip():
            toc.append((i, label.strip(), int(num)))

    if not toc:
        sys.exit("Khong tim thay dong MUC LUC nao (co tab + so trang)")

    d = pymupdf.open(str(pdf))
    pages = [norm(p.get_text()) for p in d]

    # heading thuc su = dong chu dam va co size >= 12.4pt (tranh match chuoi trong van xuoi)
    def heading_lines(page):
        out = set()
        for blk in page.get_text("dict")["blocks"]:
            for line in blk.get("lines", []):
                spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
                if not spans:
                    continue
                bold = [s for s in spans if (s.get("flags", 0) & 16) or "Bold" in s.get("font", "")]
                big = [s for s in spans if s.get("size", 0) >= 12.4]
                if bold and big and len(bold) == len(spans):
                    txt = norm(" ".join(s["text"] for s in spans))
                    if txt:
                        out.add(txt)
        return out

    heads_pages = [heading_lines(pg) for pg in d]
    # bo qua cac trang MUC LUC (nhan dien bang dot leader)
    leader = re.compile(r"(?:\.{4,}|…{2,})")
    toc_pages = [i for i, t in enumerate(pages) if len(leader.findall(t)) >= 5]
    start = (max(toc_pages) + 1) if toc_pages else 0
    print(f"PDF: {pdf.name} ({len(pages)} trang) | TOC: {len(toc)} dong | "
          f"trang muc luc: {[i+1 for i in toc_pages]}")

    changed = 0
    cur = 0
    for (pi, label, old) in toc:
        nl = norm(label)
        # tim heading tuong ung (tuan tu)
        hi = None
        for k, (hidx, htext) in enumerate(heads):
            if k < cur:
                continue
            if norm(htext) == nl:
                hi = k
                break
        if hi is None:
            continue
        cur = hi
        target = norm(heads[hi][1])
        page = None
        for pno in range(start, len(pages)):
            hp = heads_pages[pno]
            if target in hp or any(target in h for h in hp):
                page = pno + 1
                break
        if page is None:
            continue
        if page != old:
            changed += 1
            par = paras[pi]
            if par.runs:
                if not a.dry_run:
                    par.runs[0].text = f"{label}\t{page}"
                    for r in par.runs[1:]:
                        r.text = ""
            print(f"  {label[:52]:54s} {old:>3d} -> {page}")

    if not a.dry_run and changed:
        doc.save(str(docx))
        print(f"SAVED {docx} ({changed} dong sua)")
    else:
        print(f"{changed} dong lech" + (" (dry-run, khong ghi)" if a.dry_run else ""))


if __name__ == "__main__":
    main()
