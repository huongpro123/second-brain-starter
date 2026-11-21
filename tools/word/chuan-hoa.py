# -*- coding: utf-8 -*-
"""Chuẩn hoá định dạng file Word (.docx) theo chuẩn báo cáo CTUT.

Sửa được (tự động):
  - Khổ giấy A4, lề trên 2 / dưới 2 / trái 3 / phải 2 cm
  - Style Normal: Times New Roman 13pt, giãn dòng 1.5, cách sau 6pt,
    căn đều hai bên, thụt đầu dòng 1cm
  - Heading 1/2/3: Times New Roman, màu đen, 14/13/13pt, đậm
  - Caption (chú thích hình/bảng): Times New Roman 11pt đậm, giữa
  - Chữ xanh Word mặc định trong heading -> đen; chữ đỏ -> đen

KHÔNG sửa được (in ra để bạn tự xử lý):
  - Dòng chấm điền tay (………), nhãn "TÊN ĐỀ TÀI:" thừa
  - Mục lục: phải tự chèn (References > Table of Contents)
  - Số trang tự đánh lại nếu file gốc sai

Cách dùng:
    python chuan-hoa.py "bao-cao.docx"            # -> bao-cao-chuan-hoa.docx
    python chuan-hoa.py "bao-cao.docx" --in-place # ghi đè (tạo .bak trước)
Cần: pip install python-docx
"""
import sys, os, shutil, argparse
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

FONT = 'Times New Roman'
MAU_XANH_WORD = {'365F91', '4F81BD', '1F3864', '2F5597', '4472C4', '5B9BD5', '2E74B5', '1F4E79'}
MAU_DO = {'FF0000', 'C00000', 'E74C3C', 'CC0000'}


def _rpr(el):
    rPr = el.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        el.insert(0, rPr)
    return rPr


def ep_font(rPr, name=FONT):
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rPr.insert(0, rf)
    for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
        k = qn('w:' + a)
        if k in rf.attrib:
            del rf.attrib[k]
    for a in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
        rf.set(qn('w:' + a), name)


def ep_color_den(rPr):
    c = rPr.find(qn('w:color'))
    if c is None:
        c = OxmlElement('w:color')
        rPr.append(c)
    for a in ('themeColor', 'themeShade', 'themeTint'):
        k = qn('w:' + a)
        if k in c.attrib:
            del c.attrib[k]
    c.set(qn('w:val'), '000000')


def sua_style(doc, ten, **kw):
    try:
        st = doc.styles[ten]
    except KeyError:
        print(f'  (bỏ qua) không có style "{ten}"')
        return
    el = st.element
    rPr = _rpr(el)
    ep_font(rPr)
    ep_color_den(rPr)
    if kw.get('size'):
        st.font.size = Pt(kw['size'])
    st.font.bold = kw.get('bold')
    st.font.italic = kw.get('italic')
    pf = st.paragraph_format
    if kw.get('align') is not None:
        pf.alignment = kw['align']
    if kw.get('before') is not None:
        pf.space_before = Pt(kw['before'])
    if kw.get('after') is not None:
        pf.space_after = Pt(kw['after'])
    if kw.get('line') is not None:
        pf.line_spacing = kw['line']
    if kw.get('first_line') is not None:
        pf.first_line_indent = Cm(kw['first_line'])
    if kw.get('keep_next') is not None:
        pf.keep_with_next = kw['keep_next']


def dem(iterable):
    return sum(1 for _ in iterable)


