#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dung lai trang bia Mau 1 (QD 886/SV04) cho bao cao tong ket NCKH.

Mau 1 (QD 886/2022, p22): khung trang (anh nen) + TRUONG/KHOA 13 + logo CTUT 3.3cm
+ "BAO CAO TONG KET" 16 + ten de tai 16-20 + 2 khoi GVHD/SVTH 13
+ "Can Tho, <thang>/<nam>" 13.

Cach dung:
  python bia-sv04.py --file Bao_cao.docx --ten "..." --sv "Nguyen Van A" \
      --mssv MSSV001 --nganh "..." --gvhd "ThS. Giang Vien A" \
      --ma-so DTSV20XX-XX [--khoa "DIEN - DIEN TU"] [--thang 11] [--nam 2026]
  python bia-sv04.py --file template.docx --template
"""
import argparse
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

FONT = "Times New Roman"
ALIGN = {"center": WD_ALIGN_PARAGRAPH.CENTER, "left": WD_ALIGN_PARAGRAPH.LEFT,
         "right": WD_ALIGN_PARAGRAPH.RIGHT, "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}
LOGO = Path(__file__).resolve().parents[2] / "templates" / "word" / "img" / "logo-ctut.png"


def P(container, text="", size=13, bold=False, italic=False, align="center",
      sb=0, sa=0, line=1.0, color=None, anchor=None):
    doc = container._doc if hasattr(container, "_doc") else container
    if anchor is None:
        p = doc.add_paragraph()
    else:
        p = doc.add_paragraph()
        anchor._p.addprevious(p._p)
    pf = p.paragraph_format
    pf.alignment = ALIGN[align]
    pf.space_before = Pt(sb)
    pf.space_after = Pt(sa)
    pf.line_spacing = line
    pf.first_line_indent = Cm(0)
    if text:
        r = p.add_run(text)
        r.font.name = FONT
        r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        if color:
            from docx.shared import RGBColor
            r.font.color.rgb = RGBColor.from_string(color)
    return p


def rule_under(p, color="1F3864", sz=6, left_right="4.5"):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    b.set(qn("w:val"), "single")
    b.set(qn("w:sz"), str(sz))
    b.set(qn("w:space"), "1")
    b.set(qn("w:color"), color)
    pbdr.append(b)
    pPr.append(pbdr)
    p.paragraph_format.left_indent = Cm(4.5)
    p.paragraph_format.right_indent = Cm(4.5)



def chen_khung_bia(doc):
    """Chen khung bia (anh PNG nen trang) vao paragraph cuoi trang bia.

    Dung anh thay vi page border vi LibreOffice bo qua display="firstPage"
    va ve khung tren moi trang; Word thi ton trong nhung mau in tu Word khac.
    Anh cao dung 29.7cm nen khong lam lech layout (wrapNone, behindDoc).
    """
    from docx.shared import Cm
    from docx.oxml import OxmlElement
    import copy as _copy
    png = Path(__file__).resolve().parent.parent.parent / 'templates' / 'word' / 'img' / 'khung-bia-sv04.png'
    if not png.exists():
        print('(!) khong thay khung-bia-sv04.png — bo qua khung')
        return
    anchor_par = None
    for par in doc.paragraphs[:25]:
        if par.text.strip().startswith('Cần Thơ'):
            anchor_par = par
    if anchor_par is None:
        anchor_par = doc.paragraphs[0]
    run = anchor_par.add_run()
    run.add_picture(str(png), width=Cm(21), height=Cm(29.7))
    inline = run._element.findall(qn('w:drawing'))[0].find(qn('wp:inline'))
    by = {c.tag.split('}')[1]: _copy.deepcopy(c) for c in inline}
    anc = OxmlElement('wp:anchor')
    for k, v in (('distT', '0'), ('distB', '0'), ('distL', '0'), ('distR', '0'),
                 ('simplePos', '0'), ('relativeHeight', '251658240'), ('behindDoc', '1'),
                 ('locked', '0'), ('layoutInCell', '1'), ('allowOverlap', '1')):
        anc.set(k, v)
    el = OxmlElement('wp:simplePos'); el.set('x', '0'); el.set('y', '0'); anc.append(el)
    for tag in ('wp:positionH', 'wp:positionV'):
        el = OxmlElement(tag); el.set('relativeFrom', 'page')
        off = OxmlElement('wp:posOffset'); off.text = '0'; el.append(off); anc.append(el)
    anc.append(by['extent'])
    ef = OxmlElement('wp:effectExtent')
    for k in ('l', 't', 'r', 'b'):
        ef.set(k, '0')
    anc.append(ef)
    anc.append(OxmlElement('wp:wrapNone'))
    anc.append(by['docPr'])
    if 'cNvGraphicFramePr' in by:
        anc.append(by['cNvGraphicFramePr'])
    anc.append(by['graphic'])
    run._element.findall(qn('w:drawing'))[0].replace(inline, anc)


def frame_first_page(doc, color="1F3864", sz="12", space="14"):
    sectPr = doc.sections[0]._sectPr
    for old in sectPr.findall(qn("w:pgBorders")):
        sectPr.remove(old)
    pg = OxmlElement("w:pgBorders")
    pg.set(qn("w:display"), "firstPage")
    pg.set(qn("w:offsetFrom"), "page")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), sz)
        e.set(qn("w:space"), space)
        e.set(qn("w:color"), color)
        pg.append(e)
    pgMar = sectPr.find(qn("w:pgMar"))
    if pgMar is not None:
        pgMar.addnext(pg)
    else:
        sectPr.append(pg)


def borderless(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "none")
        borders.append(e)
    tblPr.append(borders)


def find_anchor(doc):
    for p in doc.paragraphs:
        if p.style.name == "Heading 1" and "CẢM ƠN" in p.text.upper():
            return p
    raise SystemExit("Khong tim thay heading LOI CAM ON de lam moc chen bia")


def build_cover(doc, v):
    anchor = find_anchor(doc)
    anchor.paragraph_format.page_break_before = True
    old = []
    for ch in doc.element.body.iterchildren():
        if ch is anchor._p:
            break
        old.append(ch)
    # xoa vat the cu
    for ch in old:
        doc.element.body.remove(ch)

    P(doc, v["truong"], 13, align="center", sb=23, sa=2, anchor=anchor)
    p = P(doc, v["khoa"], 13, align="center", sa=6, anchor=anchor)
    rule_under(p)
    P(doc, "", 13, sa=0, anchor=anchor)
    p = P(doc, "", 13, align="center", sb=34, sa=0, anchor=anchor)
    if LOGO.exists():
        r = p.add_run()
        r.add_picture(str(LOGO), width=Cm(3.3))
    P(doc, "", 13, anchor=anchor)
    P(doc, "BÁO CÁO TỔNG KẾT", 16, bold=True, sb=54, sa=0, anchor=anchor)
    P(doc, v["ten"], v["ten_size"], bold=True, sb=34, sa=0, anchor=anchor)

    P(doc, "", 13, sb=108, sa=0, anchor=anchor)
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    borderless(tbl)
    tbl.autofit = False
    c1, c2 = tbl.rows[0].cells
    c1.width = Cm(8.0)
    c2.width = Cm(8.0)

    def cell_par(cell, text, bold=False, size=13, italic=False, first=False):
        par = cell.paragraphs[0] if first else cell.add_paragraph()
        pf = par.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.space_before = Pt(0)
        pf.space_after = Pt(2)
        pf.line_spacing = 1.0
        pf.first_line_indent = Cm(0)
        if text:
            r = par.add_run(text)
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
        return par

    cell_par(c1, "GIẢNG VIÊN HƯỚNG DẪN", bold=True, first=True)
    for line in v["gvhd"]:
        cell_par(c1, line)
    cell_par(c2, "SINH VIÊN THỰC HIỆN", bold=True, first=True)
    if v.get("sv"):
        cell_par(c2, v["sv"])
    if v.get("mssv"):
        cell_par(c2, f"(MSSV: {v['mssv']})")
    if v.get("nganh"):
        cell_par(c2, f"Ngành: {v['nganh']}")
    anchor._p.addprevious(tbl._tbl)

    P(doc, "", 13, sb=66, sa=0, anchor=anchor)
    P(doc, f"Cần Thơ, tháng {v['thang']} năm {v['nam']}", 13, bold=False, anchor=anchor)
    chen_khung_bia(doc)


def build_template_cover(doc):
    build_cover(doc, dict(
        truong="TRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ CẦN THƠ",
        khoa="KHOA ĐIỆN – ĐIỆN TỬ",
        ten="[TÊN ĐỀ TÀI]",
        ten_size=18,
        ma_so="[…………]",
        gvhd=["[Học vị, họ tên GVHD]", "[Học vị, họ tên GVHD 2]"],
        sv="[Họ và tên sinh viên]",
        mssv="[MSSV]",
        nganh="[Tên ngành đào tạo]",
        thang="11",
        nam="2026",
    ))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--truong", default="TRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ CẦN THƠ")
    ap.add_argument("--khoa", default="KHOA ĐIỆN – ĐIỆN TỬ")
    ap.add_argument("--ten", default="[TÊN ĐỀ TÀI]")
    ap.add_argument("--ten-size", type=int, default=18)
    ap.add_argument("--ma-so", default="")
    ap.add_argument("--gvhd", action="append", default=[])
    ap.add_argument("--sv", default="")
    ap.add_argument("--mssv", default="")
    ap.add_argument("--nganh", default="")
    ap.add_argument("--thang", default="11")
    ap.add_argument("--nam", default="2026")
    ap.add_argument("--template", action="store_true")
    a = ap.parse_args()
    f = Path(a.file)
    doc = Document(str(f))
    if a.template:
        build_template_cover(doc)
    else:
        build_cover(doc, dict(
            truong=a.truong, khoa=a.khoa, ten=a.ten, ten_size=a.ten_size,
            ma_so=a.ma_so, gvhd=a.gvhd or ["[Học vị, họ tên GVHD]"],
            sv=a.sv, mssv=a.mssv, nganh=a.nganh, thang=a.thang, nam=a.nam))
    doc.save(str(f))
    print("SAVED", f)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
