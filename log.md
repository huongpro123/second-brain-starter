# Nhật ký vault

Ghi ngắn gọn các thay đổi đáng chú ý theo mẫu: `YYYY-MM-DD — <người/agent> — <việc gì> — vì sao: <lý do>`.

## 2026-11-21 — Thêm skill Vẽ kỹ thuật (AutoCAD · Revit · BIMvision) & Đồ họa Web + bộ tool DXF/IFC
- Thêm `skills/ve-ky-thuat-va-web/SKILL.md` (v1.1.0) và `wiki/quy-trinh/quy-trinh-ve-ky-thuat-va-web.md`: chuẩn hóa cách AI làm việc với AutoCAD (`ezdxf` + AutoLISP `.lsp`/`.scr`), Revit (`pyRevit`/Revit-MCP, quy đổi feet↔mm), BIMvision (`ifcopenshell` + Python API Bridge `localhost:5000` + BCF), mạch điện (`schemdraw`) và sơ đồ/đồ họa web (`Draw.io`, `Excalidraw`, `D2`, `Mermaid`, `HTML/SVG`) kèm vòng lặp kiểm chứng trực quan.
- Thêm `tools/draw/{tao_khung_a3_dxf,kiem_tra_dxf,dxf_to_png,kiem_tra_ifc}.py`: tạo khung bản vẽ TCVN/IEC hỗ trợ Unicode tiếng Việt (`ARIAL_VN`), tự kiểm tra DXF và IFC, và render DXF ra PNG không cần AutoCAD.
- Cập nhật `requirements.txt` (`ezdxf`, `schemdraw`, `matplotlib` + ghi chú tùy chọn `ifcopenshell`), `tools/setup.py`, `AGENTS.md`, `index.md`, `skills/README.md`, `README.md`, `phong-thoi-gian-khoi-tao.md`.

## 2026-11-21 — Thêm chế độ "Phòng Thời Gian" + Hook bảo vệ + Skill Phản biện báo cáo
- Thêm `tools/setup.py` và `tools/setup.ps1`: tự tạo `.venv`, cài `requirements.txt`, bật `.githooks/pre-commit`, kiểm tra sức khỏe vault, chấm điểm 5 mẫu Word và in sẵn prompt toàn cục theo đúng đường dẫn máy đang chạy.
- Thêm `wiki/quy-trinh/phong-thoi-gian-khoi-tao.md` và mục `0A` trong `AGENTS.md` / `CLAUDE.md`: giúp một agent hoàn toàn mới setup môi trường, nạp trọn các trụ cột kiến thức và phỏng vấn 4 câu cá nhân hóa chỉ trong một lượt.
- Thêm `.githooks/pre-commit`: chặn commit nhầm API key / private key và tự chạy `health-check.ps1` khi sửa note.
- Thêm `skills/phan-bien-bao-cao/SKILL.md` (v1.0.0): chuẩn hóa quy trình kiểm chứng đối nghịch trước khi nộp báo cáo.

## 2026-11-21 — Khởi tạo bản starter sạch để chia sẻ
- Tách bộ khung Second Brain + bộ công cụ báo cáo chuẩn CTUT (`bao-cao-ctut` v1.5.1) thành bộ starter sạch, không chứa dữ liệu cá nhân hay lịch sử Git cũ.
- Dọn đường dẫn cứng theo máy cá nhân thành đường dẫn tương đối / `<VAULT_DIR>`, bổ sung `requirements.txt`, `LICENSE`, và đồng bộ `index.md` + `skills/README.md`.
- Làm mới thư mục `wiki/{con-nguoi,du-an,he-thong}/` bằng 3 note mẫu để người nhận dễ tùy biến theo dự án riêng.
