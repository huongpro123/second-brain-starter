---
name: phan-bien-bao-cao
description: Kiểm chứng đối nghịch (Adversarial Verification) cho báo cáo đồ án, luận văn, NCKH CTUT trước khi nộp. Đóng vai Ủy viên phản biện độc lập để soi sai lệch số liệu, lỗi trích dẫn treo, câu khẳng định thiếu bằng chứng, lỗ hổng thực nghiệm và câu hỏi hội đồng chắc chắn sẽ hỏi. Kích hoạt khi người dùng nói "phản biện", "soi lỗi nội dung", "kiểm tra kỹ trước khi nộp", "đóng vai hội đồng", "check chéo số liệu".
version: 1.0.0
updated: 2026-11-21
---

# Phản biện báo cáo — Kiểm chứng đối nghịch trước khi nộp

> **Nguyên tắc:** Không khen xã giao, không sửa hộ ngay từ đầu, không tự tin rằng "bản thảo đã ổn".
> Nhiệm vụ duy nhất của skill này là **tìm bằng chứng không khớp, lỗ hổng logic và điểm dễ bị trừ điểm nhất**.

Đọc kèm trước khi phản biện:
- `wiki/quy-trinh/luat-viet-noi-dung.md`
- `wiki/quy-trinh/quy-uoc-viet-van-khoa-hoc.md`
- `wiki/quy-trinh/quy-trinh-bao-cao-ctut.md` (hoặc `nckh-quy-che-sv04.md` nếu là NCKH)

---

## Quy trình 5 bước (độc lập với tác giả)

### Bước 1: Chạy hai bộ đo tự động trước

```powershell
python tools/word/kiem-tra.py "<file.docx>"
python tools/word/kiem-tra-noi-dung.py "<file.docx>"
```

Ghi nhận điểm thật và mọi dòng `FAIL` / `WARN`. Nếu định dạng < 90 hoặc còn placeholder `[CẦN ...]`, `[?]` → **chặn nộp ngay**.

### Bước 2: Đối chiếu chéo số liệu (Tóm tắt ↔ Nội dung ↔ Kết luận ↔ Bảng/Hình ↔ `raw/`)

Kiểm tra theo 4 câu hỏi bắt buộc:
1. Mỗi con số ở Tóm tắt / Mẫu 2 và Kết luận có xuất hiện **đúng y hệt** (cùng giá trị, sai số, đơn vị) trong Chương Kết quả và Bảng/Hình không?
2. Có kết quả nào là **mô phỏng** nhưng viết mập mờ thành **đo thực nghiệm** không?
3. Các phép đo có ghi rõ **điều kiện đo** (tải, điện áp, tốc độ, nhiệt độ, số mẫu lặp `n`, thiết bị đo) không?
4. Nếu người dùng cung cấp log/CSV/ảnh gốc: giá trị trung bình, max, sai số % trong bảng Word có khớp dữ liệu gốc không?

### Bước 3: Kiểm tra trích dẫn & TLTK

1. Mọi `[n]` trong thân bài đều tồn tại trong danh mục Tài liệu tham khảo và ngược lại (không trích dẫn treo).
2. Không có câu khẳng định định lượng kiểu *"nhiều nghiên cứu cho thấy..."*, *"hệ thống rất ổn định..."* mà thiếu `[n]` hoặc Bảng/Hình chứng minh.
3. Thông số thiết bị/chuẩn IEC/TCVN lấy từ datasheet hoặc quy định có ghi nguồn rõ ràng.

### Bước 4: Đóng vai Hội đồng CTUT — 5 góc bắt bẻ thường gặp

Kiểm tra xem bản thảo đã giải thích thuyết phục chưa (nếu chưa → ghi vào mục câu hỏi hội đồng):
1. **Tính cấp thiết & điểm mới:** Điểm mới là thực chất hay chỉ ghép module sẵn? Đã so sánh với phương án nền (baseline) chưa?
2. **An toàn & biên giới hạn:** Nếu làm phần cứng/điện/SCADA — đã xử lý lỗi mất kết nối, quá dòng, E-Stop, nối đất/an toàn điện hay lỗ hổng bảo mật chưa? Có dám ghi thẳng **hạn chế** không?
3. **Tính tái lập:** Người khác đọc Chương Phương pháp có lắp/chạy lại được không, hay thiếu phiên bản phần mềm, sơ đồ đấu dây, thông số cấu hình?
4. **Cấu trúc & văn phong CTUT:** Có lọt ngôi "em/chúng em", văn kể chuyện, tiêu mục < 2 đoạn văn, hoặc sai loại báo cáo (Đồ án / ĐATN / SV04) không?

### Bước 5: Xuất Phiếu Phản Biện (đúng 3 mức)

Trả lời bằng một bảng/danh sách rõ ràng để tác giả xử lý:

- **CRITICAL (Chặn nộp — bắt buộc sửa):** Số liệu mâu thuẫn, còn placeholder, sai chuẩn loại báo cáo, khẳng định sai thực tế, lỗi định dạng `FAIL`.
- **MAJOR (Dễ bị trừ điểm / hội đồng vặn):** Thiếu điều kiện đo, thiếu giải thích nguyên nhân sai lệch, thiếu phần hạn chế, văn phong kể chuyện, tiểu mục quá mỏng.
- **MINOR (Góp ý hoàn thiện):** Chữ viết tắt chưa vào danh mục, lỗi chính tả/đơn vị, cách đặt tên bảng/hình.
- **5 câu hỏi hội đồng có xác suất hỏi cao nhất** kèm vị trí trang/mục trong bài đang yếu.
