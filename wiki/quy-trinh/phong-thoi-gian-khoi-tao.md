---
title: Phòng Thời Gian — Khởi tạo & nạp toàn bộ kiến thức cho agent mới
updated: 2026-11-21
status: active
tags: [quy-trinh, onboarding, agent, setup]
sources:
  - "[[AGENTS]]"
  - "[[quy-trinh-3-che-do]]"
  - "[[quyen-han-agent]]"
  - "[[quy-trinh-bao-cao-ctut]]"
---

# Phòng Thời Gian — Khởi tạo & nạp kiến thức trong 1 lượt

> **Mục tiêu:** Đưa một AI agent hoàn toàn trắng vào trạng thái "thuộc toàn bộ luật chơi, đã kiểm đủ công cụ, hiểu đúng chủ vault" chỉ trong **15–30 phút setup** thay vì phải chỉnh sửa qua hàng chục phiên làm việc.

---

## Pha 1: Dựng & kiểm tra môi trường (tự động bằng 1 lệnh)

Chạy script khởi tạo đa nền tảng ngay tại thư mục gốc của vault:

```powershell
python tools/setup.py
```

*(Nếu chỉ muốn kiểm tra không cài thêm gì: `python tools/setup.py --check`.)*

Script sẽ tự động:
1. Tạo môi trường ảo `.venv` và cài `requirements.txt` (`python-docx`, `pillow`, `pymupdf`, và `pywin32` nếu là Windows).
2. Bật `.githooks/pre-commit` để chặn commit nhầm API key / private key và kiểm tra link vault khi sửa `wiki/`.
3. Chạy `tools/health-check.ps1` (phải ra `Vault sạch`) và `tools/word/cham-loat.py templates/word` (các mẫu phải đạt `100/100`).
4. In ra **khối Prompt toàn cục** đã điền sẵn đường dẫn thật trên máy hiện tại để gắn vào Claude Code / Codex / Cursor / Antigravity.

**Lưu ý phần mềm ngoài repo:** Nếu máy chưa có **Microsoft Word desktop**, **LibreOffice**, **Git** hoặc **Obsidian**, agent cần **xin phép chủ máy (mục B trong [[quyen-han-agent]])** hoặc hướng dẫn người dùng tự cài.

---

## Pha 2: Nạp 5 trụ cột kinh nghiệm cốt lõi (đọc tuần tự 1 lượt)

Agent mới đọc đúng 5 nhóm tài liệu dưới đây để nắm trọn kinh nghiệm đã chưng cất — **không đọc lan man**:

1. **Tư duy trí nhớ 2 lớp (`raw/` vs `wiki/`):** [[obsidian-second-brain]] — hiểu vì sao chỉ đọc `index.md` → mở đúng note, tránh context rot.
2. **Kỷ luật dự án & phân quyền:** [[quy-trinh-3-che-do]] + [[quyen-han-agent]] — chọn đúng chế độ Vibe / Spike / Spec, trả lời DoR 5 câu trước khi đụng dự án vừa, giữ ranh giới A/B/C/D.
3. **Làm web/app & quản lý repo lớn:** [[quy-trinh-10-giai-doan-xay-web-app]] + [[quy-trinh-github-spec-kit]] — đi theo cổng xác nhận, mỗi việc một nhánh/PR, tránh commit file nhị phân > 50 MB.
4. **Chuẩn báo cáo CTUT & bẫy kỹ thuật Word:** `skills/bao-cao-ctut/SKILL.md` + [[quy-trinh-bao-cao-ctut]] + [[nckh-quy-che-sv04]] + [[ky-nang-viet-word]] — nắm rõ khác biệt 4 loại văn bản (Đồ án 2 mặt / ĐATN 1 mặt số trên / TTTN / NCKH SV04 Mẫu 1–3), 13 điểm hay sai theo QĐ 345/2025 và bẫy xuất PDF Word COM vs LibreOffice.
5. **Chống ảo giác & phản biện đối nghịch:** [[luat-viet-noi-dung]] + [[quy-uoc-viet-van-khoa-hoc]] + `skills/phan-bien-bao-cao/SKILL.md` — cấm bịa số/nguồn, thiếu số ghi `[CẦN SỐ LIỆU: …]`, và biết cách tự phản biện trước khi nộp.

---

## Pha 3: Phỏng vấn 4 câu để cá nhân hóa Vault (chỉ hỏi khi mới clone)

Nếu thấy `wiki/con-nguoi/ho-so-mau.md` vẫn còn placeholder (`[Điền tên của bạn]`), agent hỏi chủ vault ngắn gọn **1 lượt 4 câu**:

1. **Bạn tên gì, đang học/làm ở ngành hoặc lĩnh vực nào?**
2. **1–3 mục tiêu chính trong 3–6 tháng tới là gì?**
3. **Bạn đang chạy những dự án/đồ án nào cần theo dõi thường xuyên (tên + thư mục/repo nếu có)?**
4. **Bạn thích agent giao tiếp kiểu nào (ngôn ngữ, độ ngắn gọn, quy tắc riêng cần tránh)?**

Sau khi người dùng trả lời → agent cập nhật `wiki/con-nguoi/ho-so-mau.md` (hoặc tạo `ho-so.md` riêng, sửa link trong `index.md`), tạo note dự án trong `wiki/du-an/`, cập nhật `wiki/he-thong/moi-truong-va-agent.md`, rồi chạy `powershell -ExecutionPolicy Bypass -File tools\health-check.ps1` xác nhận **0 mồ côi · 0 link gãy**.

---

## Pha 4: Bài test "tốt nghiệp Phòng Thời Gian" (chứng minh đã sẵn sàng)

Trước khi báo *"Đã setup xong"*, agent kiểm tra đủ 4 tiêu chí:

- [ ] `tools/setup.py` (hoặc `--check`) chạy qua với bộ mẫu Word **100/100** và `health-check.ps1` báo **Vault sạch**.
- [ ] Đã có thông tin chủ vault + ít nhất 1 note dự án (hoặc giữ mẫu nếu chủ vault muốn tự điền sau).
- [ ] Đã in/gắn xong đường dẫn vault thật cho agent toàn cục (`skills/README.md`).
- [ ] Khi thử hỏi: *"Tóm tắt khác nhau giữa Đồ án và NCKH SV04"* hoặc *"Tạo thử 1 bìa báo cáo mẫu"*, agent trả lời đúng ngay không cần tra mò.

## Liên quan

- [[ho-so-mau]]
- [[moi-truong-va-agent]]
- [[obsidian-second-brain]]
- [[do-hieu-qua-workflow]]
