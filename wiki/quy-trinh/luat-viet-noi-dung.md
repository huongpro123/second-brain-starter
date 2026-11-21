---
title: Luật viết nội dung báo cáo — chống ảo giác, chống số liệu bịa
updated: 2026-11-21
status: active
tags: [quy-trinh, bao-cao, noi-dung, chong-ao-giac]
sources:
  - "Hướng dẫn, định dạng báo cáo Đồ án (ĐA1/2/3)"
  - "Hướng dẫn trình bày ĐATN/KLTN/TTTN — QĐ 345/QĐ-ĐHKTCN 08/4/2025, mục 1.2.4 viết tắt + 1.3 trích dẫn"
  - "[[quy-trinh-bao-cao-ctut]]"
---

# Luật viết nội dung báo cáo — chống ảo giác, chống số liệu bịa

> [!danger] Luật số 0
> **Không có số liệu thật thì không được viết ra một con số nào.**
> Không đo được → ghi `[CẦN SỐ LIỆU: mô tả cần đo gì]` và hỏi lại tác giả, **không lấy số cho đẹp bài**.
> Không đọc tài liệu → ghi `[CẦN TRÍCH DẪN]`, **không bịa tên tác giả, năm, tạp chí, DOI**.

Áp dụng cho: đồ án (ĐA1/2/3), NCKH, ĐATN/KLTN, TTTN — và mọi văn bản học thuật mà AI agent hỗ trợ soạn thảo.

## 1. Mười luật nội dung

1. **Số liệu phải có nguồn nội bộ**: từ log đo, file CSV, ảnh chụp màn hình, hoặc buổi đo có ghi ngày.
   Số không có nguồn = số bịa, kể cả khi "trông hợp lý".
2. **Không kể chuyện không xảy ra**: không thêm "nhóm đã khảo sát 30 hộ dân", "đã thử nghiệm 3 tháng"
   nếu thực tế không làm. Không mô tả kết quả chưa đạt được.
3. **Trích dẫn phải thật**: mỗi khẳng định khoa học cần `[n]` trỏ tới tài liệu **có trong danh mục TLTK**
   và **đã thực sự đọc**. Không bịa: tên tác giả, tên bài, tên tạp chí, năm, số trang, DOI.
4. **Số liệu phải kèm đơn vị + điều kiện đo**: `97,1 %` (không phải `97.1`), `±0,02 g`, "với tải 1,5 kg,
   nhiệt độ phòng 28 ± 2 °C". Không có điều kiện đo thì con số vô nghĩa.
5. **Nhất quán số liệu giữa 3 nơi**: TÓM TẮT ↔ chương KẾT QUẢ ↔ KẾT LUẬN phải cùng một con số.
   Sửa ở một chỗ thì phải rà lại hai chỗ kia.
6. **Không thổi phồng**: cấm "hoàn hảo", "tuyệt vời", "kết quả rất tốt", "xuất sắc" khi không có thang đo.
   Thay bằng số + so sánh với mục tiêu.
7. **Trung thực về giới hạn**: mỗi chương kết quả phải nêu hạn chế (sai số, phạm vi áp dụng, điều kiện biên,
   điều chưa kiểm chứng). Không giấu điểm yếu.
8. **Không lan man**: chỉ viết đúng đề tài, đúng mục tiêu đã nêu ở LỜI MỞ ĐẦU. Không copy lý thuyết
   không dùng tới; mỗi đoạn phải trả lời được "đoạn này phục vụ mục tiêu nào".
9. **Văn phong khách quan**: hạn chế "em/chúng em/mình"; không cảm xúc, không khẩu ngữ, không emoji.
   Dùng "nhóm thực hiện", "kết quả cho thấy", "có thể thấy".
10. **Không chắc thì đánh dấu, không đoán**: dùng `[?]` hoặc `[CẦN KIỂM CHỨNG]` ngay chỗ đó,
    rồi hỏi lại tác giả. Đoán bừa bị phát hiện trong buổi bảo vệ còn tệ hơn bỏ trống.

## 2. Dấu hiệu ảo giác — agent tự soát trước khi nộp

| Dấu hiệu | Nghĩa là | Sửa thế nào |
|---|---|---|
| Con số tròn trịa bất thường (100 %, 0 %, 99,9 %) | thường là số ước lượng/bịa | thay bằng số đo thật hoặc ghi rõ "ước tính" |
| "Theo nhiều nghiên cứu…" mà không có `[n]` | khẳng định suông | thêm `[n]` thật hoặc bỏ câu |
| Tên tác giả/tạp chí tiếng Anh "nghe hợp lý" | nguy cơ bịa nguồn | mở file PDF thật trong `raw/` để kiểm |
| Bảng kết quả không nói thiết bị/mẫu | không kiểm chứng được | thêm cột điều kiện đo |
| Số ở tóm tắt khác số ở kết luận | mâu thuẫn | đồng bộ một nguồn số duy nhất |
| Đoạn văn dài không có số, không có `[n]`, không có hình | có thể là "văn cho đủ trang" | cắt hoặc thay bằng dẫn chứng |
| Kết quả "vượt mục tiêu" ở mọi chỉ tiêu | quá đẹp để tin | rà lại điều kiện đo + sai số |

## 3. Quy ước đánh dấu (để không bịa mà vẫn viết tiếp được)

| Đánh dấu | Dùng khi | Ai xử lý |
|---|---|---|
| `[CẦN SỐ LIỆU: …]` | cần số đo nhưng chưa có | Tác giả đo / cung cấp log |
| `[CẦN TRÍCH DẪN: chủ đề]` | cần nguồn nhưng chưa đọc | Agent tìm + tác giả xác nhận |
| `[CẦN KIỂM CHỨNG]` | suy luận chưa thử | Thí nghiệm bổ sung |
| `[?]` | agent không chắc | Tác giả quyết định |

