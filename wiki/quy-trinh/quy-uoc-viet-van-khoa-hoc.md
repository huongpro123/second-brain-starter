---
title: Quy ước viết văn khoa học — claim phải có evidence
updated: 2026-11-21
status: active
tags: [quy-trinh, viet-van-khoa-hoc]
sources:
  - "https://ece.illinois.edu/academics/grad/overview/thesis-ieee"
  - "https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/"
  - "https://www.elsevier.com/about/policies-and-standards/publishing-ethics"
  - "https://www.phrasebank.manchester.ac.uk/referring-to-sources/"
  - "https://www.phrasebank.manchester.ac.uk/using-cautious-language/"
  - "https://lib.hcmute.edu.vn/ArticleId/e4db314c-3179-4756-8ee0-3d199ecb3d80/huong-dan-trich-dan-tai-lieu-tham-khao-theo-chuan-ieee-va-apa"
  - "https://lib.hcmute.edu.vn/?ArticleId=d8a888b3-a153-4daf-a013-de872b60a0fd"
  - "https://icmje.acponline.org/news-and-editorials/updated_recommendations_jan2025.html"
---

# Quy ước viết văn khoa học — claim phải có evidence

> "Đây là bài khoa học, đâu phải thi văn..." — đúng. Câu không kèm số, Bảng/Hình hay [n] thì chỉ là **ý kiến**, không phải **kết quả**.

Đọc kèm: [[luat-viet-noi-dung]] · [[quy-trinh-bao-cao-ctut]] · [[prompt-lam-bao-cao]]

## 1. Nguyên tắc claim–evidence

**Claim** = câu khẳng định về kết quả/chất lượng/so sánh. **Evidence** = chỗ dựa kiểm chứng được. Claim hợp lệ khi người đọc lần được tới đúng con số.

Ba loại evidence được phép:
- **Tự đo** → dẫn vị trí: "(Bảng 3.5)", "(Hình 3.9)", "(mục 3.4.2)".
- **Nguồn ngoài** → dẫn số hiệu: "[3]", "[5], [7]".
- **Suy luận từ dữ liệu đã dẫn** → chỉ rõ dữ liệu nào: "Từ Bảng 3.5, sai lệch tăng khi tải > 80 %, phù hợp với đặc tuyến trong [4]".

Không được viết khi thiếu số/tiêu chí: "hệ thống rất tốt", "hoạt động ổn định", "đạt hiệu quả cao", "đáp ứng yêu cầu", "tối ưu", "an toàn". Phải nói rõ **tốt theo tiêu chí nào, đo ở đâu, bao nhiêu**.

Phép thử 3 câu cho mỗi câu kết luận: **Số nào? Ở đâu (Bảng/Hình/mục)? Ai đo hoặc nguồn nào?** Không trả lời được → xoá câu, hạ mức khẳng định, hoặc ghi `[CẦN SỐ LIỆU: …]` rồi đi đo.

| Loại câu | Ví dụ | Bắt buộc evidence? |
|---|---|---|
| Quan sát | "Điện áp ra đo được 12,04 V." | Có — Bảng/Hình + điều kiện đo |
| Kết luận | "Bộ điều khiển giữ điện áp trong ± 0,2 V." | Có — số + dải tải + Bảng |
| Đề xuất | "Nên thử thêm ở tải 3 A." | Không, nhưng phải nêu căn cứ ngay trước |

## 2. Trích dẫn: khi nào và thế nào

**Bắt buộc [n]** khi:
- số liệu/thông số không do mình đo: "Hiệu suất tấm pin đạt 21,3 % [2]";
- phương pháp/thuật toán/mạch của người khác: PID, SVPWM, MPPT, ANFIS — kể cả khi tự viết lại;
- so sánh với nghiên cứu trước: "cao hơn 2,1 điểm phần trăm so với [6]";
- định nghĩa/khái niệm không phổ thông, tiêu chuẩn TCVN/IEC;
- thông số thiết bị lấy từ datasheet: "Vds = 60 V, Id = 2 A [9]";
- hình/bảng phỏng theo nguồn → ghi "Nguồn: [4]" ngay dưới hình/bảng.

**Không cần [n]** khi: kết quả tự đo (nhưng **phải chỉ Bảng/Hình/Chương**); kiến thức phổ thông trong giáo trình (Ohm, Kirchhoff, Nyquist) trừ khi lấy nguyên câu chữ; kết luận của mình rút ra từ dữ liệu đã dẫn (vẫn phải chỉ về dữ liệu đó).

