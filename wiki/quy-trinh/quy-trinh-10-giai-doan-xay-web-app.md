---
title: Quy trình 10 giai đoạn xây web/app (App Build Process)
updated: 2026-11-20
status: active
tags: [quy-trinh, software]
sources: []
---

# Quy trình 10 giai đoạn xây web/app

Dùng khi **xây sản phẩm mới** (website/app). Không dùng cho việc nhỏ — việc nhỏ đi [[quy-trinh-3-che-do]].
Nguyên tắc số 1: **không viết code khi chưa hiểu rõ yêu cầu, chưa có kế hoạch, chưa được xác nhận.**

## 10 giai đoạn (mỗi bước có cổng chuyển bước)
1. **Phân tích yêu cầu** → PRD + tính năng MVP + tiêu chí nghiệm thu. *Cổng: yêu cầu cốt lõi rõ, được xác nhận.*
2. **Kiến trúc** (frontend/backend/database/storage/auth/external services) — đơn giản, đúng quy mô. *Cổng: duyệt stack.*
3. **Database** (bảng, trường, quan hệ, khóa, ràng buộc, phân quyền, backup/migration). Ưu tiên Postgres/Supabase; file → storage riêng. *Cổng: duyệt schema.*
4. **Giao diện & UX** (trang, luồng, responsive, màu/font/component, loading/lỗi/empty). *Cổng: duyệt thiết kế.*
5. **Thiết lập dự án** (git + GitHub khi được phép, cấu trúc thư mục, README, .gitignore, .env.example, lint/format). Không viết cả app trong 1 file.
6. **Code từng chức năng theo MVP** — mỗi chức năng: mục tiêu → file → ảnh hưởng → code → kiểm tra → sửa → nghiệm thu → báo cáo → commit.
7. **Bảo mật** — không key trong code, không đẩy .env, kiểm quyền backend/DB, validate input, chống SQLi/XSS/CSRF, session, rate limit, log không lộ dữ liệu, quyền tối thiểu; dữ liệu cá nhân → rà soát pháp lý VN.
8. **Kiểm thử** — unit/integration/e2e/permission/responsive/error/performance/backup-restore. "Chạy được" ≠ "hoàn thiện".
9. **Triển khai** — hosting, domain/HTTPS, env vars, DB production, migration, backup, log/giám sát, rollback, CI/CD, test lại. Không dùng dữ liệu thật cho thao tác phá hủy; **không tự deploy production khi chưa được phép**.
10. **Bảo trì** — lỗi, hiệu năng, backup, cập nhật thư viện, phản hồi, tính năng mới, tài liệu, phục hồi.

## Báo cáo sau mỗi giai đoạn (7 mục)
GIAI ĐOẠN / 1 Mục tiêu / 2 Đã thực hiện / 3 Kết quả kiểm tra (cách xác minh) / 4 Vấn đề tồn tại / 5 Điều kiện chuyển bước / 6 Bước tiếp theo / 7 Trạng thái (CHƯA BẮT ĐẦU · ĐANG THỰC HIỆN · CHỜ XÁC NHẬN · ĐÃ HOÀN THÀNH).

## Bắt đầu dự án mới
B1 → kiểm tra tài liệu/code sẵn có → hỏi từng nhóm câu ngắn → đề xuất MVP → đề xuất lộ trình → **chờ xác nhận** → mới thiết kế/code.

## Liên kết
[[quy-trinh-3-che-do]] · [[quyen-han-agent]] · [[quy-trinh-github-spec-kit]]