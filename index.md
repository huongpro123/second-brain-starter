# Bản đồ bộ não thứ hai

> Đọc file này đầu tiên để tìm đúng note, không đọc cả vault.
> Luật dùng vault: [AGENTS.md](AGENTS.md) · Tóm tắt: [CLAUDE.md](CLAUDE.md) · Nhật ký: [log.md](log.md)

> [!tip] Mới cài cho agent trắng? (Phòng Thời Gian)
> Mở [[phong-thoi-gian-khoi-tao]] và chạy `python tools/setup.py` để tự dựng `.venv`, bật `.githooks`, kiểm thử bộ mẫu và phỏng vấn cá nhân hóa vault trong một lượt.

---

## 👤 Con người

| Note | Nội dung | Trạng thái |
|---|---|---|
| [[ho-so-mau]] | Mẫu hồ sơ chủ vault: mục tiêu, dự án chính, thói quen làm việc | active |

---

## 🚀 Dự án

| Note | Nội dung | Trạng thái |
|---|---|---|
| [[du-an-mau]] | Mẫu ghi chú 1 trang cho một dự án (mục tiêu, trạng thái, nợ kỹ thuật) | active |

---

## ⚙️ Hệ thống & môi trường

| Note | Nội dung | Trạng thái |
|---|---|---|
| [[moi-truong-va-agent]] | Mẫu ghi công cụ cài sẵn, đường dẫn cục bộ và cấu hình AI agent | active |

---

## 📋 Quy trình & skill

| Chủ đề / Note | Nội dung | Trạng thái |
|---|---|---|
| [[phong-thoi-gian-khoi-tao]] | **Phòng Thời Gian:** luồng setup 1 lệnh + nạp toàn bộ kiến thức + phỏng vấn 4 câu cho agent mới | active |
| [[quy-trinh-3-che-do]] | Chọn chế độ **Vibe / Spike / Spec** + DoR 5 câu + DoD | active |
| [[quyen-han-agent]] | Ma trận quyền A (làm luôn) · B (xin phép) · C (không bao giờ) · D (gom thao tác) | active |
| [[quy-trinh-10-giai-doan-xay-web-app]] | 10 bước xây sản phẩm phần mềm, chốt cổng & báo cáo 7 mục | active |
| [[quy-trinh-github-spec-kit]] | Quy tắc nhánh/PR và luồng Spec Kit cho dự án lớn | active |
| [[do-hieu-qua-workflow]] | Chỉ số review workflow mỗi 2 tuần | active |
| [[quy-trinh-bao-cao-ctut]] | Quy trình + định dạng chuẩn **QĐ 345/QĐ-ĐHKTCN 08/4/2025**: lề, font, 3 loại báo cáo | active |
| [[nckh-quy-che-sv04]] | NCKH sinh viên — **QĐ 886/2022**, form **SV04** (Mẫu 1–3, 50–100 trang, 3 chương) | active |
| [[luat-viet-noi-dung]] | 10 luật **chống ảo giác** khi viết báo cáo: không bịa số, không bịa nguồn | active |
| [[quy-uoc-viet-van-khoa-hoc]] | Claim–evidence, trích dẫn IEEE, tránh văn kể chuyện, tiểu mục ≥ 2 đoạn | active |
| [[prompt-lam-bao-cao]] | Prompt 10 dòng để gắn vào system prompt của bất kỳ AI agent nào | active |
| [[quy-trinh-ve-ky-thuat-va-web]] | **Vẽ kỹ thuật & Web:** AutoCAD DXF/LISP, Revit (`pyRevit`/MCP), BIMvision (`IFC`/Bridge), Draw.io/Excalidraw/SVG | active |
| Skill `bao-cao-ctut` | [skills/bao-cao-ctut/SKILL.md](skills/bao-cao-ctut/SKILL.md) — `v1.5.1`: quy trình tạo bìa & kiểm báo cáo | active |
| Skill `phan-bien-bao-cao` | [skills/phan-bien-bao-cao/SKILL.md](skills/phan-bien-bao-cao/SKILL.md) — `v1.0.0`: kiểm chứng đối nghịch trước khi nộp | active |
| Skill `ve-ky-thuat-va-web` | [skills/ve-ky-thuat-va-web/SKILL.md](skills/ve-ky-thuat-va-web/SKILL.md) — `v1.1.0`: vẽ AutoCAD, Revit, BIMvision & sơ đồ web | active |

---

## 💡 Ý tưởng & phương pháp

| Note | Nội dung | Trạng thái |
|---|---|---|
| [[obsidian-second-brain]] | Giải phẫu kiến trúc "LLM Wiki" / Second Brain và khi nào nên dùng | active |
| [[ky-nang-viet-word]] | Phân tích lỗi hay gặp khi viết báo cáo Word và cách khắc phục | active |

---

## 📎 Mẫu & công cụ có sẵn

| Nhóm | Thành phần | Đường dẫn |
|---|---|---|
| Khởi tạo nhanh | `setup.py`, `setup.ps1` (Phòng Thời Gian) + `.githooks/pre-commit` | `tools/` · `.githooks/` |
| Công cụ Vault | `health-check.ps1`, `new-note.ps1`, `push-vault.ps1` | `tools/` |
| Mẫu note | Frontmatter chuẩn của vault | `templates/note.md` |
| Mẫu Word Đồ án | `mau-bao-cao-do-an.docx` (2 mặt, không khung, ≥ 30 trang) | `templates/word/do-an/` |
| Mẫu Word ĐATN/KLTN | `mau-luan-van-tot-nghiep.docx` (BM 2.1–2.3, ≥ 40 trang) | `templates/word/luan-van/` |
| Mẫu Word NCKH | `mau-bao-cao-tong-ket-sv04.docx`, `mau-bao-cao-nckh.docx`, `mau-de-cuong-nckh.docx` | `templates/word/nckh/` |
| Công cụ Word | 8 script Python: tạo bìa, chuẩn hóa, chấm điểm định dạng & nội dung, xuất PDF | `tools/word/` ([README](templates/word/README.md)) |
| Công cụ Vẽ kỹ thuật & BIM | 4 script: `tao_khung_a3_dxf.py`, `kiem_tra_dxf.py`, `dxf_to_png.py`, `kiem_tra_ifc.py` | `tools/draw/` |
| Ảnh xem trước | 10 ảnh bìa, trang xác nhận, Mẫu 2, Mẫu 3, trang nội dung mẫu | `assets/word/` |

---

## 🔄 Cách thêm tri thức mới

1. Tạo note bằng `tools/new-note.ps1` (hoặc copy `templates/note.md` vào `wiki/<khu-vuc>/ten-kebab-case.md`).
2. Thêm 1 dòng vào bảng tương ứng trong `index.md`.
3. Chạy `powershell -ExecutionPolicy Bypass -File tools\health-check.ps1` — đảm bảo **0 mồ côi · 0 link gãy**.
4. Ghi 1 dòng ngắn vào `log.md`.