**Không được để các dấu này trong bản in cuối** — trước khi nộp chạy `kiem-tra-noi-dung.py`, nó bắt hết.

## 4. Trích dẫn — tối thiểu phải đúng

- Số `[n]` phải khớp danh mục TLTK: có `[7]` thì TLTK phải có mục 7.
- Sách: `Tên tác giả (năm), Tên sách (in nghiêng), Nhà xuất bản.`
- Bài tạp chí: `Tác giả (năm), "Tên bài", Tên tạp chí (in nghiêng), tập(số), trang.`
- Web: `Tác giả (nếu có), năm (nếu có). Tên tài liệu, <đường dẫn>, truy cập ngày …/…/….`
- Không trích nguồn cấp 2 khi có bản gốc; không trích Wikipedia/forum làm nguồn chính.
- Ưu tiên: tiêu chuẩn (TCVN/IEC), giáo trình, bài báo khoa học, tài liệu nhà sản xuất.

## 5. Số liệu — quy ước trình bày

- Thập phân dùng **dấu phẩy**: `12,5 V`; phân cách nghìn dùng **dấu chấm**: `1.250 Hz` (quy ước VN).
- Mỗi số phải có **đơn vị** và **sai số** nếu là số đo: `96,8 ± 0,3 %`.
- Thống nhất số chữ số có nghĩa trong cả bảng (thường 1–2 chữ số thập phân).
- Bảng: tên bảng ở **trên**, đơn vị ghi trong tiêu đề cột, ô trống ghi `-`, có chú thích dưới bảng.
- Hình: tên hình ở **dưới**, trục có đơn vị, có chú thích; số liệu gốc giữ trong `raw/` của vault.

## 6. Quy luật riêng theo loại (khác nhau thật)

| | Đồ án | NCKH | ĐATN / KLTN |
|---|---|---|---|
| Trọng tâm nội dung | sản phẩm chạy được + đánh giá thực nghiệm | tính mới + phương pháp + kết quả nghiên cứu | nghiên cứu đầy đủ + so sánh tài liệu |
| Bắt buộc có | sơ đồ nguyên lý, ảnh sản phẩm, kết quả đo trên sản phẩm | câu hỏi nghiên cứu, phương pháp, kết quả so với baseline | tổng quan tài liệu sâu + thảo luận |
| Độ dài nội dung | ≥ 30 trang | theo đơn vị quản lý | ≥ 40 trang |
| Số liệu bắt buộc | chỉ tiêu kỹ thuật đo được (sai số, độ ổn định) | số liệu chứng minh giả thuyết + so sánh | số liệu + đối chiếu tài liệu |
| Cấm | nhận "chạy ổn định" mà không có log | nhận "mới" mà không so baseline | nhận "vượt trội" mà không dẫn chứng |

## 7. Trước khi nộp — 10 câu tự vấn

1. Con số nào trong bài mà tôi **không** chỉ ra được nguồn? → xoá hoặc đánh dấu.
2. Có `[n]` nào **không** nằm trong TLTK? → sửa.
3. Tên tài liệu nào tôi **chưa mở** mà vẫn trích? → mở hoặc bỏ.
4. TÓM TẮT, chương kết quả, KẾT LUẬN có **cùng số** không?
5. Mỗi bảng/hình có điều kiện đo chưa?
6. Có câu nào kết luận **mạnh hơn** dữ liệu cho phép? → hạ giọng.
7. Có đoạn nào chỉ để **cho dài**? → cắt.
8. Có từ thổi phồng nào? → thay bằng số.
9. Đã ghi **hạn chế** chưa?
10. Đã chạy `python tools/word/kiem-tra-noi-dung.py <file>` chưa?

## 8. Quy tắc hình thức viết bổ sung

- **Tiểu mục ≥2 đoạn văn**: chỉ tách heading khi có ít nhất hai đoạn triển khai; một đoạn lẻ thì gộp dưới mục cha (`kiem-tra-noi-dung.py` → `TIEU_MUC_MONG`).
- **Mỗi danh mục một trang**: MỤC LỤC / DANH MỤC BẢNG BIỂU / DANH MỤC HÌNH VẼ / DANH MỤC TỪ VIẾT TẮT bắt đầu trang riêng.
- **Khung trang chỉ ở bìa** (với báo cáo NCKH/ĐATN/KLTN); trang thân không khung.
- **Khoa học ≠ thi văn**: mỗi khẳng định định lượng phải có dẫn chứng (số đo của chính mình + bảng/hình, hoặc `[n]` tới tài liệu tham khảo). Không viết "hệ thống hoạt động rất tốt" mà thiếu điều kiện đo, thiết bị đo, sai số.
- Văn phong: khách quan, ngôi thứ ba/tổ chức ("nhóm thực hiện"), không kể chuyện, không cảm xúc, không cường điệu.
- **Gạch đầu dòng** dùng `- ` (không dùng ●/•/*) — chuẩn trình bày tiếng Việt.

## Liên quan

- [[quy-trinh-bao-cao-ctut]] — form, số trang, bìa, quy trình (QĐ 345/2025)
- [[quy-uoc-viet-van-khoa-hoc]] — quy tắc claim–evidence và câu xấu → câu sửa
- [[ky-nang-viet-word]] — kỹ năng format + kiểm tra file Word
- Công cụ: `tools/word/kiem-tra-noi-dung.py` (soát nội dung), `tools/word/kiem-tra.py` (soát format)
