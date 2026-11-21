---
title: Quyền hạn agent — việc nào được làm luôn, việc nào phải xin phép
updated: 2026-11-21
status: active
tags: [quy-trinh, agent]
sources: []
---

# Quyền hạn agent

Khung phân quyền giúp làm việc nhanh với AI agent nhưng vẫn giữ an toàn cho code, dữ liệu và hệ thống.

## A. ĐƯỢC LÀM LUÔN (báo sau, không cần hỏi)
- Đọc file/repo/log, grep/search; clone/fetch **read-only**
- Chạy test, build, lint, script kiểm tra
- Tạo/sửa file trong workspace/vault
- Cài thư viện **user-scope** (trong virtualenv hoặc user profile)
- Tạo nhánh mới (không push main), commit local
- Truy vấn dữ liệu công khai

## B. PHẢI XIN PHÉP (một lần, rồi làm)
- `git push` lên nhánh chính (`main`/`master`) / force push / xoá nhánh từ xa
- Xoá/đổi tên nhiều file, `git reset --hard`, `git revert`
- Cài phần mềm **cần quyền quản trị (UAC / sudo)**
- Đổi cấu hình hệ thống (registry, mạng, firewall, phân vùng)
- Tiêu tiền, đăng ký dịch vụ, gửi email/tin nhắn ra ngoài
- Xuất dữ liệu nội bộ/nhóm ra dịch vụ công khai
- Sửa vùng cấu hình cốt lõi hoặc dữ liệu chuẩn của dự án nhóm

## C. KHÔNG BAO GIỜ (trừ chỉ đạo rõ bằng văn bản)
- Format/xoá ổ, đổi phân vùng
- Đưa dữ liệu thật của khách hàng/nhóm/giảng viên lên dịch vụ ngoài khi chưa được duyệt
- Crack, bẻ license, dùng phần mềm vi phạm bản quyền
- Sửa code đang chạy lab/production mà không có người duyệt
- Bịa số liệu/kết quả thực nghiệm (xem [[luat-viet-noi-dung]])

## D. Gom thao tác cần quyền cao
Nhiều việc thuộc mục B cùng lúc → gom vào **1 script chạy 1 lần xác nhận**, không bật hộp thoại quyền lẻ tẻ từng việc.

## Liên kết
[[quy-trinh-3-che-do]] · [[quy-trinh-10-giai-doan-xay-web-app]]
