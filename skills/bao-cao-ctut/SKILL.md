---
name: bao-cao-ctut
description: Quy trình + bộ mẫu chuẩn cho báo cáo Đồ án / NCKH / Luận văn tốt nghiệp ở Trường Đại học Kỹ thuật – Công nghệ Cần Thơ (CTUT), bám QĐ 345/QĐ-ĐHKTCN ngày 08/4/2025 của Hiệu trưởng (ĐATN/KLTN/TTTN, đồ án) và QĐ 886/QĐ-ĐHKTCN (2022) cho NCKH sinh viên (mẫu SV04) + hướng dẫn định dạng báo cáo Đồ án. Dùng khi bắt đầu, viết, sửa hoặc nộp một báo cáo học thuật: tạo 2 bìa chuẩn bằng 1 lệnh, điền thông tin, kiểm tra định dạng, chuẩn hoá file cũ, chấm điểm hàng loạt. Kích hoạt khi người dùng nói "làm báo cáo", "viết đồ án", "luận văn", "NCKH", "sửa bìa", "kiểm tra format", "nộp báo cáo".
version: 1.5.1
updated: 2026-11-18
---

# Báo cáo CTUT — quy trình chuẩn + bộ mẫu (theo QĐ 345/2025)

## 0. Nguyên tắc số 1: bìa quyết định giám khảo có đọc hay không

> Khung bìa NCKH = **ảnh nền** `templates/word/img/khung-bia-sv04.png` (đổi viền = thay PNG);
> gạch đầu dòng dùng **"- "** (không dùng ●/•).

Nội dung tốt đến đâu mà bìa sai (sai cỡ chữ, thiếu bìa phụ/trang xác nhận, còn dòng chấm, chữ màu)
thì người chấm mất thiện cảm trước khi đọc dòng nào. Vì vậy: **làm bìa trước, nhìn tận mắt, rồi mới viết.**

Thứ tự bắt buộc:
1. Tạo khung + bìa bằng `du-an-moi.py`
2. Mở `bia-preview.png` **xem bằng mắt** — sai thì sửa ngay
3. Chỉ khi bìa đúng mới viết chương

## 0.4. NCKH sinh viên — chuẩn RIÊNG (QĐ 886/2022, mẫu SV04)

NCKH **không** dùng form đồ án/ĐATN. Chi tiết: `wiki/quy-trinh/nckh-quy-che-sv04.md`. Tóm:

- Bố cục: **bìa Mẫu 1** (bìa cứng xanh dương) → lời cảm ơn → **Mẫu 2** (thông tin kết quả NC, 6 mục, 1 trang) →
  **Mẫu 3** (thông tin sinh viên chịu trách nhiệm chính, 1 trang) → mục lục → danh mục bảng/hình → từ viết tắt →
  **ĐẶT VẤN ĐỀ** → **CHƯƠNG 1 TỔNG QUAN TÀI LIỆU** → **CHƯƠNG 2 ĐỐI TƯỢNG VÀ PHƯƠNG PHÁP NGHIÊN CỨU** →
  **CHƯƠNG 3 KẾT QUẢ VÀ THẢO LUẬN** → KẾT LUẬN VÀ KIẾN NGHỊ → TLTK → PHỤ LỤC (bắt buộc: bản sao thuyết minh đã duyệt + minh chứng bài báo).
- Hình thức: TNR 13 · giãn **1,3–1,5** · lề **3/2/2/2** · header/footer 1cm · **số trang giữa dưới** ·
  in **một mặt** · **50–100 trang** · 3 chương (không phải 5 chương kiểu đồ án).
- Template: `templates/word/nckh/mau-bao-cao-tong-ket-sv04.docx`.

## 0.5. Luật nội dung — chống ảo giác (bắt buộc)

Chi tiết: `wiki/quy-trinh/luat-viet-noi-dung.md`. Tóm 8 luật:

1. **Không có số liệu thật thì không viết số nào.** Chưa đo → `[CẦN SỐ LIỆU: …]`.
2. **Không bịa nguồn**: mọi `[n]` phải có trong danh mục TLTK và đã thực sự đọc; cấm bịa tên tác giả/tạp chí/năm/DOI.
3. **Không kể chuyện không xảy ra**: không thêm hoạt động, khảo sát, thí nghiệm chưa làm.
4. **Số phải có đơn vị + điều kiện đo** (`97,1 %`, `±0,02 g`, "tải 1,5 kg") — sai số và chữ số có nghĩa thống nhất.
5. **Nhất quán 3 nơi**: TÓM TẮT ↔ chương KẾT QUẢ ↔ KẾT LUẬN cùng một số.
6. **Không thổi phồng**: cấm "hoàn hảo/tuyệt vời/rất tốt/xuất sắc" khi không có thang đo — thay bằng số + so mục tiêu.
7. **Nêu hạn chế** mỗi chương kết quả; không giấu điểm yếu; phân biệt rõ **mô phỏng** vs **đo thực**.
8. **Không chắc thì đánh dấu** `[?]` / `[CẦN KIỂM CHỨNG]` rồi hỏi lại — không đoán.

