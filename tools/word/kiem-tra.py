# -*- coding: utf-8 -*-
"""Chấm điểm định dạng một file Word (.docx) theo chuẩn báo cáo CTUT.

Cách dùng:
    python kiem-tra.py "D:\\duong\\dan\\bao-cao.docx"
    python kiem-tra.py file1.docx file2.docx --json

Thang điểm 100. Dưới 80 điểm = chưa nên in.
Cần: pip install python-docx
"""
import sys, re, json, argparse, zipfile
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

A4 = (21.0, 29.7)
BODY_FONT = 'Times New Roman'
BODY_SIZE = 13.0
CHUAN_LE = dict(top=(1.6, 3.3), bottom=(1.6, 3.3), left=(2.5, 3.7), right=(1.2, 2.6))
TU_KHOA_BIA = ('TRƯỜNG ĐẠI HỌC', 'KHOA ', 'GIẢNG VIÊN HƯỚNG DẪN', 'SINH VIÊN THỰC HIỆN', 'CÁN BỘ HƯỚNG DẪN')
MAU_XANH_WORD = {'365F91', '4F81BD', '4472C4', '5B9BD5', '2E74B5'}
MAU_NAVY_OK = {'1F3864', '1F4E79', '2F5597', '0F243E', '000000'}
MAU_DO = {'FF0000', 'C00000', 'E74C3C', 'CC0000'}


def font_name(style_or_run):
    try:
        f = style_or_run.font.name
        if f:
            return f
    except Exception:
        pass
    el = getattr(style_or_run, 'element', None)
    if el is None:
        el = getattr(style_or_run, '_element', None)
    if el is not None:
        rPr = el.find(qn('w:rPr'))
        if rPr is not None:
            rf = rPr.find(qn('w:rFonts'))
            if rf is not None:
                for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
                    v = rf.get(qn(attr))
                    if v:
                        return v
        rf = el.find(qn('w:rFonts'))
        if rf is not None:
            for attr in ('w:ascii', 'w:hAnsi'):
                v = rf.get(qn(attr))
                if v:
                    return v
    return None


def font_size(style_or_run):
    try:
        if style_or_run.font.size:
            return style_or_run.font.size.pt
    except Exception:
        pass
    el = getattr(style_or_run, 'element', None)
    if el is None:
        el = getattr(style_or_run, '_element', None)
    if el is not None:
        rPr = el.find(qn('w:rPr'))
        if rPr is not None:
            sz = rPr.find(qn('w:sz'))
            if sz is not None:
                try:
                    return float(sz.get(qn('w:val'))) / 2
                except Exception:
                    return None
    return None


def run_color(run):
    try:
        if run.font.color and run.font.color.rgb:
            return str(run.font.color.rgb).upper()
    except Exception:
        pass
    return None


def _rfonts_val(el):
    rPr = el.find(qn('w:rPr')) if el is not None else None
    if rPr is None:
        return None
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        return None
    v = rf.get(qn('w:ascii')) or rf.get(qn('w:hAnsi'))
    if v:
        return ('font', v)
    th = rf.get(qn('w:asciiTheme')) or rf.get(qn('w:hAnsiTheme'))
    if th:
        return ('theme', th)
    return None


def theme_fonts(path):
    """Doc theme1.xml: font latin cua majorFont / minorFont."""
    d = {'major': None, 'minor': None}
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/theme/theme1.xml').decode('utf-8', 'ignore')
    except Exception:
        return d
    for key, tag in (('major', 'majorFont'), ('minor', 'minorFont')):
        m = re.search(r'<a:%s>(.*?)</a:%s>' % (tag, tag), xml, re.S)
        if m:
            lm = re.search(r'<a:latin[^>]*typeface="([^"]*)"', m.group(1))
            d[key] = lm.group(1) if lm else None
    return d


def _theme_pick(theme, name):
    return theme.get('major') if 'major' in (name or '').lower() else theme.get('minor')


def _docdefaults_font(doc, theme):
    try:
        dd = doc.styles.element.find(qn('w:docDefaults'))
        rp = dd.find(qn('w:rPrDefault')) if dd is not None else None
        rPr = rp.find(qn('w:rPr')) if rp is not None else None
        rf = rPr.find(qn('w:rFonts')) if rPr is not None else None
        if rf is None:
            return None
        v = rf.get(qn('w:ascii')) or rf.get(qn('w:hAnsi'))
        if v:
            return v
        th = rf.get(qn('w:asciiTheme')) or rf.get(qn('w:hAnsiTheme'))
        if th:
            return _theme_pick(theme, th)
    except Exception:
        pass
    return None


def eff_font(doc, style_or_name, theme):
    """Font hieu dung: style -> basedOn -> docDefaults/theme."""
    try:
        st = doc.styles[style_or_name] if isinstance(style_or_name, str) else style_or_name
    except Exception:
        st = None
    for _ in range(8):
        if st is None:
            break
        el = getattr(st, 'element', None)
        rv = _rfonts_val(el) if el is not None else None
        if rv:
            kind, val = rv
            return val if kind == 'font' else (_theme_pick(theme, val) or val + ' (theme)')
        try:
            st = st.base_style
        except Exception:
            st = None
    return _docdefaults_font(doc, theme)

