---
title: Môi trường máy và cấu hình agent (mẫu)
updated: 2026-11-21
status: active
tags: [he-thong, moi-truong, agent]
sources: []
---

# Môi trường máy và cấu hình agent

Ghi lại đường dẫn công cụ, môi trường Python/Git và cách nối vault với từng AI agent để chuyển máy mới không phải tìm lại từ đầu.

## 1. Vị trí vault & công cụ chính

- **Thư mục vault (`<VAULT_DIR>`):** đường dẫn nơi bạn clone repo này.
- **Python venv:** dùng môi trường ảo (`.venv`) + `pip install -r requirements.txt`.
- **Git / GitHub CLI (`gh`):** dùng nhánh riêng cho mỗi đầu việc (`[[quy-trinh-github-spec-kit]]`).
- **Word / LibreOffice:**
  - Bộ chấm định dạng & tạo bìa (`du-an-moi.py`, `kiem-tra.py`, `kiem-tra-noi-dung.py`) chạy đa nền tảng chỉ cần `python-docx`.
  - Xuất PDF chuẩn trang in bằng Word thật (`word-hoan-tat.py`) cần Windows + Microsoft Word desktop + `pywin32`.

## 2. Nối vault với các AI agent

- **Mở trực tiếp thư mục vault làm workspace:** agent sẽ tự đọc `AGENTS.md` / `CLAUDE.md` và skill `skills/bao-cao-ctut/SKILL.md`.
- **Dùng toàn cục từ repo khác:** xem hướng dẫn tại [skills/README.md](../../skills/README.md) và khối prompt mẫu ở [[prompt-lam-bao-cao]].

## 3. Lệnh kiểm tra bảo trì vault

```powershell
powershell -ExecutionPolicy Bypass -File tools\health-check.ps1
```

## Liên quan

- [[obsidian-second-brain]]
- [[ho-so-mau]]
- [[quy-trinh-github-spec-kit]]
