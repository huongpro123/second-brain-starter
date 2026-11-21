# Skills & Tích hợp Agent

Thư mục này chứa các **Agent Skills** chuẩn bị sẵn quy trình + công cụ đi kèm để AI agent đọc và làm đúng ngay từ đầu.

## Danh sách skill

| Skill | Mục đích | Phiên bản | Chi tiết |
|---|---|---|---|
| `bao-cao-ctut/` | Báo cáo Đồ án / ĐATN-KLTN / TTTN / NCKH chuẩn CTUT (**QĐ 345/2025** & **QĐ 886/2022 SV04**) + bộ tool Word + luật chống ảo giác | **1.5.1** | [SKILL.md](bao-cao-ctut/SKILL.md) · [CHANGELOG.md](bao-cao-ctut/CHANGELOG.md) |

---

## Cách kết nối cho từng AI Agent

### 1. Mở trực tiếp repo này làm workspace (đơn giản nhất)

- **Antigravity / Cursor / Claude Code / Codex CLI:** chỉ cần mở thư mục root của repo này.
- Agent sẽ tự nhìn thấy [AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md) và gọi skill [bao-cao-ctut/SKILL.md](bao-cao-ctut/SKILL.md) khi làm báo cáo.

### 2. Dùng toàn cục ở các dự án khác (khi repo code nằm ở thư mục riêng)

Thay `<VAULT_DIR>` bằng đường dẫn thực tế tới bản clone repo này trên máy bạn (ví dụ `D:\second-brain` hoặc `~/second-brain`):

- **Claude Code:** gắn nội dung trong `wiki/quy-trinh/prompt-lam-bao-cao.md` vào `~/.claude/CLAUDE.md` (thay `<VAULT_DIR>` bằng đường dẫn thật), hoặc symlink thư mục skill:
  ```powershell
  New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\bao-cao-ctut" -Target "<VAULT_DIR>\skills\bao-cao-ctut"
  ```
- **Codex CLI:** gắn khối prompt vào `~/.codex/AGENTS.md` hoặc `~/.codex/skills/`.
- **Antigravity:** tạo rule/skill trỏ tới `<VAULT_DIR>\AGENTS.md` và `<VAULT_DIR>\skills\bao-cao-ctut\SKILL.md`.
- **ChatGPT / Gemini / Claude Web (Custom Instructions):** copy khối trong `wiki/quy-trinh/prompt-lam-bao-cao.md` (giữ những phần phù hợp hoặc đính kèm file `.md` liên quan khi hỏi).