**Đặt câu dẫn** — chủ ngữ là nghiên cứu, không phải cảm nhận:
- "Nguyễn Văn A và cộng sự [3] đã đề xuất...", "[3] chỉ ra rằng...", "Theo [5], sai lệch dưới 1 % khi...".
- "Kết quả này tương đồng với [7]...", "Trái với kết luận của [8], thí nghiệm này cho thấy...".
- [n] đứng **sát** ý được dẫn, không dồn một cụm [n] cuối đoạn; bỏ "như chúng ta đã biết" (không kiểm chứng được).

**Trích dẫn treo** — lỗi bị bắt nhanh nhất: mọi [n] trong bài phải có trong TÀI LIỆU THAM KHẢO và ngược lại (IEEE: "All sources must be mentioned in the text"); không nhồi citation cho dày (IEEE coi đây là vi phạm đạo đức xuất bản); không trích nguồn chưa đọc (ICMJE: tác giả chịu trách nhiệm về tính chính xác của tài liệu dẫn). Kiểu IEEE: [n] theo thứ tự xuất hiện, đặt trước dấu chấm, nhiều nguồn "[1], [3]" hoặc "[1]–[5]", danh mục theo thứ tự trích — chọn một kiểu và giữ nhất quán cả bài.

## 3. Lỗi "văn kể chuyện" trong báo cáo kỹ thuật

Báo cáo là **bản chứng minh**, không phải nhật ký. Các lỗi phải xoá (câu nào chỉ kể lại thì chuyển thành số hoặc xoá):

1. **Kể cảm xúc**: "em rất lo khi mạch không chạy", "may quá cuối cùng cũng xong".
2. **Ngôi thứ nhất trong nội dung**: "em nghĩ", "tôi thấy" — chỉ dùng "em" ở lời cảm ơn/cam đoan.
3. **Từ thổi phồng**: tuyệt vời, hoàn hảo, siêu nhanh, cực kỳ ổn định, đáng tin cậy tuyệt đối.
4. **Khẳng định không số**: "chạy êm", "không có lỗi", "đáp ứng tốt".
5. **Kể việc đã làm thay vì kết quả**: "em hàn xong, em cắm điện, em đo..." → thay bằng bảng số và kết luận.
6. **Nhân hoá thiết bị**: "board không chịu chạy", "động cơ phản đối", "vi điều khiển hiểu lệnh".
7. **Chuyện ngoài lề**: thức đêm, mưa, mất điện, đi mua linh kiện — trừ khi là **biến** ảnh hưởng kết quả và được ghi như điều kiện thí nghiệm.

## 4. Quy tắc cấu trúc tiểu mục

- **Heading cấp 3 chỉ tách khi có ≥ 2 đoạn văn** (mỗi đoạn 3–6 câu). Một đoạn duy nhất → gộp vào mục cha.
- **Mỗi mục phải có ≥ 2 tiểu mục cùng cấp**: có 1.1.1 thì phải có 1.1.2 (đúng yêu cầu QĐ 345). Không có "1.3.4" đứng một mình.
- **Heading mô tả nội dung**, không dùng từ rỗng: ❌ "Kết quả", "Nhận xét", "Làm rõ", "Một số vấn đề". ✅ "Sai lệch điện áp ở tải 50–100 %", "Hiệu chỉnh hệ số PID", "So sánh với [6]".
- **Không tiểu mục chỉ 1 câu** hoặc chỉ 1 bảng — nội dung đó thuộc mục cha.
- Tối đa 3–4 cấp; heading dùng style Word để mục lục tự cập nhật, không đánh số tay.
- Ví dụ: `3.2 Kết quả` + `3.2.1 Điện áp (1 câu)` + `3.2.2 Dòng điện` + `3.2.3 Nhiệt độ` → gộp thành `3.2 Kết quả đo ở tải định mức`, chia 2 tiểu mục, mỗi tiểu mục 2 đoạn + 1 Bảng/Hình.

## 5. Văn phong và số liệu

- **Câu 15–25 từ**, một câu một ý; quá 40 từ thì tách.
- **Khách quan**: "Mạch được cấp nguồn 24 V DC" hoặc "Nguồn 24 V DC cấp cho mạch" — chọn một kiểu và giữ; không "em".
- **Thì**: hiện tại khi mô tả hệ thống/nguyên lý ("Bộ PID có dạng..."); quá khứ khi tường thuật thí nghiệm đã làm ("Thí nghiệm được chạy 3 lần ở 25 °C"); hiện tại khi trình bày kết quả ("Bảng 3.4 cho thấy...").
- **Bỏ tính từ cảm tính**: "cao", "nhanh", "ổn định" phải kèm đại lượng/ngưỡng — "thời gian xác lập 0,8 s", "sai lệch ≤ 1,06 %".
- **Thuật ngữ nhất quán**: một khái niệm một tên (không lúc "bộ điều khiển", lúc "controller", lúc "bộ điều chỉnh"); viết tắt phải có trong DANH MỤC TỪ VIẾT TẮT.
- **Số kiểu Việt Nam**: phẩy thập phân (`3,3 V`), chấm nghìn (`1.500 W`), khoảng trắng trước đơn vị (`50 Hz`, `1,06 %`), sai số (`12,0 ± 0,2 V`), nhiệt độ (`25 °C`). Không trộn `3.3 V` với `3,3 V`.
- **Số đo phải kèm điều kiện**: "12,04 V tại tải 1,5 A, 27 °C" — thiếu điều kiện là thiếu evidence; không dùng "v.v.", "..." trong câu kết luận.

