#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Soat NOI DUNG bao cao: bat placeholder, so lieu khong dan chung, van thoi phong,
trich dan lech, va in bang so sanh so lieu giua TOM TAT / KET LUAN.

Chay: python tools/word/kiem-tra-noi-dung.py file.docx [--json]
Muc dich: chong ao giac — khong thay the viec doc lai bang mat.
"""
import argparse
import json
import re
import sys

from docx import Document

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


PLACEHOLDER = re.compile(r"\[(?:CẦN|CHUA|CHƯA|\?)[^\]]*\]|\bTODO\b|\?\?\?")
BOMBAST = ["tuyệt vời", "rất tốt", "cực kỳ", "xuất sắc", "đẹp mắt",
           "vượt trội", "ổn định tuyệt đối", "không thể tốt hơn"]
FIRSTPERSON = ["em thấy", "em nghĩ", "chúng em", "chúng ta", "mình đã", "tôi đã",
               "theo em", "theo mình"]
SO_LIEU = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|°C|mm|cm|m|kg|g|V|A|mA|Hz|kHz|MHz|s|ms|us|µs|W|kW|Wh|kWh|dB|ppm|bar|kPa|MPa|rpm|vòng/phút|lít|l/ph)", re.I)
DAN_CHUNG = re.compile(r"\[\d+\]")
REF_HINH_BANG = re.compile(r"(Bảng|Hình|Sơ đồ|Biểu đồ)\s*\d", re.I)
CLAIM = re.compile(r"(đạt|sai số|giảm|tăng|hiệu suất|độ chính xác|độ ổn định|so với|trung bình|tỉ lệ|tỷ lệ|phần trăm|chứng minh)", re.I)
NGAY_THANG = re.compile(r"ngày\s*\d{1,2}\s*tháng|tháng\s*\d{1,2}\s*năm", re.I)


def doan_cua(doc):
    """Sinh (chi_so, style, text) cho doan van + o bang, theo thu tu tai lieu."""
    i = 0
    for p in doc.paragraphs:
        yield i, p.style.name, p.text.strip()
        i += 1
    for tb in doc.tables:
        for row in tb.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    yield i, "Table", p.text.strip()
                    i += 1


def tach_so(text):
    return set(re.findall(r"\d+(?:[.,]\d+)?", text))


def kiem(texts):
    findings = []
    so_dan_chung = []
    so_lieu_ph = []
    muc = ""
    so_theo_muc = {}
    tltk_idx = 0
    trong_tltk = False

    for idx, style, t in texts:
        if not t:
            continue
        # xac dinh muc dang doc
        if style.startswith("Heading"):
            muc = t.upper()[:40]
            if "TÀI LIỆU THAM KHẢO" in muc:
                trong_tltk = True
        if re.match(r"^(TÓM TẮT|KẾT LUẬN|CHƯƠNG \d|LỜI MỞ ĐẦU|MỞ ĐẦU)", muc):
            so_theo_muc.setdefault(muc, set()).update(tach_so(t))

        # 1. placeholder con sot
        for m in PLACEHOLDER.finditer(t):
            findings.append(("FAIL", "PLACEHOLDER", f"#đoạn {idx}: còn '{m.group(0)}' — không được có trong bản nộp: {t[:90]}"))

        # 2. van thoi phong
        low = t.lower()
        for w in BOMBAST:
            if w in low:
                findings.append(("WARN", "THOI_PHONG", f"#đoạn {idx}: '{w}' — thay bằng số liệu/so sánh: {t[:90]}"))

        # 3. ngoi thu nhat
        for w in FIRSTPERSON:
            if w in low:
                findings.append(("WARN", "VAN_PHONG", f"#đoạn {idx}: '{w}' — văn phong học thuật nên khách quan: {t[:90]}"))
                break

        # 4. so lieu dang % nhung khong dan chung (thong so ky thuat 1 kg / 5 V khong tinh)
        if ("%" in t) and CLAIM.search(t) and not DAN_CHUNG.search(t) \
                and not REF_HINH_BANG.search(t) and not NGAY_THANG.search(t) and len(t) > 60:
            so_lieu_ph.append(("WARN", "SO_LIEU_KHONG_DAN",
                               f"#đoạn {idx}: số liệu nhưng không có [n]/Bảng/Hình: {t[:100]}"))

        # 5. dem trich dan + TLTK
        so_dan_chung += [int(x) for x in re.findall(r"\[(\d+)\]", t)]
        if trong_tltk:
            if re.match(r"^\s*\[\d+\]|^\s*\d+\.\s", t):
                tltk_idx += 1

    for f in so_lieu_ph[:6]:
        findings.append(f)
    if len(so_lieu_ph) > 6:
        findings.append(("INFO", "SO_LIEU_KHONG_DAN", f"còn {len(so_lieu_ph) - 6} chỗ nữa — chạy --json để xem hết"))

    # 6. trich dan lech danh muc
    if so_dan_chung:
        mx = max(so_dan_chung)
        if tltk_idx and mx > tltk_idx:
            findings.append(("FAIL", "TLTK_LECH", f"trích dẫn tới [{mx}] nhưng danh mục TLTK chỉ có {tltk_idx} mục"))
        elif not tltk_idx:
            findings.append(("WARN", "TLTK_THIEU", f"có {len(so_dan_chung)} trích dẫn nhưng chưa thấy danh mục TLTK đánh số"))

    # 7. so sanh so lieu giua cac muc
    def chi_pct(ks):
        return {x for x in ks if "%" in x or "," in x}

    tom_tat = next((v for k, v in so_theo_muc.items() if "TÓM TẮT" in k), None)
    ket_luan = next((v for k, v in so_theo_muc.items() if "KẾT LUẬN" in k), None)
    if tom_tat is not None and ket_luan is not None:
        tom_tat = {x for x in tom_tat if x.split(" ")[0].replace(",", ".").replace(".", "").isdigit() and "." in x.replace(",", ".")}
        ket_luan = {x for x in ket_luan if x.split(" ")[0].replace(",", ".").replace(".", "").isdigit() and "." in x.replace(",", ".")}
    if tom_tat and ket_luan:
        chi_tom_tat = {x for x in tom_tat if x not in ket_luan}
        chi_ket_luan = {x for x in ket_luan if x not in tom_tat}
        if chi_tom_tat or chi_ket_luan:
            findings.append(("INFO", "SO_LIEU_LECH",
                             f"số có ở TÓM TẮT nhưng không ở KẾT LUẬN: {sorted(chi_tom_tat)[:8]} · ngược lại: {sorted(chi_ket_luan)[:8]}"))
    return findings, so_theo_muc


def kiem_tieu_muc_mong(doc):
    """Tieu muc (Heading 2/3) phai co it nhat 2 doan van truoc heading ke tiep.

    Quy uoc (SV04 + van khoa hoc): khong tach heading cho mot doan van le loi.
    """
    findings = []
    paras = doc.paragraphs
    n = len(paras)
    for i, p in enumerate(paras):
        style = p.style.name or ""
        if not style.startswith("Heading"):
            continue
        try:
            level = int(style.split()[-1])
        except Exception:
            continue
        if level < 2 or not p.text.strip():
            continue
        dem = 0
        cap_duoi = False
        for j in range(i + 1, n):
            q = paras[j]
            qs = q.style.name or ""
            if qs.startswith("Heading"):
                try:
                    qlv = int(qs.split()[-1])
                except Exception:
                    qlv = 0
                cap_duoi = qlv > level
                break
            if q.text.strip():
                dem += 1
        if cap_duoi:
            continue  # muc cha chua tieu muc con — khong can doan rieng
        if dem < 2:
            lvl = "WARN" if level >= 3 else "INFO"
            findings.append((lvl, "TIEU_MUC_MONG",
                            f"#đoạn {i}: '{p.text.strip()[:60]}' chỉ có {dem} đoạn văn "
                            f"— quy ước: tiểu mục (cấp 3 trở xuống) phải có từ 2 đoạn văn"))
    if len(findings) > 6:
        du = len(findings) - 6
        findings = findings[:6] + [("INFO", "TIEU_MUC_MONG", f"còn {du} tiểu mục mỏng nữa — chạy --json để xem hết")]
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    doc = Document(a.file)
    findings, so_theo_muc = kiem(list(doan_cua(doc)))
    findings += kiem_tieu_muc_mong(doc)
    n_fail = sum(1 for f in findings if f[0] == "FAIL")
    n_warn = sum(1 for f in findings if f[0] == "WARN")
    diem = max(0, 100 - 8 * n_fail - 3 * n_warn)
    words = sum(len(t.split()) for _, _, t in doan_cua(doc))
    hinh = len(doc.inline_shapes)
    bang = len(doc.tables)
    if words > 1500 and bang == 0 and hinh == 0:
        findings.append(("WARN", "THIEU_BANG_HINH", f"{words} từ nhưng không có bảng/hình nào — báo cáo kỹ thuật thường cần"))
        diem = max(0, diem - 3)
        n_warn += 1
    ket = "OK — nộp được" if diem >= 90 else ("CẦN RÀ LẠI" if diem >= 75 else "CHƯA NỘP ĐƯỢC")
    if a.json:
        print(json.dumps({"file": a.file, "diem": diem, "fail": n_fail, "warn": n_warn,
                          "words": words, "tables": bang, "images": hinh,
                          "findings": findings, "so_lieu_theo_muc": {k: sorted(v) for k, v in so_theo_muc.items()}},
                         ensure_ascii=False, indent=2))
        return 0 if diem >= 90 else 1
    print(f"=== {a.file}")
    print(f"    {words} từ · {bang} bảng · {hinh} hình · {len(so_theo_muc)} mục có số liệu")
    if not findings:
        print("    Không thấy dấu hiệu ảo giác nào.")
    for lvl, code, msg in findings:
        print(f"  {'✗' if lvl == 'FAIL' else ('!' if lvl == 'WARN' else '·')} [{code}] {msg}")
    print(f"\nĐIỂM NỘI DUNG: {diem}/100 — {ket}")
    return 0 if diem >= 90 else 1


if __name__ == "__main__":
    sys.exit(main())
