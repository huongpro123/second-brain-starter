#!/usr/bin/env python3
"""Tao bo bao cao moi tu mau chuan CTUT (do an / luan van / NCKH).

Vi du:
  python du-an-moi.py --loai do-an --ten "Ten de tai bao cao" \
      --ten-en "English project title" \
      --nganh "Cong nghe Ky thuat Dieu khien va Tu dong hoa" \
      --sv "Nguyen Van A" --mssv "MSSV001" --lop "LOP01" \
      --gvhd "TS. Giang Vien A" --gvhd2 "ThS. Giang Vien B" \
      --out "./out/Bao-cao.docx"

Ket qua: 1 file .docx da dien bia + trang bia-preview.png + CHECK-LIST.md
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

from docx import Document

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]  # .../second-brain
MAU = {
    "do-an": ROOT / "templates/word/do-an/mau-bao-cao-do-an.docx",
    "luan-van": ROOT / "templates/word/luan-van/mau-luan-van-tot-nghiep.docx",
    "nckh": ROOT / "templates/word/nckh/mau-bao-cao-nckh.docx",
}
TEN_LOAI = {"do-an": "do-an", "luan-van": "luan-van", "nckh": "nckh"}
def _find_soffice():
    """Tim duong dan LibreOffice (soffice) tren Windows / macOS / Linux."""
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return Path(found)
    for cand in (
        Path(r"C:\Program Files\LibreOffice\program\soffice.com"),
        Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
        Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.com"),
        Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),
    ):
        if cand.exists():
            return cand
    return None
TOKEN_BIA = {
    "do-an": "[TÊN ĐỀ TÀI ĐỒ ÁN]",
    "luan-van": "[TÊN ĐỀ TÀI LUẬN VĂN]",
    "nckh": "[TÊN ĐỀ TÀI NCKH]",
}


def _co_field(par):
    """Paragraph co chua field (PAGE, TOC...) khong? Neu co thi chi sua tung run."""
    from docx.oxml.ns import qn
    for el in par._p.iter():
        if el.tag in (qn("w:fldChar"), qn("w:instrText"), qn("w:fldSimple")):
            return True
    return False


def thay_trong_doan(par, mapping):
    """Thay text giu format run dau tien. Tra ve True neu co thay doi."""
    cu = par.text
    moi = cu
    for k, v in mapping.items():
        if k in moi:
            moi = moi.replace(k, v)
    if moi == cu:
        return False
    if _co_field(par):
        # giu nguyen field (vi du PAGE o footer): chi sua trong tung run
        for r in par.runs:
            if r.text:
                t2 = r.text
                for k, v in mapping.items():
                    t2 = t2.replace(k, v)
                if t2 != r.text:
                    r.text = t2
        return True
    if par.runs:
        par.runs[0].text = moi
        for r in par.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        par.add_run(moi)
    return True


def duyet_pars(doc):
    """Sinh moi paragraph: than bai, bang (ke ca long nhau), header/footer."""
    def tu_bang(tb):
        for row in tb.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    yield p
                for t in cell.tables:
                    yield from tu_bang(t)

    for p in doc.paragraphs:
        yield p
    for tb in doc.tables:
        yield from tu_bang(tb)
    for s in doc.sections:
        for hf in (s.header, s.footer):
            for p in hf.paragraphs:
                yield p
            for tb in hf.tables:
                yield from tu_bang(tb)


def dien_bia(doc, mapping):
    dem = 0
    for p in duyet_pars(doc):
        if thay_trong_doan(p, mapping):
            dem += 1
    return dem


def _par_bia(doc):
    """Paragraph thuoc phan bia (truoc section break dau tien) + header/footer."""
    from docx.oxml.ns import qn
    ra = []
    for el in doc.element.body.iterchildren():
        if el.tag != qn("w:p"):
            continue
        if el.find(qn("w:pPr")) is not None and el.find(qn("w:pPr")).find(qn("w:sectPr")) is not None:
            break
        yield_par = el
        ra.append(yield_par)
    return ra


def placeholder_con_lai(doc):
    """Chi bao placeholder o BIA va HEADER (than bai la dong goi y, bo qua)."""
    mau = re.compile(r"\[[^\]]{2,40}\]")
    thay = set()
    from docx.text.paragraph import Paragraph
    for el in _par_bia(doc):
        for m in mau.findall(Paragraph(el, doc).text):
            thay.add(m)
    for s in doc.sections:
        for hf in (s.header, s.footer):
            for p in hf.paragraphs:
                for m in mau.findall(p.text):
                    thay.add(m)
    return sorted(thay)


def render_bia(docx_path, out_png):
    """Docx -> PDF -> PNG trang 1 (de nhin bia truoc khi viet noi dung)."""
    soffice = _find_soffice()
    if not soffice:
        print("  ! Khong thay LibreOffice, bo qua render bia.")
        return None
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
    except ImportError:
        print("  ! Chua cai pymupdf, bo qua render bia (pip install pymupdf).")
        return None
    tmp = Path(tempfile.mkdtemp(prefix="bia-"))
    try:
        subprocess.run([str(soffice), "--headless", "--norestore",
                        "--convert-to", "pdf", "--outdir", str(tmp), str(docx_path)],
                       capture_output=True, timeout=180)
        pdf = next(tmp.glob("*.pdf"), None)
        if not pdf:
            return None
        d = fitz.open(str(pdf))
        pix = d[0].get_pixmap(dpi=150)
        pix.save(str(out_png))
        d.close()
        return out_png
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


INFO = {
    "do-an": dict(
        che_do_in="HAI mặt giấy A4", so_trang="tối thiểu 30 trang nội dung chính (không kể phụ lục)",
        bia_cung="bìa cứng XANH DƯƠNG + dán gáy xanh dương, KHÔNG khung bìa",
        so_trang_vi_tri="giữa, phía DƯỚI (footer trái: tên sinh viên in nghiêng; header: tiêu đề phần in nghiêng)",
        chuong="LỜI MỞ ĐẦU (lý do, mục tiêu & phạm vi, ý nghĩa) → CHƯƠNG 1 TỔNG QUAN ĐỀ TÀI → CHƯƠNG 2 CƠ SỞ LÝ THUYẾT → CHƯƠNG 3 THIẾT KẾ VÀ CHẠO SẢN PHẨM (hoặc KẾT QUẢ VÀ THẢO LUẬN) → CHƯƠNG 4 KẾT LUẬN VÀ KIẾN NGHỊ → TLTK → PHỤ LỤC",
    ),
    "luan-van": dict(
        che_do_in="MỘT mặt giấy A4", so_trang="tối thiểu 40 trang nội dung chính (không kể phụ lục)",
        bia_cung="bìa cứng XANH DƯƠNG có khung xanh, 2 bìa (BM 2.1 + BM 2.2) + trang xác nhận (BM 2.3)",
        so_trang_vi_tri="giữa, phía TRÊN (header)",
        chuong="LỜI MỞ ĐẦU → CHƯƠNG 1 TỔNG QUAN LÝ THUYẾT VÀ CƠ SỞ NGHIÊN CỨU → CHƯƠNG 2 PHƯƠNG TIỆN NGHIÊN CỨU - PHƯƠNG PHÁP NGHIÊN CỨU → CHƯƠNG 3 KẾT QUẢ VÀ THẢO LUẬN → CHƯƠNG 4 KẾT LUẬN VÀ ĐỀ XUẤT (KIẾN NGHỊ) → TLTK → PHỤ LỤC",
    ),
    "nckh": dict(
        che_do_in="một mặt giấy A4", so_trang="theo yêu cầu đơn vị quản lý đề tài",
        bia_cung="bìa cứng xanh dương có khung, 2 bìa + trang xác nhận",
        so_trang_vi_tri="giữa, phía TRÊN (header)",
        chuong="LỜI MỞ ĐẦU → CH1 TỔNG QUAN LÝ THUYẾT VÀ CƠ SỞ NGHIÊN CỨU → CH2 PHƯƠNG TIỆN VÀ PHƯƠNG PHÁP NGHIÊN CỨU → CH3 KẾT QUẢ VÀ THẢO LUẬN → CH4 KẾT LUẬN VÀ ĐỀ XUẤT → TLTK → PHỤ LỤC",
    ),
}

CHECKLIST = """# CHECK-LIST báo cáo — {ten}