## 6. Viết đoạn kết quả / thảo luận

Công thức 4 bước cho mỗi đoạn:
1. **Số** (dẫn Bảng/Hình): "Sai lệch điện áp lớn nhất là 1,06 % tại tải 100 % (Bảng 3.5)."
2. **So sánh** với kỳ vọng/tài liệu: "Thấp hơn ngưỡng 2 % ở mục 2.3.2 và tương đồng với [n]."
3. **Giải thích nguyên nhân**: "Do mạch hồi tiếp dùng TL431 có hệ số nhiệt nhỏ; sai lệch tăng ở tải lớn vì sụt áp trên MOSFET."
4. **Giới hạn**: "Chỉ đúng trong dải 0,2–2,0 A, 3 lần đo, nhiệt độ 20–30 °C."

Quy tắc phụ:
- Kết quả xấu hơn tài liệu vẫn phải báo **trung thực** + giả thuyết + cách kiểm chứng.
- Không suy diễn quá dữ liệu: 10 điểm đo ở 20–100 % tải ≠ "chạy tốt mọi điều kiện"; n = 3 không đủ kết luận thống kê.
- Results mô tả, Discussion giải thích — không lặp lại bảng bằng lời.
- Hedge đúng mức: "có thể do", "gợi ý rằng", "cần kiểm chứng thêm" — nhưng đừng hedge đến mức mất kết luận.
- Kết luận chương chỉ mạnh bằng đúng dữ liệu trong chương.

## 7. Checklist tự soát trước khi nộp

- [ ] Mỗi câu kết luận có số, Bảng/Hình, hoặc [n]?
- [ ] Mọi Bảng/Hình được gọi đúng số, không "bảng dưới đây"?
- [ ] Mọi [n] trong bài có trong TLTK và ngược lại?
- [ ] Không còn "rất tốt / ổn định / hiệu quả cao / tối ưu" vô căn cứ?
- [ ] Không còn "em / tôi nghĩ", không kể cảm xúc, không nhân hoá thiết bị?
- [ ] Số dùng phẩy thập phân, đơn vị đúng, có sai số?
- [ ] Mỗi số đo có điều kiện đo (tải, nhiệt độ, số lần lặp)?
- [ ] Heading mô tả nội dung, không "Kết quả / Nhận xét / Làm rõ"?
- [ ] Mỗi mục có ≥ 2 tiểu mục, mỗi tiểu mục ≥ 2 đoạn?
- [ ] Thì hiện tại/quá khứ dùng đúng chỗ?
- [ ] Thuật ngữ nhất quán, viết tắt có trong danh mục?
- [ ] Kết luận không mạnh hơn dữ liệu và có nêu hạn chế?

## 8. Câu xấu → câu sửa (ví dụ minh họa cách viết)

