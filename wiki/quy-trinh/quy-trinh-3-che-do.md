---
title: Quy trình 3 chế độ — Vibe / Spike / Spec
updated: 2026-11-20
status: active
tags: [quy-trinh, agent]
sources: []
---

# Quy trình 3 chế độ — Vibe / Spike / Spec

Trả lời câu hỏi: **việc này làm ngay hay phải rào trước?** Nguyên tắc: rào **quyết định**, không rào **tìm hiểu**.

## Ba chế độ

| Chế độ | Khi nào | Làm gì | Giới hạn |
|---|---|---|---|
| **Vibe** | Rõ ràng, reversible, 1–2 file | Làm ngay, chạy kiểm, ghi log | ≤ 2 giờ |
| **Spike** | Chưa chắc cách làm, cần thử để ra quyết định | Đặt câu hỏi + giới hạn thời gian, prototype nháp, ghi kết luận | 15–60 phút |
| **Spec** | Nhiều tuần, nhiều người, khó đảo ngược (an toàn, điểm số) | Đủ 6 tài liệu + DoR + duyệt rồi mới code | theo dự án |

Chuyển chế độ: Vibe/Spike phát sinh lớn → dừng, chuyển Spec. Spec thấy phần rõ → tách task Vibe nhỏ.

## Definition of Ready — 5 câu (bản Lite)
Trả lời được 5 câu là được làm (task vừa):
1. Mục tiêu **đo được**?
2. **Không làm** gì (ngoài phạm vi)?
3. Rủi ro lớn nhất + cách giảm?
4. Task nhỏ nhất để bắt đầu?
5. Ai duyệt / xác nhận xong?

Chỉ dự án nhiều tuần / có người thứ 2 mới cần 6 tài liệu: `PRD · ARCHITECTURE · DESIGN · RULES · TASKS · PROGRESS`.

## Definition of Done
- [ ] Chạy/test thật qua (bằng chứng, không tin báo cáo suông)
- [ ] Đúng phạm vi, không lấn "ngoài phạm vi"
- [ ] Cập nhật PROGRESS/log
- [ ] Người duyệt xác nhận

## Liên kết
[[quy-trinh-10-giai-doan-xay-web-app]] · [[quyen-han-agent]] · [[do-hieu-qua-workflow]]