**Loại:** {loai} · **SV:** {sv} — {mssv} · **Lớp:** {lop}
**GVHD:** {gvhd}{gvhd2}
**File báo cáo:** `{file}` · **Ảnh bìa:** `{bia}`

## 0. Việc đầu tiên: nhìn bìa
- [ ] Mở `{bia}` xem: logo, tên trường/khoa, loại văn bản, ngành, tên đề tài, bảng GVHD/SVTH, "Cần Thơ, năm ..."
- [ ] Không còn dòng chấm điền tay, không còn chữ `[...]`, không còn chữ đỏ/xanh mặc định Word
- [ ] Không có header/footer ở trang bìa

## 1. Bản in — KHÁC NHAU theo loại (QĐ 345/QĐ-ĐHKTCN 08/4/2025)
- [ ] Chế độ in: **{che_do_in}**
- [ ] Bìa: **{bia_cung}**
- [ ] Nội dung chính: **{so_trang}**
- [ ] Số trang: **{so_trang_vi_tri}** (La Mã cho mục mở đầu, Ả Rập từ nội dung chính)
- [ ] Cấu trúc chương: {chuong}

## 2. Trước khi viết
- [ ] Đọc `skills/bao-cao-ctut/SKILL.md` + `wiki/quy-trinh/quy-trinh-bao-cao-ctut.md`
- [ ] Chốt đề cương với GVHD (lý do, mục tiêu, phạm vi, phương pháp, bố cục)