Trước khi nộp: `python tools/word/kiem-tra-noi-dung.py <file>` (bắt placeholder, % không dẫn chứng, trích dẫn lệch,
số liệu TÓM TẮT/KẾT LUẬN lệch nhau). ≥90 mới nộp. Tool chỉ bắt *dấu hiệu* — người vẫn phải đọc.

## 1. Ba loại báo cáo — KHÁC NHAU, đừng dùng chung một kiểu

| | Đồ án (ĐA1/2/3) | ĐATN / KLTN | TTTN |
|---|---|---|---|
| In giấy | **hai mặt** | **một mặt** | một mặt |
| Bìa cứng | **xanh dương** + gáy xanh dương | xanh dương | **xanh lá** |
| Khung bìa | **không** | có (màu `1F3864`) | có |
| Bìa phụ + xác nhận | bìa phụ + **xác nhận đơn vị** + "Ngày nộp báo cáo" | BM 2.2 + **BM 2.3** (3 ô chữ ký ban chấm) | bìa phụ + xác nhận GV |
| Số trang | **giữa, phía DƯỚI** (footer trái: tên SV nghiêng; header: tiêu đề phần nghiêng) | **giữa, phía TRÊN** | giữa, trên |
| Trang tối thiểu | **30** | **40** | theo đơn vị |
| Danh mục | bảng biểu → hình ảnh | hình vẽ → bảng biểu | hình → bảng |

Mẫu: `templates/word/do-an/`, `luan-van/`, `nckh/` (đều 100/100 theo `kiem-tra.py`).

## 2. Quy trình 7 bước

1. **Xác định loại** (đồ án / ĐATN-KLTN / NCKH / TTTN) — quyết định bìa, in, số trang, cấu trúc.
2. **Tạo báo cáo mới**:
   `python tools/word/du-an-moi.py --loai do-an --ten "Tên đề tài" --nganh "..." --sv "Họ tên" --mssv "..." --gvhd "TS. ..." --out "./out/BaoCao.docx" --mo`
   → sinh file 2 bìa + front matter + 4 chương + `bia-preview.png` (nếu có LibreOffice + `pymupdf`) + `CHECK-LIST.md`.
3. **Nhìn `bia-preview.png`** — so với ảnh mẫu `assets/word/mau-bia-chinh.png`, `mau-bia-phu.png`.
4. **Viết nội dung** theo cấu trúc §4; tên bảng TRÊN bảng, tên hình DƯỚI hình; heading bằng style Heading.
5. **F9** cập nhật mục lục + danh mục; chạy `python tools/word/kiem-tra.py file.docx` → phải ≥ 90.
6. **Xuất bản bằng Word thật** (bước cuối, chuẩn nhất):
   `python tools/word/word-hoan-tat.py file.docx --pdf file.pdf` (cần Windows + Microsoft Word + `pip install pywin32`)
   → Word cập nhật mọi field (PAGE, TOC, danh mục bảng/hình), repaginate, lưu .docx và xuất PDF.
   Nếu có cài thêm validator OpenXML (`openxml-audit`): `openxml-audit file.docx -f microsoft365 -q` (exit 0 = không lỗi).
   Chỉ in **PDF do Word xuất** — LibreOffice có thể lệch trang/khung.
7. **In**: đúng chế độ in + bìa cứng đúng màu + dán gáy; nộp 2 bản in + 1 PDF sau bảo vệ 7 ngày.

## 3. Số đo chuẩn (QĐ 345 + HD Đồ án)

- A4 (21 × 29,7 cm); **lề Trái 3 · Phải 2 · Trên 2 · Dưới 2 cm**; header/footer **1 cm**
- Times New Roman **13**; **giãn dòng 1,2**; cách đoạn **6 pt (before + after)**; thụt **1 cm**; justify
- Đề mục: TÊN CHƯƠNG 14 in hoa đậm giữa; cấp 1 in hoa đậm; cấp 2 đậm; **cấp 3 đậm nghiêng**;
  tên bảng 13 đậm trái-trên; chú thích bảng 11 nghiêng; tên hình 13 đậm giữa-dưới; ghi chú hình 11 nghiêng
- Số trang: La Mã cho mục mở đầu, Ả Rập từ nội dung chính; mỗi nhóm mục **≥ 2 mục**
- Bảng nên **3 dòng** (hạn chế kẻ dọc), ô trống ghi "-", khi nhắc phải gọi số ("xem Hình 2.3")

