---
title: Bộ não thứ hai cho agent — trào lưu và cách hiểu đúng
updated: 2026-11-21
status: active
tags: [y-tuong, pattern, memory, agent]
sources: []
---

# "Bộ não thứ hai" cho agent

Ghi lại bản chất của mô hình vault Markdown kết hợp AI agent để khỏi tốn công tra lại hoặc dùng sai cách.

## 1. Gốc gác

| Mốc | Chuyện gì |
|---|---|
| 4/2026 | **Andrej Karpathy** mô tả pattern **"LLM Wiki"**: tách tài liệu thô vào `raw/`, để LLM biên dịch thành wiki Markdown liên kết chéo. |
| 2026 | Nhiều cộng đồng đóng gói lại thành workflow kết hợp **Claude Code / Cursor / Codex + Obsidian**. |

## 2. Nó giải ba vấn đề gì

1. **Mất trí nhớ giữa các phiên.** Context window reset sau mỗi phiên chat → mọi quyết định, lý do, lỗi đã gặp biến mất nếu không lưu xuống file.
2. **Rối loạn ngữ cảnh (Context rot).** Nhồi nhiều tài liệu thô *làm giảm* chất lượng suy luận và tốn token. Chia tầng `index.md` → `wiki/` giúp agent nạp đúng 1–3 note chất lượng cao.
3. **Đứt gãy thực thi.** AI sinh text nhưng không nối vào quy trình làm việc. Khi đặt `AGENTS.md` + `skills/` + `tools/` ngay trong vault, agent vừa đọc tri thức vừa chạy công cụ kiểm chứng.

## 3. Kiến trúc cốt lõi

```text
raw/                  ← nguồn thô (PDF, bài viết, transcript). Chỉ trích dẫn, KHÔNG đọc bừa.
wiki/                 ← bản chưng cất: 1 chủ đề = 1 file .md, [[link]] chéo, bám index.md.
AGENTS.md / CLAUDE.md ← bộ luật đọc/ghi và thứ tự tra cứu cho agent.
tools/                ← script kiểm tra sức khỏe vault (health-check) + công cụ đặc thù.
```

Giá trị thật: **nén một lần, tái dùng nhiều lần** → giảm token, tăng nhất quán.

## 4. Hiểu nhầm phổ biến: "cho agent đọc hết cả ổ đĩa"

**Sai.** Vault là thư mục **nhỏ, có chọn lọc**:

- Nhiễu từ `node_modules/`, file nháp, log rác sẽ phá chất lượng câu trả lời.
- **Obsidian chỉ là giao diện xem cho người.** Bản chất vẫn là các file `.md` thuần; VS Code, Cursor, Claude Code, Codex hay script PowerShell/Python đều đọc ghi trực tiếp không phụ thuộc app.
- Nếu cài Obsidian, chỉ cần chọn *"Open folder as vault"* trỏ tới `<VAULT_DIR>` — giao diện tím khói trong `.obsidian/` tự được kích hoạt.

Muốn agent tìm trong hàng chục nghìn file lộn xộn thì đó là bài toán **RAG/search index**, khác với một **Second Brain** đã qua chưng cất và kiểm chứng.

## 5. Khi nào đáng dùng

| Đáng | Không đáng |
|---|---|
| Công việc lặp lại, nhiều phiên, dùng nhiều agent | Việc lặt vặt làm một lần rồi bỏ |
| Quyết định kỹ thuật có lý do cần nhớ về sau | Chỉ tra cứu cú pháp tài liệu công khai |
| Nhiều dự án song song dễ lẫn bối cảnh | Dự án đơn lẻ, code tự nói hết mọi thứ |
| Cần giữ bằng chứng/số liệu và checklist chuẩn | Không có nhu cầu xem lại |

## Liên quan

- [[moi-truong-va-agent]]
- [[ho-so-mau]]
- [[quy-trinh-3-che-do]]