## 3. Trong khi viết
- [ ] Body: Times New Roman 13, **giãn dòng 1,2**, justify, thụt đầu dòng 1 cm, cách đoạn 6 pt (before + after)
- [ ] Lề: **trái 3 · phải 2 · trên 2 · dưới 2 cm**; header/footer 1 cm
- [ ] Heading: chữ đen, TNR, đậm — KHÔNG dùng xanh mặc định của Word
- [ ] Mỗi bảng: tên bảng ở TRÊN (Bảng 4.1...), mỗi hình: tên ở DƯỚI (Hình 3.2...) — cùng cỡ chữ 13
- [ ] Dùng style Heading để mục lục tự cập nhật; cuối cùng Ctrl+A → F9
- [ ] Đánh số hình/bảng theo chương: Bảng 2.1, Hình 2.3

## 4. Trước khi nộp
- [ ] Chạy: `python tools/word/kiem-tra.py "{file}"` → phải ≥ 90, lý tưởng 100
- [ ] Tải lại quy định mới nhất trên trang Khoa nếu đang giữa học kỳ
- [ ] In thử 1 trang bìa + 1 trang thân để kiểm tra lề + chế độ in
- [ ] Tên file: `HoTen_MSSV_BaoCaoDoAn2.pdf` (theo yêu cầu GVHD)