def xu_ly(path, in_place=False):
    doc = Document(path)
    bao_cao = []

    # 1. khổ giấy + lề
    doi_kho = 0
    for s in doc.sections:
        if abs(s.page_width.cm - 21.0) > 0.2 or abs(s.page_height.cm - 29.7) > 0.2:
            doi_kho += 1
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Cm(2.0)
        s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(3.0)
        s.right_margin = Cm(2.0)
    bao_cao.append(f'Đặt A4 + lề 2/2/3/2cm cho {len(doc.sections)} section (đổi khổ: {doi_kho} section)')

    # 2. các style
    sua_style(doc, 'Normal', size=13, bold=False, italic=False,
              align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=6, line=1.5, first_line=1.0)
    sua_style(doc, 'Heading 1', size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
              before=12, after=6, line=1.5, first_line=0, keep_next=True)
    sua_style(doc, 'Heading 2', size=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT,
              before=12, after=6, line=1.5, first_line=0, keep_next=True)
    sua_style(doc, 'Heading 3', size=13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT,
              before=6, after=6, line=1.5, first_line=0, keep_next=True)
    sua_style(doc, 'Caption', size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
              before=6, after=6, line=1.0, first_line=0)
    bao_cao.append('Chuẩn hoá style: Normal 13pt/1.5/justify/thụt 1cm; Heading 1-3 Times New Roman đen; Caption 11pt đậm giữa')

    # 3. chữ xanh trong heading / chữ đỏ trong thân -> đen
    so_xanh = 0
    so_do = 0
    for p in doc.paragraphs:
        st_name = (p.style.name or '').lower()
        la_heading = st_name.startswith('heading')
        for r in p.runs:
            if not r.text.strip():
                continue
            rPr = r._element.find(qn('w:rPr'))
            mau = None
            if r.font.color is not None and r.font.color.rgb:
                mau = str(r.font.color.rgb).upper()
            elif rPr is not None:
                c = rPr.find(qn('w:color'))
                if c is not None:
                    mau = (c.get(qn('w:val')) or '').upper()
                    if c.get(qn('w:themeColor')) and la_heading:
                        mau = mau or 'THEME'
            if la_heading and (mau in MAU_XANH_WORD or mau == 'THEME'):
                r.font.color.rgb = RGBColor(0, 0, 0)
                rPr2 = r._element.find(qn('w:rPr')) or r._element.get_or_add_rPr()
                c = rPr2.find(qn('w:color'))
                if c is not None:
                    for a in ('themeColor', 'themeShade', 'themeTint'):
                        k = qn('w:' + a)
                        if k in c.attrib:
                            del c.attrib[k]
                so_xanh += 1
            elif mau in MAU_DO:
                r.font.color.rgb = RGBColor(0, 0, 0)
                so_do += 1
    bao_cao.append(f'Đổi màu chữ: {so_xanh} run heading xanh -> đen, {so_do} run chữ đỏ -> đen')

    # 3b. giữ thụt đầu dòng 1cm CHỈ cho đoạn văn xuôi; bìa, tiêu đề, bảng, header/footer thì về 0
    so_bo = 0

    def bo_thut(par):
        nonlocal so_bo
        pf = par.paragraph_format
        # ghi đè cả khi paragraph đang thừa hưởng thụt đầu dòng 1cm từ style Normal
        if pf.first_line_indent != Cm(0):
            pf.first_line_indent = Cm(0)
            so_bo += 1

    for par in doc.paragraphs:
        ten = (par.style.name or '').lower()
        dai = len(par.text.strip())
        can_giua = par.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.CENTER
        if ten.startswith('heading') or ten.startswith('toc') or can_giua or dai < 80:
            bo_thut(par)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for par in cell.paragraphs:
                    bo_thut(par)
    for sec in doc.sections:
        for part in (sec.header, sec.footer, sec.first_page_header, sec.first_page_footer):
            try:
                for par in part.paragraphs:
                    bo_thut(par)
            except Exception:
                continue
    bao_cao.append(f'Bỏ thụt đầu dòng ở bìa/tiêu đề/bảng/header-footer: {so_bo} đoạn (thân bài giữ 1cm)')

    # 4. quét những thứ không tự sửa được
    import re
    cham = []
    for p in doc.paragraphs:
        t = p.text.strip()
        if len(re.findall(r'\.{3,}|…{2,}', t)) and len(t) < 200:
            cham.append(t[:70])
    if cham:
        bao_cao.append(f'CÒN LẠI: {len(cham)} chỗ còn dòng chấm điền tay, ví dụ: ' + ' | '.join(cham[:3]))
    xml = doc.element.body.xml
    if '<w:instrText' not in xml or 'TOC' not in xml:
        bao_cao.append('CÒN LẠI: chưa có Mục lục tự động -> chèn References > Table of Contents, rồi F9 cập nhật')

    # 5. lưu
    if in_place:
        bak = path + '.bak'
        shutil.copy2(path, bak)
        out = path
        bao_cao.append(f'Đã sao lưu bản gốc: {bak}')
    else:
        root, ext = os.path.splitext(path)
        out = root + '-chuan-hoa' + (ext or '.docx')
    doc.save(out)
    return out, bao_cao


def main():
    ap = argparse.ArgumentParser(description='Chuẩn hoá định dạng báo cáo Word')
    ap.add_argument('files', nargs='+')
    ap.add_argument('--in-place', action='store_true', help='ghi đè file gốc (tạo .bak)')
    a = ap.parse_args()
    for f in a.files:
        print(f'\n=== {f} ===')
        try:
            out, bc = xu_ly(f, a.in_place)
            for d in bc:
                print('  -', d)
            print('  => Lưu:', out)
        except Exception as e:
            print('  ✗ Lỗi:', e)


if __name__ == '__main__':
    main()
