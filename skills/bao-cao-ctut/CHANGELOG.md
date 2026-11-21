# CHANGELOG — bao-cao-ctut

## 1.5.1 — 2026-11-18
- Chuẩn hoá quy tắc khung bìa SV04 bằng ảnh nền PNG (`khung-bia-sv04.png`) đặt behindDoc để Word và LibreOffice hiển thị giống nhau, không bị dính khung qua các trang sau.
- Chuẩn hoá gạch đầu dòng dùng `- ` thay cho ký tự symbol `●`/`•`.
- Bổ sung công cụ `word-hoan-tat.py` (Word COM automation) cập nhật TOC/PAGE/repaginate và xuất PDF chuẩn in, cùng `dong-bo-muc-luc.py` và kiểm tra tiểu mục mỏng (`TIEU_MUC_MONG`).

## 1.4.0 — 2026-11-18
- Thêm **NCKH sinh viên theo chuẩn riêng QĐ 886/QĐ-ĐHKTCN (2022)** — không dùng form đồ án/ĐATN:
  - Bố cục bắt buộc: bìa **Mẫu 1** (bìa cứng xanh dương) → lời cảm ơn → **Mẫu 2** (thông tin kết quả NC, 6 mục) →
    **Mẫu 3** (thông tin sinh viên chịu trách nhiệm chính) → mục lục → danh mục bảng/hình → từ viết tắt →
    ĐẶT VẤN ĐỀ → 3 chương (Tổng quan tài liệu / Đối tượng và phương pháp / Kết quả và thảo luận) → Kết luận và kiến nghị →
    TLTK → Phụ lục (bắt buộc có bản sao thuyết minh đã duyệt + minh chứng bài báo).
  - Hình thức: TNR 13, giãn **1,3–1,5**, lề **3/2/2/2**, header/footer 1cm, **số trang giữa dưới**, in một mặt,
    **50–100 trang**, tối đa 4 cấp đề mục.
  - Template mới `templates/word/nckh/mau-bao-cao-tong-ket-sv04.docx`; note `wiki/quy-trinh/nckh-quy-che-sv04.md`.

## 1.3.0 — 2026-11-18
- Thêm **luật nội dung chống ảo giác** (mục 0.5): không bịa số liệu, không bịa nguồn, không kể chuyện
  không xảy ra, số phải có đơn vị + điều kiện đo, nhất quán TÓM TẮT ↔ KẾT QUẢ ↔ KẾT LUẬN, không thổi phồng,
  nêu hạn chế, không chắc thì đánh dấu `[?]`/`[CẦN SỐ LIỆU]`.
- Note mới `wiki/quy-trinh/luat-viet-noi-dung.md` + tool `tools/word/kiem-tra-noi-dung.py`.

## 1.2.0 — 2026-11-18
- **Chuyển sang chuẩn cấp TRƯỜNG: QĐ 345/QĐ-ĐHKTCN ngày 08/4/2025 của Hiệu trưởng**, thay thế các thông số dựng theo QĐ 407 (Khoa, 2023):
  - Số trang ĐATN/KLTN: **giữa, phía TRÊN**
  - Đồ án: **in HAI mặt, bìa cứng xanh dương, KHÔNG khung**, tối thiểu **30 trang**
  - Giãn dòng **1,2**
  - Biểu mẫu: **BM 2.1 bìa chính / BM 2.2 bìa phụ / BM 2.3 trang xác nhận**
  - Cấu trúc **4 chương** với tên riêng cho đồ án / ĐATN-KLTN / TTTN
- Viết lại 3 mẫu `.docx` chuẩn (4/4 mẫu báo cáo đạt **100/100** với `kiem-tra.py`).

## 1.1.0 — 2026-11-18
- Chuẩn hoá công cụ tạo khung + bìa `du-an-moi.py` và chấm hàng loạt `cham-loat.py`.
- Bổ sung note quy trình `wiki/quy-trinh/quy-trinh-bao-cao-ctut.md`.

## 1.0.0 — 2026-11-18
- Ra mắt skill: quy trình 6 bước + 3 mẫu báo cáo + 1 mẫu đề cương + `kiem-tra.py`, `chuan-hoa.py`, `cham-loat.py`.