## 4. Cấu trúc nội dung

- **Đồ án**: LỜI MỞ ĐẦU (1–2 tr: lý do / mục tiêu & phạm vi / ý nghĩa) → CH1 TỔNG QUAN ĐỀ TÀI (¼)
  → CH2 CƠ SỞ LÝ THUYẾT (¼) → CH3 THIẾT KẾ VÀ CHẾ TẠO SẢN PHẨM (hoặc KẾT QUẢ VÀ THẢO LUẬN, ⅓)
  → CH4 KẾT LUẬN VÀ KIẾN NGHỊ (1–2 tr) → TLTK → PHỤ LỤC
- **ĐATN/KLTN**: CH1 TỔNG QUAN LÝ THUYẾT VÀ CƠ SỞ NGHIÊN CỨU → CH2 PHƯƠNG TIỆN NGHIÊN CỨU -
  PHƯƠNG PHÁP NGHIÊN CỨU → CH3 KẾT QUẢ VÀ THẢO LUẬN → CH4 KẾT LUẬN VÀ ĐỀ XUẤT
- **TTTN**: CH1 GIỚI THIỆU TỔNG QUAN (1/3: đơn vị, công việc, an toàn–vệ sinh) → CH2 TỔNG QUAN CƠ SỞ
  LÝ THUYẾT → CH3 KẾT QUẢ – THẢO LUẬN (nội dung, phân tích, giải pháp) → CH4 KẾT LUẬN VÀ ĐỀ XUẤT

## 5. Sáu lỗi hay mắc trong thực tế

1. Heading để **xanh mặc định Word** (`365F91`/`4F81BD`) hoặc **font theme Calibri** — sai.
2. Bìa còn **dòng chấm điền tay** ("TRƯỜNG ĐẠI HỌC …….") — dấu hiệu chưa hoàn thiện.
3. **Không có mục lục field TOC** → không cập nhật số trang được.
4. **Sai lề** (2/2/3/2 của mẫu đề cương; 3/3/3,5/2 của quy định cũ) — chuẩn hiện hành là **3/2/2/2**.
5. **Giãn dòng 1,5** (hoặc 1,3) dùng cho đồ án/ĐATN — chuẩn QĐ 345 là **1,2** (riêng SV04 là **1,3–1,5**).
6. **Ngày bìa nghiêng / tên đề tài chữ đen** — bìa ĐATN: ngày 14 đậm, tên đề tài xanh dương.

## 6. Cập nhật và đổi mới

- Nguồn chuẩn có thể đổi: **luôn kiểm tra trang Khoa** `https://khoaddt.ctuet.edu.vn/` trước khi dùng
  (nếu gặp link cũ dạng `khoaddtvt.ctuet.edu.vn`, hãy kiểm tra lại trên domain `khoaddt.ctuet.edu.vn`).
- Khi có văn bản mới: cập nhật `wiki/quy-trinh/quy-trinh-bao-cao-ctut.md` §2–§5, tăng version file này,
  ghi vào `CHANGELOG.md`, render lại ảnh mẫu trong `assets/word/`.
- Chấm lại toàn bộ mẫu: `python tools/word/cham-loat.py templates/word --md cham-mau.md` → tất cả mẫu báo cáo phải đạt 100.

## 7. File liên quan

- Note quy trình đầy đủ: `wiki/quy-trinh/quy-trinh-bao-cao-ctut.md`
- Luật nội dung: `wiki/quy-trinh/luat-viet-noi-dung.md` (chống ảo giác, quy ước đánh dấu, dấu hiệu ảo giác)
- Văn khoa học: `wiki/quy-trinh/quy-uoc-viet-van-khoa-hoc.md` (claim–evidence, trích dẫn IEEE, 12 câu xấu→sửa)
- Mẫu: `templates/word/{do-an,luan-van,nckh}/mau-*.docx` + `templates/word/README.md`
- Công cụ: `tools/word/du-an-moi.py` (tạo + điền bìa), `word-hoan-tat.py` (Word COM: field + TOC + PDF),
  `bia-sv04.py` (dựng bìa Mẫu 1 NCKH), `dong-bo-muc-luc.py` (số trang mục lục), `kiem-tra.py` (chấm format 100 điểm),
  `kiem-tra-noi-dung.py` (soát nội dung/ảo giác + `TIEU_MUC_MONG`),
  `chuan-hoa.py` (chuẩn hoá file cũ), `cham-loat.py` (chấm hàng loạt)
- Ảnh mẫu: `assets/word/{mau-bia-chinh,mau-bia-phu,mau-bia-do-an,mau-trang-xac-nhan,nckh-mau-2,nckh-mau-3}.png`
