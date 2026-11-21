---
title: Kỹ năng viết Word — lỗi thường gặp và cách chuẩn hóa
updated: 2026-11-21
status: active
tags: [word, bao-cao, chuan, do-an, nckh, luan-van]
sources:
  - "QĐ 345/QĐ-ĐHKTCN ngày 08/4/2025 — Quy định trình bày ĐATN/KLTN/TTTN (CTUT)"
  - "QĐ 886/QĐ-ĐHKTCN (2022) — Quy chế hoạt động NCKH sinh viên CTUT (SV04)"
  - "QĐ 263/QĐ-TKT ngày 06/8/2024 — Trường Kinh tế, ĐH Cần Thơ (đối chiếu tham khảo)"
---

# Kỹ năng viết Word — lỗi thường gặp và cách chuẩn hóa

> [!abstract] Nguyên tắc cốt lõi
> Không có "một form chung cho mọi loại báo cáo" — Đồ án, ĐATN/KLTN, TTTN và NCKH SV04 dùng **4 bộ quy chuẩn khác nhau**. Chọn đúng template ngay từ đầu sẽ tránh cảnh sửa format lặp đi lặp lại.

> [!warning] Đối chiếu chuẩn hiện hành CTUT
> Chuẩn định dạng hiện hành theo **QĐ 345/QĐ-ĐHKTCN ngày 08/4/2025** và **QĐ 886/2022 (SV04)**: xem chi tiết ở **[[quy-trinh-bao-cao-ctut]]** và **[[nckh-quy-che-sv04]]**.

## 1. Phân biệt các bộ mẫu có sẵn trong kit

| Loại | Chuẩn áp dụng | Mẫu dùng trong repo | Bìa cứng |
|---|---|---|---|
| Đồ án / Đồ án 2 | QĐ 345 + HD Đồ án (CTUT) | `templates/word/do-an/mau-bao-cao-do-an.docx` | xanh dương, không khung, in 2 mặt |
| ĐATN / Khóa luận tốt nghiệp | QĐ 345/2025 (CTUT) | `templates/word/luan-van/mau-luan-van-tot-nghiep.docx` | xanh dương, có khung, in 1 mặt |
| NCKH SV — báo cáo tổng kết (SV04) | QĐ 886/2022 mẫu SV04 | `templates/word/nckh/mau-bao-cao-tong-ket-sv04.docx` | xanh dương, khung PNG, in 1 mặt |
| NCKH SV — mẫu cũ (tham khảo) | Form đồ án cũ | `templates/word/nckh/mau-bao-cao-nckh.docx` | — |
| NCKH SV — đề cương | Mẫu đề cương tham khảo | `templates/word/nckh/mau-de-cuong-nckh.docx` | bìa trắng |

*(Lưu ý: Một số văn bản của trường khác như QĐ 263/QĐ-TKT của Trường Kinh tế – ĐH Cần Thơ có bộ lề/giãn dòng khác. Tuyệt đối không trộn thông số giữa hai trường trong cùng một quyển.)*

## 2. Sáu lỗi format phá hỏng báo cáo phổ biến nhất

Qua kiểm tra các báo cáo sinh viên bằng `tools/word/kiem-tra.py`, có 6 lỗi lặp đi lặp lại nhiều nhất:

1. **Heading lấy màu/font mặc định của Word** (`#365F91`, `#4F81BD`, Calibri/Cambria) trong khi thân bài dùng Times New Roman → quyển báo cáo bị lệch tông màu và font.
2. **Trộn nhiều chuẩn lề & giãn dòng:** lúc dùng lề `2/2/3/2`, lúc `2,5/2,5/3/2`, lúc `3/3/3,5/2`; giãn dòng nhảy giữa `1,2` / `1,3` / `1,5`.
3. **Bìa chưa hoàn thiện:** còn dòng chấm điền tay `………`, nhãn thừa `"TÊN ĐỀ TÀI:"`, tên đề tài cỡ chữ quá nhỏ (≤ 17 pt), hoặc chèn ảnh sản phẩm lên bìa chính.
4. **Sai khổ giấy (Letter 21,6 × 27,9 cm thay vì A4 21,0 × 29,7 cm)** — mang ra tiệm in sẽ lệch toàn bộ trang.
5. **Thiếu mục lục tự động (field TOC):** gõ tay từng dòng chấm dẫn tới lệch số trang khi thêm/bớt đoạn.
6. **Số trang gõ tay hoặc thiếu section break:** đánh số cả lên trang bìa hoặc lẫn lộn số La Mã với Ả Rập.