## 5. Nguồn chuẩn
- QĐ **345/QĐ-ĐHKTCN ngày 08/4/2025** (Hiệu trưởng) — quy định ĐATN/KLTN/TTTN + hướng dẫn trình bày
- Hướng dẫn, định dạng báo cáo ĐỒ ÁN (ĐA1/2/3) — in 2 mặt, bìa xanh dương
- Chi tiết: `wiki/quy-trinh/quy-trinh-bao-cao-ctut.md`
"""


def main():
    ap = argparse.ArgumentParser(description="Tao bao cao moi tu mau chuan CTUT")
    ap.add_argument("--loai", required=True, choices=list(MAU), help="do-an | luan-van | nckh")
    ap.add_argument("--ten", required=True, help="ten de tai")
    ap.add_argument("--ten-en", default="", help="ten de tai tieng Anh (khong bat buoc)")
    ap.add_argument("--nganh", default="", help="ten nganh dao tao")
    ap.add_argument("--sv", default="", help="ho ten sinh vien")
    ap.add_argument("--mssv", default="")
    ap.add_argument("--lop", default="")
    ap.add_argument("--gvhd", default="")
    ap.add_argument("--gvhd2", default="")
    ap.add_argument("--khoa", default="", help="khoa dao tao, vd '2023 – 2027' (luan van)")
    ap.add_argument("--ma-so", default="", help="ma so de tai (nckh)")
    ap.add_argument("--nam", type=int, default=date.today().year)
    ap.add_argument("--thang", type=int, default=date.today().month)
    ap.add_argument("--out", required=True, help="thu muc xuat")
    ap.add_argument("--mo", action="store_true", help="mo file bang Word sau khi tao")
    a = ap.parse_args()

    if not MAU[a.loai].exists():
        sys.exit(f"Khong thay mau: {MAU[a.loai]}")

    out = Path(a.out)
    if out.suffix.lower() == '.docx':
        out.parent.mkdir(parents=True, exist_ok=True)
        dich = out
        out = out.parent
    else:
        out.mkdir(parents=True, exist_ok=True)
        dich = None
    ten_file = {"do-an": "Bao-cao-do-an.docx", "luan-van": "Luan-van-tot-nghiep.docx",
                "nckh": "Bao-cao-tong-ket-NCKH.docx"}[a.loai]
    if dich is None:
        dich = out / ten_file

    mapping = {
        TOKEN_BIA[a.loai]: a.ten,
        "(Tên đề tài bằng tiếng Anh – nếu có)": a.ten_en,
        "[Học vị, họ tên GVHD]": a.gvhd,
        "[Học vị, họ tên GVHD 2]": a.gvhd2,
        "[Họ tên SV – MSSV]": (f"{a.sv} – {a.mssv}" if a.sv or a.mssv else ""),
        "[Lớp]": a.lop,
        "[MSSV]": a.mssv,
        "[TÊN ĐỀ TÀI]": a.ten,
        "[Họ và tên sinh viên]": a.sv,
        "Cần Thơ, tháng 11 năm 2026": f"Cần Thơ, tháng {a.thang:02d} năm {a.nam}",
        "Cần Thơ, năm 2026": f"Cần Thơ, năm {a.nam}",
    }
    if a.loai in ("do-an", "luan-van"):
        mapping["Ngành: [Tên ngành đào tạo]"] = f"Ngành: {a.nganh}"
    if a.loai == "luan-van":
        mapping["Khóa: [20xx – 20xx]"] = f"Khóa: {a.khoa}"
    if a.loai == "nckh":
        mapping["Mã số: […………]"] = f"Mã số: {a.ma_so}"

    doc = Document(str(MAU[a.loai]))
    dem = dien_bia(doc, mapping)
    doc.save(str(dich))

    con_lai = placeholder_con_lai(doc)
    print(f"\nĐã tạo: {dich}")
    print(f"  Đã điền {dem} đoạn (bìa + header).")
    if con_lai:
        print("  ! Placeholder còn lại (điền tay hoặc thêm tham số):")
        for x in con_lai:
            print(f"    - {x}")

    bia = out / "bia-preview.png"
    ok = render_bia(dich, bia)
    if ok:
        print(f"  Ảnh bìa: {bia}  ← MỞ XEM NGAY trước khi viết nội dung")
    else:
        bia = Path("(chưa render được)")

    checklist = out / "CHECK-LIST.md"
    checklist.write_text(CHECKLIST.format(
        ten=a.ten, loai=a.loai, sv=a.sv, mssv=a.mssv, lop=a.lop,
        gvhd=a.gvhd, gvhd2=(f" · {a.gvhd2}" if a.gvhd2 else ""),
        file=ten_file, bia=bia.name, **INFO[a.loai]), encoding="utf-8")
    print(f"  Check-list: {checklist}")
    print(f"\nBước tiếp: mở file, viết nội dung theo CHECK-LIST, cuối cùng chạy:")
    print(f"  python tools/word/kiem-tra.py \"{dich}\"")

    if a.mo and os.name == "nt":
        try:
            os.startfile(str(dich))  # type: ignore[attr-defined]
        except Exception as e:
            print("  ! Không mở được file:", e)


if __name__ == "__main__":
    main()