| # | Câu xấu | Lỗi | Câu sửa |
|---|---|---|---|
| 1 | Hệ thống hoạt động rất ổn định. | không số | Trong 10 điểm đo ở tải 20–100 %, sai lệch điện áp lớn nhất là 1,06 % (Bảng 3.5). |
| 2 | Mạch chạy tốt, đáp ứng yêu cầu. | "tốt" không định nghĩa | Điện áp ra giữ 12,0 ± 0,2 V khi dòng tải tăng từ 0,2 A lên 2,0 A (Hình 3.7). |
| 3 | Bộ PID đáp ứng rất nhanh. | không số | Với Kp = 2,4; Ki = 0,8; Kd = 0,05, thời gian xác lập (sai số 2 %) là 0,8 s, không vọt lố (Hình 3.9). |
| 4 | Em đã chỉnh PID rất nhiều lần. | ngôi "em", kể việc | Sai số xác lập giảm từ 4,2 % (PID mặc định) xuống 0,9 % sau hiệu chỉnh (Bảng 3.6). |
| 5 | Động cơ chạy êm, gần như không ồn. | cảm tính | Độ ồn cách động cơ 1 m ở 1.450 vòng/phút là 58 dB(A), dưới mức 70 dB(A) của mục tiêu thiết kế. |
| 6 | Hệ thống đạt hiệu quả cao. | "cao" không mốc | Hiệu suất tại tải định mức đạt 91,3 %, cao hơn 2,1 điểm phần trăm so với mạch nguyên bản (Bảng 3.8). |
| 7 | Kết quả phù hợp với nghiên cứu trước. | không nêu nguồn nào | Kết quả tương đồng với [n]: sai lệch điện áp dưới 1,5 % ở cùng dải tải. |
| 8 | Board lỗi vì em chưa hiểu datasheet. | kể chuyện, không cơ chế | Sai số đo dòng tới 8 % do ACS712-05B bão hoà ở 8 A; sau khi thay ACS712-20A, sai số còn 1,7 % (Bảng 3.4). |
| 9 | Hệ thống an toàn tuyệt đối. | tuyệt đối hoá | Khi thử quá dòng 120 % định mức, rơ-le ngắt sau 42 ms, trong giới hạn 100 ms ở mục 2.3.2 (Hình 3.12). |
| 10 | Tụ lọc có vai trò rất quan trọng. | nhận xét chung | Giảm tụ lọc từ 470 µF xuống 100 µF làm độ gợn tăng từ 24 mV lên 118 mV (Bảng 3.7). |
| 11 | Chắc chắn hệ thống sẽ chạy tốt ở tải lớn hơn. | suy diễn quá dữ liệu | Trong dải 0,2–2,0 A, sai lệch giữ dưới 1,1 %; cần đo thêm ở 3 A trước khi kết luận cho toàn dải (mục 4.2). |
| 12 | Nhờ đồ án em học được rất nhiều. | cảm xúc, ngoài phạm vi | Xoá khỏi phần kết quả; nếu cần, đưa một câu ngắn vào phần kết luận về kỹ năng, không đặt trong mục số liệu. |

Các số trong bảng là ví dụ minh hoạ cách viết — khi áp dụng phải thay bằng số liệu thật của mình.

## 9. Nguồn tham khảo đã đọc

1. [IEEE — Thesis Reference Guide: IEEE Style (UIUC ECE)](https://ece.illinois.edu/academics/grad/overview/thesis-ieee): đánh số [n] theo thứ tự xuất hiện, đặt trước dấu chấm; danh mục phải khớp bài, mọi nguồn phải được nêu trong bài.
2. [IEEE Author Center — Structure Your Article](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/): chức năng từng phần; phần kết luận không thổi phồng; nhồi citation là vi phạm đạo đức xuất bản.
3. [Elsevier — Publishing Ethics](https://www.elsevier.com/about/policies-and-standards/publishing-ethics): cấm bịa/làm giả/sửa dữ liệu, citation manipulation, nộp trùng; nghĩa vụ tác giả.
4. [Manchester — Academic Phrasebank: Referring to Sources](https://www.phrasebank.manchester.ac.uk/referring-to-sources/): mẫu câu dẫn nguồn và cách chọn thì khi nói về tài liệu.
5. [Manchester — Academic Phrasebank: Being Cautious](https://www.phrasebank.manchester.ac.uk/using-cautious-language/): mẫu hedge ("may be due to", "a possible explanation", "interpreted with caution") để không khẳng định quá dữ liệu.
6. [Thư viện HCMUTE — Trích dẫn theo IEEE và APA](https://lib.hcmute.edu.vn/ArticleId/e4db314c-3179-4756-8ee0-3d199ecb3d80/huong-dan-trich-dan-tai-lieu-tham-khao-theo-chuan-ieee-va-apa): mẫu TLTK IEEE/APA tiếng Việt, ví dụ câu dẫn, gợi ý Zotero/Mendeley.
7. [Thư viện HCMUTE — Đạo văn và hướng dẫn trích dẫn](https://lib.hcmute.edu.vn/?ArticleId=d8a888b3-a153-4daf-a013-de872b60a0fd): các dạng đạo văn (không trích nguồn, ghép câu nhiều nguồn, tự đạo văn), hậu quả, cách tránh.
8. [ICMJE — Updated Recommendations 1/2025](https://icmje.acponline.org/news-and-editorials/updated_recommendations_jan2025.html): tác giả chịu trách nhiệm về tính chính xác của tài liệu dẫn; cảnh báo tạp chí săn mồi.

## 10. Liên kết

- [[luat-viet-noi-dung]] — 10 luật nội dung + quy ước số/bảng/hình.
- [[quy-trinh-bao-cao-ctut]] — QĐ 345: bố cục chương, quy tắc ≥ 2 tiểu mục.
- [[prompt-lam-bao-cao]] — quy trình tạo file và chấm điểm trước khi nộp.
