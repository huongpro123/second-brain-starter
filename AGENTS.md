# Bộ luật của bộ não thứ hai

File này áp dụng cho **mọi công cụ AI agent** (Claude Code, Codex, Gemini CLI, Antigravity, Cursor…). Khi mở workspace này, đọc file này trước khi làm bất cứ việc gì.

---

## 0. Khi làm báo cáo / đồ án / luận văn / NCKH / Word

Khi yêu cầu chạm tới *báo cáo, đồ án (ĐA1/2/3), NCKH, luận văn, KLTN, ĐATN, TTTN, bìa, Word, format, in ấn, số liệu, kết quả, viết chương* → đọc theo đúng thứ tự:

1. `skills/bao-cao-ctut/SKILL.md` — quy trình tạo bìa, xuất ảnh xem trước, chấm điểm ≥90 trước khi nộp.
2. `wiki/quy-trinh/quy-trinh-bao-cao-ctut.md` — chuẩn **QĐ 345/QĐ-ĐHKTCN 08/4/2025** + hướng dẫn Đồ án (riêng NCKH SV xem `wiki/quy-trinh/nckh-quy-che-sv04.md`).
3. `wiki/quy-trinh/luat-viet-noi-dung.md` — luật **chống ảo giác** (không số liệu thật = không viết số nào) và `wiki/quy-trinh/quy-uoc-viet-van-khoa-hoc.md` (claim phải có evidence).

---

## 1. Thứ tự đọc (tiết kiệm token)

1. Đọc `index.md` trước để tìm đúng note cần mở.
2. Chỉ mở **đúng 1–3 note liên quan** tới việc đang làm.
3. **Không** đọc cả vault, **không** đọc hết `raw/` khi chưa cần.
4. Nếu thông tin ở note khác với code thật trong repo dự án → **code/tài liệu gốc là chuẩn**, cập nhật lại note kèm lý do.

---

## 2. Hai lớp dữ liệu

| Thư mục | Bản chất | Agent được làm |
|---|---|---|
| `raw/` | Nguồn thô (bài viết, PDF, transcript, log) | **CHỈ ĐỌC VÀ TRÍCH DẪN**. Không tự sửa nguồn thô. |
| `wiki/` | Bản đã tiêu hoá (1 chủ đề = 1 note `.md`) | Đọc, tạo mới, cập nhật, gắn link chéo. |

Mọi kết luận quan trọng phải **ghi nguồn**: trỏ về file trong `raw/` hoặc đường dẫn ngoài kèm ngày.

---

## 3. Khi trả lời hoặc tạo kiến thức mới

Sau một phiên làm việc có kết luận tái dùng được ở phiên sau (quyết định thiết kế, bẫy đã gặp, số đo chuẩn, lệnh hay dùng):

1. Hỏi xem nội dung đó thuộc note đã có chưa → có thì cập nhật; chưa thì tạo note mới trong `wiki/` theo mẫu `templates/note.md` (hoặc chạy `tools/new-note.ps1`).
2. Thêm link vào `index.md` (không để note mồ côi).
3. Gắn link `[[ten-note]]` tới 2–3 note liên quan.
4. Thêm 1 dòng vào `log.md`: `YYYY-MM-DD — <agent> — <việc gì> — vì sao`.

Không ghi vào vault các cuộc hỏi đáp vặt hoặc log thô không có giá trị tái dùng.

---

## 4. Định dạng mỗi note trong `wiki/`

Mọi note bắt đầu bằng frontmatter:

```yaml
---
title: Tên ngắn gọn
updated: YYYY-MM-DD
status: active   # active | draft | stale | done
tags: [chu-de]
sources: []
---
```

Ngay dưới frontmatter là 1 đoạn 1–3 câu: *note này trả lời câu hỏi gì, dùng khi nào*. Nếu là bản nháp chưa kiểm chứng thì đặt `status: draft`.

---

## 5. Quy tắc đặt tên & thư mục

- Tên file: `kebab-case`, không dấu tiếng Việt, không khoảng trắng (`quy-trinh-3-che-do.md`).
- Dùng wikilink Obsidian `[[ten-file-khong-can-duoi]]`.
- Thư mục con trong `wiki/`: `du-an/` (đồ án, sản phẩm), `he-thong/` (máy, tool, môi trường), `con-nguoi/` (hồ sơ, định hướng), `quy-trinh/` (cách làm lặp lại), `y-tuong/` (kiến thức nền, so sánh).

---

## 6. Luật cứng (vi phạm = hỏng vault)

1. **Không bịa kết nối.** Không chắc có liên quan thì đừng link.
2. **Không tự động tóm tắt lại những thứ đã rõ chỉ để tỏ ra bận rộn.** Ít chữ mà đúng > dài mà thừa.
3. **Không bịa số liệu, không bịa kết quả, không kể chuyện không xảy ra** — xem `wiki/quy-trinh/luat-viet-noi-dung.md`.
4. **Không ghi đè kiến thức đã kiểm chứng** bằng suy đoán từ cuộc trò chuyện mới — nếu thấy mâu thuẫn, ghi rõ `[MÂU THUẪN: note cũ nói X, thực tế Y]` để chủ vault xử lý.
5. **Không đưa bí mật vào vault** (mật khẩu, API key, token, thông tin riêng tư của người khác).
6. **Số liệu phải kèm bối cảnh đo** (mẫu, điều kiện, ngày, số lần chạy).

---

## 7. Bảo trì

Chạy định kỳ bằng PowerShell từ thư mục gốc của vault:

```powershell
powershell -ExecutionPolicy Bypass -File tools\health-check.ps1
```

Script báo: note mồ côi (không có trong `index.md`), link gãy (`[[...]]` trỏ sai tên), note cũ quá 60 ngày chưa kiểm lại, frontmatter thiếu.

Khi `health-check` báo note cũ: **không tự sửa nội dung**. Đọc lại, xác minh với thực tế rồi mới cập nhật `updated` và ghi phần đã đổi.

---

## 8. Quy trình dự án

Trước khi bắt đầu bất kỳ dự án hoặc task lập trình mới nào:

1. Đọc `wiki/quy-trinh/quy-trinh-3-che-do.md` để chọn đúng chế độ (**Vibe** / **Spike** / **Spec**).
2. Khi xây website/app mới: đi theo `wiki/quy-trinh/quy-trinh-10-giai-doan-xay-web-app.md` (B1–B10, chốt từng cổng trước khi code).
3. Theo ranh giới hành động ở `wiki/quy-trinh/quyen-han-agent.md` (A: làm luôn · B: xin phép · C: cấm).
4. Dự án lớn nhiều bước → tham khảo `wiki/quy-trinh/quy-trinh-github-spec-kit.md`.
5. Định kỳ review quy trình mỗi 2 tuần theo `wiki/quy-trinh/do-hieu-qua-workflow.md`.
6. Quản lý danh sách dự án đang mở tại `index.md` và thư mục `wiki/du-an/`.
