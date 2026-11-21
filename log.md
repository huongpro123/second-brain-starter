# Nhật ký vault

Ghi ngắn gọn các thay đổi đáng chú ý theo mẫu: `YYYY-MM-DD — <người/agent> — <việc gì> — vì sao: <lý do>`.

## 2026-11-21 — Thêm chế độ "Phòng Thời Gian" + Hook bảo vệ + Skill Phản biện báo cáo
- Thêm `tools/setup.py` và `tools/setup.ps1`: tự tạo `.venv`, cài `requirements.txt`, bật `.githooks/pre-commit`, kiểm tra sức khỏe vault, chấm điểm 5 mẫu Word và in sẵn prompt toàn cục theo đúng đường dẫn máy đang chạy.
- Thêm `wiki/quy-trinh/phong-thoi-gian-khoi-tao.md` và mục `0A` trong `AGENTS.md` / `CLAUDE.md`: giúp một agent hoàn toàn mới setup môi trường, nạp trọn 5 trụ cột kiến thức và phỏng vấn 4 câu cá nhân hóa chỉ trong một lượt.
- Thêm `.githooks/pre-commit`: chặn commit nhầm API key / private key và tự chạy `health-check.ps1` khi sửa note.
- Thêm `skills/phan-bien-bao-cao/SKILL.md` (v1.0.0): chuẩn hóa quy trình kiểm chứng đối nghịch trước khi nộp báo cáo.

## 2026-11-21 — Khởi tạo bản starter sạch để chia sẻ
- Tách bộ khung Second Brain + bộ công cụ báo cáo chuẩn CTUT (`bao-cao-ctut` v1.5.1) thành bộ starter sạch, không chứa dữ liệu cá nhân hay lịch sử Git cũ.
- Dọn đường dẫn cứng theo máy cá nhân thành đường dẫn tương đối / `<VAULT_DIR>`, bổ sung `requirements.txt`, `LICENSE`, và đồng bộ `index.md` + `skills/README.md`.
- Làm mới thư mục `wiki/{con-nguoi,du-an,he-thong}/` bằng 3 note mẫu để người nhận dễ tùy biến theo dự án riêng.