def iter_pars(doc):
    """Mọi paragraph trong body, bảng, header/footer."""
    def walk(container):
        for p in container.paragraphs:
            yield p
        for t in container.tables:
            for row in t.rows:
                for cell in row.cells:
                    yield from walk(cell)
    yield from walk(doc)
    for sec in doc.sections:
        for part in (sec.header, sec.footer, sec.first_page_header, sec.first_page_footer):
            try:
                yield from walk(part)
            except Exception:
                continue


def has_field(doc, instr_prefix):
    xmls = [doc.element.body.xml]
    for sec in doc.sections:
        for part in (sec.header, sec.footer, sec.first_page_header, sec.first_page_footer):
            try:
                xmls.append(part._element.xml)
            except Exception:
                continue
    pat = re.compile(r'<w:instrText[^>]*>[^<]*' + re.escape(instr_prefix))
    return any(pat.search(x) for x in xmls)


def dem_cham(text):
    t = re.sub(r'\[[^\]]*\]', ' ', text)  # bo placeholder [...], vd: Ma so: [...]
    return len(re.findall(r'[.…]{6,}', t))


def check(path):
    doc = Document(path)
    theme = theme_fonts(path)
    res = []  # (mức, điểm_trừ, tiêu chí, chi tiết)
    def add(muc, tru, tieu_chi, chi_tiet):
        res.append(dict(muc=muc, tru=tru, tieu_chi=tieu_chi, chi_tiet=chi_tiet))

    # 1. cỡ giấy
    s0 = doc.sections[0]
    w, h = s0.page_width.cm, s0.page_height.cm
    if abs(w - A4[0]) < 0.3 and abs(h - A4[1]) < 0.3:
        pass
    elif abs(w - A4[1]) < 0.3 and abs(h - A4[0]) < 0.3:
        add('WARN', 5, 'Khổ giấy', f'A4 nằm ngang ({w:.1f}×{h:.1f}cm) – thường chỉ dùng cho phụ lục')
    elif abs(w - 21.59) < 0.3:
        add('FAIL', 10, 'Khổ giấy', f'Letter {w:.1f}×{h:.1f}cm – phải là A4 21×29,7cm')
    else:
        add('FAIL', 10, 'Khổ giấy', f'{w:.1f}×{h:.1f}cm – phải là A4 21×29,7cm')

    # 2. lề — bìa có lề riêng nên chỉ chấm các section nội dung
    sec_kiem = doc.sections[1:] if len(doc.sections) > 1 else doc.sections
    sb = sec_kiem[-1]
    le = dict(top=sb.top_margin.cm, bottom=sb.bottom_margin.cm,
              left=sb.left_margin.cm, right=sb.right_margin.cm)
    ten = dict(top='trên', bottom='dưới', left='trái', right='phải')
    for k, v in le.items():
        lo, hi = CHUAN_LE[k]
        if not (lo <= v <= hi):
            add('WARN', 3, 'Lề', f'lề {ten[k]} {v:.2f}cm (chuẩn {lo}–{hi}cm)')
    so_section = len(doc.sections)

    # 3. Normal
    try:
        normal = doc.styles['Normal']
        f = eff_font(doc, 'Normal', theme) or ''
        if BODY_FONT.lower() not in f.lower() and 'time' not in f.lower():
            add('FAIL', 10, 'Font thân bài', f'font hiệu dụng "{f or "(không xác định)"}" – phải Times New Roman')
        sz = font_size(normal)
        if sz and abs(sz - BODY_SIZE) > 0.6:
            add('WARN', 5, 'Cỡ chữ thân bài', f'{sz:g}pt – chuẩn 13pt')
        pf = normal.paragraph_format
        ls = pf.line_spacing
        if ls is not None and not (1.15 <= float(ls) <= 1.6):
            add('WARN', 8, 'Giãn dòng', f'{float(ls):g} – chuẩn 1,2 hoặc 1,5')
        ds_doan = [p for p in doc.paragraphs if p.text.strip() and len(p.text.strip()) > 80]
        if ds_doan:
            chuan = sum(1 for p in ds_doan if p.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
                        or (p.paragraph_format.alignment is None and pf.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY))
            ty_le = chuan / len(ds_doan)
            if ty_le < 0.7:
                add('WARN', 5, 'Căn lề đoạn',
                    f'chỉ {ty_le*100:.0f}% đoạn văn dài được căn đều hai bên (nên ~100%)')
    except Exception as e:
        add('WARN', 5, 'Style Normal', f'không đọc được ({e})')

    # 4. heading
    for lvl, lo, hi in ((1, 13.5, 16.5), (2, 12.5, 14.5), (3, 11.5, 13.5)):
        try:
            st = doc.styles[f'Heading {lvl}']
        except Exception:
            continue
        f = eff_font(doc, st, theme) or ''
        if f and BODY_FONT.lower() not in f.lower() and 'time' not in f.lower():
            add('FAIL', 6, f'Heading {lvl}', f'font hieu dung "{f}" - phai Times New Roman')
        sz = font_size(st) or font_size(doc.styles['Normal'])
        if sz and not (lo <= sz <= hi):
            add('WARN', 3, f'Heading {lvl}', f'{sz:g}pt - chuan {lo:g}-{hi:g}pt')
        try:
            el = st.element
            rPr = el.find(qn('w:rPr'))
            col = rPr.find(qn('w:color')) if rPr is not None else None
            if col is not None:
                mc = (col.get(qn('w:val')) or '').upper()
                if mc in MAU_XANH_WORD:
                    add('FAIL', 5, f'Heading {lvl}', f'mau xanh Word ({mc}) - nen den')
                elif (not mc) and col.get(qn('w:themeColor')):
                    add('WARN', 3, f'Heading {lvl}', 'mau lay theo theme Word - nen dat den')
        except Exception:
            pass

    # 5. mục lục
    if not has_field(doc, 'TOC'):
        add('WARN', 8, 'Mục lục', 'không có trường TOC – thiếu mục lục tự động')

    # 6. số trang
    if not has_field(doc, ' PAGE'):
        add('FAIL', 10, 'Số trang', 'footer không có trường PAGE')

    # 7. placeholder dòng chấm + 8. chữ đỏ + 9. ảnh lớn
    cham = []
    do = []
    for p in iter_pars(doc):
        t = p.text.strip()
        if dem_cham(t) and not re.search(r'\b(20\d\d)\b', t):
            if len(t) < 160:
                cham.append(t[:60])
        for r in p.runs:
            c = run_color(r)
            if c in MAU_DO and r.text.strip():
                do.append(f'"{r.text.strip()[:30]}" ({c})')
    cham_bia = [c for c in cham if any(k.lower() in c.lower() for k in TU_KHOA_BIA)]
    cham_form = [c for c in cham if c not in cham_bia]
    if cham_bia:
        add('FAIL', 8, 'Dòng chấm điền tay (bìa/form)', f'{len(cham_bia)} chỗ còn dấu chấm, ví dụ: ' + ' | '.join(cham_bia[:3]))
    elif cham_form:
        add('WARN', 3, 'Dòng chấm điền tay', f'{len(cham_form)} chỗ, ví dụ: ' + ' | '.join(cham_form[:2]))
    if do:
        add('WARN', 4, 'Chữ đỏ', f'{len(do)} đoạn: ' + ' | '.join(do[:3]))
    to_anh = []
    for dr in doc.element.body.iter(qn('w:drawing')):
        ext = dr.find('.//' + qn('wp:extent'))
        if ext is None:
            continue
        try:
            cx = int(ext.get('cx')) / 360000
            cy = int(ext.get('cy')) / 360000
        except Exception:
            continue
        anc = dr.find(qn('wp:anchor'))
        # anh nen trang (khung bia): floating behindDoc hoac cao ~ ca trang -> bo qua
        if anc is not None and anc.get('behindDoc') == '1':
            continue
        if cy > 20.0:
            continue
        if cx > 16.0:
            to_anh.append(round(cx, 1))
    if to_anh:
        add('WARN', 3, 'Ảnh tràn lề', f'{len(to_anh)} ảnh rộng >16cm: {to_anh[:4]}')

    # tổng điểm
    diem = 100 - sum(r['tru'] for r in res)
    diem = max(0, min(100, diem))
    return dict(file=str(path), diem=diem, muc_loi=[r for r in res if r['muc'] == 'FAIL'],
                canh_bao=[r for r in res if r['muc'] == 'WARN'],
                so_trang=None, thong_tin=dict(page=f'{s0.page_width.cm:.1f}×{s0.page_height.cm:.1f}cm',
                                              le={k: round(v, 2) for k, v in le.items()}))


def in_ket_qua(kq):
    print(f"\n=== {kq['file']} ===")
    print(f"Khổ giấy {kq['thong_tin']['page']} | lề {kq['thong_tin']['le']}")
    for r in kq['muc_loi']:
        print(f"  ✗ [{r['tieu_chi']}] {r['chi_tiet']}")
    for r in kq['canh_bao']:
        print(f"  ! [{r['tieu_chi']}] {r['chi_tiet']}")
    if not kq['muc_loi'] and not kq['canh_bao']:
        print('  ✓ Không thấy lỗi định dạng nào.')
    print(f"  ĐIỂM: {kq['diem']}/100 " + ('— nên sửa trước khi in' if kq['diem'] < 80 else '— in được'))


def main():
    ap = argparse.ArgumentParser(description='Chấm điểm định dạng báo cáo Word')
    ap.add_argument('files', nargs='+')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    out = []
    for f in a.files:
        try:
            kq = check(f)
            out.append(kq)
            if not a.json:
                in_ket_qua(kq)
        except Exception as e:
            print(f'\n=== {f} ===\n  ✗ Không đọc được: {e}')
            out.append(dict(file=f, error=str(e)))
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