**Bài học quan trọng:** *Bìa đẹp không kéo điểm format lên được nếu thân bài sai chuẩn.* Cả bìa lẫn thân bài đều nên chấm kiểm tra đạt ≥ 90/100.

## 3. Trang bìa — thứ tự chuẩn và 5 lỗi cần tránh

Thứ tự dòng trên bìa (tham khảo mẫu `assets/word/mau-bia-chinh.png` & `mau-bia-phu.png`):

1. TRƯỜNG ĐẠI HỌC KỸ THUẬT – CÔNG NGHỆ CẦN THƠ
2. KHOA …
3. Logo / đường kẻ ngang
4. ĐỒ ÁN … / ĐỒ ÁN TỐT NGHIỆP / BÁO CÁO TỔNG KẾT
5. Ngành: … (và Khóa nếu có)
6. **TÊN ĐỀ TÀI (16–22 pt đậm)** — dòng nổi bật nhất trang
7. Tên đề tài tiếng Anh (nếu có)
8. Bảng 2 cột không viền: CÁN BỘ HƯỚNG DẪN | SINH VIÊN THỰC HIỆN
9. Cần Thơ, tháng … năm … (đáy trang)

Năm lỗi hay gặp: (a) để chữ `"TÊN ĐỀ TÀI:"` làm nhãn; (b) sót dòng chấm `………`; (c) cỡ chữ tiêu đề quá nhỏ; (d) chèn hình minh họa lên trang bìa; (e) dòng ngày/tháng đặt sai cỡ hoặc dùng màu chữ đỏ/xanh mặc định.

## 4. Checklist nhanh trước khi in

- [ ] Dùng đúng mẫu theo loại (Đồ án / ĐATN-KLTN / NCKH SV04)
- [ ] `python tools/word/kiem-tra.py <file.docx>` đạt ≥ 90/100, không còn lỗi `FAIL`
- [ ] `python tools/word/kiem-tra-noi-dung.py <file.docx>` đạt ≥ 90/100, không còn placeholder `[CẦN ...]`
- [ ] Khổ giấy A4 (không phải Letter); lề chuẩn Trái 3 / Phải 2 / Trên 2 / Dưới 2 cm
- [ ] Toàn bộ Times New Roman, chữ đen (riêng tên đề tài bìa ĐATN màu xanh navy/xanh dương theo QĐ 345)
- [ ] Bìa không có số trang, không có header/footer; mở đầu đánh La Mã (`i, ii...`); thân bài đánh Ả Rập (`1, 2...`)
- [ ] Tên bảng **trên** bảng, tên hình **dưới** hình, đánh số theo chương
- [ ] Xuất PDF cuối cùng qua Microsoft Word (`word-hoan-tat.py` hoặc `Ctrl+A → F9` rồi Save As PDF) và mở kiểm lại trang

## 5. Công cụ trong repo

| Việc cần làm | Lệnh |
|---|---|
| Tạo báo cáo mới + bìa + checklist | `python tools/word/du-an-moi.py ...` |
| Dựng lại bìa Mẫu 1 NCKH (SV04) | `python tools/word/bia-sv04.py ...` |
| Chấm điểm định dạng (thang 100) | `python tools/word/kiem-tra.py file.docx` |
| Soát nội dung & chống ảo giác | `python tools/word/kiem-tra-noi-dung.py file.docx` |
| Chuẩn hóa style file Word cũ | `python tools/word/chuan-hoa.py file.docx` |
| Chấm hàng loạt nhiều file | `python tools/word/cham-loat.py <thu-muc> --md ket-qua.md` |
| Cập nhật TOC/field & xuất PDF (Windows + Word) | `python tools/word/word-hoan-tat.py file.docx --pdf file.pdf` |

## Liên quan

- [[quy-trinh-bao-cao-ctut]] — chi tiết chuẩn QĐ 345/2025
- [[nckh-quy-che-sv04]] — quy chế SV04 cho NCKH sinh viên
- [[luat-viet-noi-dung]] — 10 luật chống ảo giác và nhất quán số liệu
- [[quy-uoc-viet-van-khoa-hoc]] — quy ước văn phong và trích dẫn khoa học
