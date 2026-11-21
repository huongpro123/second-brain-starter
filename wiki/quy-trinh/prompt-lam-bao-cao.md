---
title: "Prompt làm báo cáo — bản tổng hợp (copy nguyên khối)"
updated: 2026-11-21
status: active
tags: [quy-trinh, prompt, bao-cao]
sources:
  - "QĐ 345/QĐ-ĐHKTCN ngày 08/4/2025"
  - "Hướng dẫn trình bày báo cáo đồ án — Khoa Điện – Điện tử"
---

# Prompt làm báo cáo — bản tổng hợp

Một khối duy nhất để dán vào system prompt / `~/.claude/CLAUDE.md` / `~/.codex/AGENTS.md` / Custom Instructions.
Trước khi dán, **thay `<VAULT_DIR>` bằng đường dẫn thư mục repo này trên máy bạn** (nếu mở trực tiếp repo làm workspace thì dùng đường dẫn tương đối luôn).

## Prompt (copy nguyên khối)

```markdown
# Quy trình chuẩn khi làm báo cáo học thuật (CTUT)

Khi yêu cầu chạm tới: báo cáo, đồ án (ĐA1/2/3), NCKH, luận văn, KLTN, ĐATN, TTTN, bìa, Word,
format, in ấn, số liệu, kết quả, viết chương — bắt buộc làm đúng thứ tự sau, không tự bịa form:

1. Đọc `<VAULT_DIR>/AGENTS.md` (luật vault + thứ tự đọc note).
2. Đọc `<VAULT_DIR>/skills/bao-cao-ctut/SKILL.md` (quy trình + luật nội dung).
3. Đọc `<VAULT_DIR>/wiki/quy-trinh/quy-trinh-bao-cao-ctut.md` — chuẩn hiện hành
   **QĐ 345/QĐ-ĐHKTCN ngày 08/4/2025**; phân biệt rõ 3 loại: đồ án ≠ ĐATN/KLTN ≠ TTTN
   (bìa + màu bìa, in 1 hay 2 mặt, vị trí số trang, số trang tối thiểu, thứ tự front matter,
   tên chương — đều khác nhau). Riêng NCKH SV đọc thêm `wiki/quy-trinh/nckh-quy-che-sv04.md`.
4. Đọc `<VAULT_DIR>/wiki/quy-trinh/luat-viet-noi-dung.md` — cấm bịa số;
   `wiki/quy-trinh/quy-uoc-viet-van-khoa-hoc.md` — claim phải có evidence, tiểu mục ≥2 đoạn văn.
5. Tạo khung + bìa từ `<VAULT_DIR>`:
   `python tools/word/du-an-moi.py --loai <do-an|luan-van|nckh> --ten "..." --sv "..." --mssv "..." --lop "..." --gvhd "..." --out "./out/BaoCao.docx"`
   (tool điền bìa chính + bìa phụ + trang xác nhận, giữ field PAGE, xuất `bia-preview.png` nếu có LibreOffice + `CHECK-LIST.md`).
6. Chấm trước khi in: `python tools/word/kiem-tra.py <file.docx>` ≥90 (định dạng) và
   `python tools/word/kiem-tra-noi-dung.py <file.docx>` ≥90 (nội dung). Dưới 90 → sửa rồi chấm lại.
7. Bìa là ưu tiên số 1 — sai bìa thì giám khảo mất thiện cảm ngay. Luôn kiểm tra bìa
   (`bia-preview.png` hoặc mở PDF/Word xem trang 1) trước khi báo xong.
8. Thiếu dữ liệu thật → ghi dấu `[CẦN SỐ LIỆU: …]`, `[CẦN TRÍCH DẪN: …]`, `[?]` rồi hỏi lại chủ bài;
   tuyệt đối không đoán, không sinh số ảo.
9. Có văn bản/quy định mới của Trường hoặc Khoa → cập nhật note, ghi `skills/bao-cao-ctut/CHANGELOG.md`,
   tăng version skill, ghi `log.md`.
10. Cần bối cảnh dự án đang mở: đọc `index.md` của vault — đừng quét cả vault.
```

## Nơi dán gợi ý

| Nơi dán | Ghi chú |
|---|---|
| `~/.claude/CLAUDE.md` | Claude Code tự đọc mỗi phiên |
| `~/.codex/AGENTS.md` | Codex CLI tự đọc |
| Global rule / plugin của Antigravity hoặc Cursor | Dùng khi mở các repo code khác ngoài vault |
| Custom Instructions của ChatGPT / Gemini Web | Dán khối này và đính kèm file cần sửa |

## Vì sao 10 dòng này

- Dòng 1–4: **đọc trước khi làm** — tránh để agent tự đoán form sai chuẩn.
- Dòng 5: tool đã đóng gói bìa + trang xác nhận → không phải gõ tay từng dòng.
- Dòng 6: hai thang điểm 100 tách **định dạng** và **nội dung** — cái sau chống ảo giác.
- Dòng 7: bìa là thứ đầu tiên người chấm nhìn thấy.
- Dòng 8: cơ chế đánh dấu thay vì bịa — người viết điền số thật sau.
- Dòng 9: quy định học thuật có thể thay đổi giữa các năm học → luôn giữ đường dẫn kiểm tra lại.

## Liên quan

- [[quy-trinh-bao-cao-ctut]] — chuẩn QĐ 345 đầy đủ
- [[nckh-quy-che-sv04]] — quy chế SV04 cho NCKH sinh viên
- [[luat-viet-noi-dung]] — luật nội dung chống ảo giác
- [[quy-uoc-viet-van-khoa-hoc]] — claim–evidence, trích dẫn, văn phong kỹ thuật
- [[ky-nang-viet-word]] — lỗi hay gặp khi viết Word và cách khắc phục
