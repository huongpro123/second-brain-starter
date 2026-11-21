---
title: Quy trình GitHub + Spec Kit cho dự án phần mềm
updated: 2026-11-21
status: active
tags: [quy-trinh, tool, github]
sources: []
---

# Quy trình GitHub + Spec Kit

Quy ước dùng Git/GitHub và Spec Kit (`specify-cli`) cho các dự án nhiều bước để tránh mất kiểm soát nhánh và tài liệu.

## 1. Công cụ gợi ý
- **Git** + **GitHub CLI (`gh`)** đã đăng nhập tài khoản cá nhân để tạo PR/clone nhanh.
- **Spec Kit CLI (`specify`)** (tùy chọn cho dự án lớn, cài qua `uv tool install specify-cli` hoặc `pipx`).

## 2. Khi nào dùng Spec Kit
- Dự án **lớn / nhiều bước** cần đi tuần tự `spec → plan → tasks → implement → converge`.
- Lệnh khởi tạo: `specify init <thu-muc> --integration <claude|codex|copilot|vibe>`
- Quy trình trong phiên chat: `/speckit-constitution` → `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` → `/speckit-converge`
- Mở rộng hữu ích: `specify extension add bug` (sửa lỗi có quy trình), `specify extension add assess` (đánh giá ý tưởng).
- Nếu agent chưa có integration sẵn → chạy `specify init` rồi yêu cầu agent đọc `.specify/`.

## 3. Quy tắc Git & bảo vệ repo
- Vùng an toàn của dự án nhóm: phân quyền rõ người có quyền duyệt/merge.
- Mỗi việc = một nhánh = một PR; push cuối buổi; tạo PR nháp từ sớm để dễ review.
- Không push trực tiếp lên `main` khi chưa kiểm tra hoặc chưa được duyệt (xem [[quyen-han-agent]]).
- File nhị phân lớn (>50 MB như video, dữ liệu đo thô, bản build): tránh commit trực tiếp vào Git — dùng `.gitignore`, Git LFS hoặc lưu tách ngoài repo.

## Liên kết
[[quy-trinh-3-che-do]] · [[moi-truong-va-agent]] · [[quyen-han-agent]]
