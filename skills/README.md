# Skills & Tích hợp Agent

Thư mục này chứa các **Agent Skills** chuẩn bị sẵn quy trình + công cụ đi kèm để AI agent đọc và làm đúng ngay từ đầu.

## Danh sách skill

| Skill | Mục đích | Phiên bản | Chi tiết |
|---|---|---|---|
| `bao-cao-ctut/` | Báo cáo Đồ án / ĐATN-KLTN / TTTN / NCKH chuẩn CTUT (**QĐ 345/2025** & **QĐ 886/2022 SV04**) + bộ tool Word + luật chống ảo giác | **1.5.1** | [SKILL.md](bao-cao-ctut/SKILL.md) · [CHANGELOG.md](bao-cao-ctut/CHANGELOG.md) |
| `phan-bien-bao-cao/` | Kiểm chứng đối nghịch (Adversarial Verification): đóng vai Hội đồng phản biện soi sai lệch số liệu, trích dẫn treo, lỗ hổng thực nghiệm trước khi nộp | **1.0.0** | [SKILL.md](phan-bien-bao-cao/SKILL.md) |

---

## Cách kết nối cho từng AI Agent

### 1. Mở trực tiếp repo này làm workspace (đơn giản nhất)

- **Antigravity / Cursor / Claude Code / Codex CLI:** mở thư mục root của repo này.
- Nếu là lần đầu: chạy `python tools/setup.py` hoặc yêu cầu agent đọc [AGENTS.md](../AGENTS.md) và làm theo luồng **Phòng Thời Gian** (`wiki/quy-trinh/phong-thoi-gian-khoi-tao.md`).

### 2. Dùng toàn cục ở các dự án khác (khi repo code nằm ở thư mục riêng)

Chạy `python tools/setup.py --check` ngay trong repo để in sẵn đoạn cấu hình đã điền đúng đường dẫn máy bạn (`<VAULT_DIR>`), sau đó gắn vào:

- **Claude Code:** dán vào `~/.claude/CLAUDE.md`, hoặc symlink hai skill sang `~/.claude/skills/`:
  ```powershell
  New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\bao-cao-ctut" -Target "<VAULT_DIR>\skills\bao-cao-ctut"
  New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\phan-bien-bao-cao" -Target "<VAULT_DIR>\skills\phan-bien-bao-cao"
  ```
- **Codex CLI:** gắn khối cấu hình vào `~/.codex/AGENTS.md` hoặc `~/.codex/skills/`.
- **Antigravity:** tạo global rule/plugin trỏ tới `<VAULT_DIR>\AGENTS.md`, `<VAULT_DIR>\skills\bao-cao-ctut\SKILL.md` và `<VAULT_DIR>\skills\phan-bien-bao-cao\SKILL.md`.
- **ChatGPT / Gemini / Claude Web (Custom Instructions):** copy khối trong `wiki/quy-trinh/prompt-lam-bao-cao.md` và đính kèm file cần rà soát.
