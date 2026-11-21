---
name: ve-ky-thuat-va-web
description: Kỹ năng vẽ & tự động hóa bản vẽ kỹ thuật (AutoCAD .dxf/.dwg/AutoLISP, Revit pyRevit/Revit-MCP/API, BIMvision IFC/Python Bridge/BCF), sơ đồ điện (ezdxf, schemdraw) và sơ đồ/đồ họa ứng dụng Web (Draw.io .drawio, Excalidraw .excalidraw, Mermaid, D2, HTML5 SVG/Canvas). Bắt buộc render kiểm tra trực quan (PNG/viewport) trước khi bàn giao. Kích hoạt khi người dùng nói "autocad", "revit", "bimvision", "ifc", "dxf", "dwg", "autolisp", "bản vẽ kỹ thuật", "sơ đồ nguyên lý", "mạch điện", "tủ điện", "draw.io", "excalidraw", "mermaid", "d2", "svg", "vẽ web".
version: 1.1.0
updated: 2026-11-21
---

# Vẽ Kỹ Thuật (AutoCAD · Revit · BIMvision) & Đồ Họa Ứng Dụng Web

> **Nguyên tắc số 0 — Không bao giờ vẽ "mù" 1 lần rồi giao ngay.**
> Mọi bản vẽ 2D/3D/BIM hay sơ đồ web đều phải đi qua vòng lặp:
> **Thiết kế theo lưới & tham số → Sinh file chuẩn (`DXF`/`LSP`/`IFC`/`DRAWIO`/`SVG`) → Chạy kiểm lỗi cấu trúc → Render PNG / Mở xem trực quan → Tự sửa 1–3 vòng → Bàn giao.**

Đọc kèm: `wiki/quy-trinh/quy-trinh-ve-ky-thuat-va-web.md`.

---

## 1. Chọn đúng công cụ theo phần mềm & đầu ra (Decision Matrix)

| Nhu cầu / Phần mềm | Công cụ ưu tiên | Định dạng tạo ra | Ghi chú quan trọng |
|---|---|---|---|
| **AutoCAD 2D** (tủ điện, sơ đồ nguyên lý, mặt bằng, chi tiết 2D — không cần mở AutoCAD) | **Python `ezdxf`** + `tools/draw/` | `.dxf` (`AC1024`) + `.png`/`.pdf` | Xuất DXF chuẩn + render PNG tự soi bằng mắt |
| **AutoCAD Desktop đang mở (Windows)** | **AutoLISP (`.lsp`) / Script (`.scr`)** hoặc COM (`pywin32`) | `.lsp` / `.scr` | Tạm tắt `OSMODE = 0` khi vẽ tự động để tránh hít nhầm điểm |
| **Revit (tạo/sửa trực tiếp trong mô hình `.rvt`)** | **pyRevit (MCP / script Python)** hoặc **Revit-MCP (C#/.NET)** | Script Python/Revit API trong `Transaction` | Luôn xem trước thay đổi (Transaction group) trước khi commit vào `.rvt` |
| **Revit ↔ BIMvision / openBIM không cần mở Revit** | **Python `ifcopenshell`** + `tools/draw/kiem_tra_ifc.py` | `.ifc` (`IFC4` / `IFC2X3`) + `.bcf` | Tạo/vá Property Sets, kiểm tra chuẩn IDS/BCF, mở trực tiếp trên BIMvision & Revit |
| **BIMvision (kiểm tra mô hình đang mở bằng script)** | **BIMvision Python API Bridge** (`localhost:5000`) + `requests` | JSON query / chọn `GlobalId` / BCF viewpoint | Kết hợp `ifcopenshell` xử lý dữ liệu + BIMvision tô sáng & chụp góc nhìn |
| **Sơ đồ mạch điện tử / nguyên lý gọn nhúng báo cáo Word** | **Python `schemdraw`** | `.svg` + `.png` (300 DPI) | Ký hiệu chuẩn, tự nối dây sạch |
| **Chi tiết cơ khí / vỏ hộp 3D tham số** | **`build123d` / `CadQuery`** | `.step`, `.stl`, `.dxf` chiếu 2D | Phù hợp in 3D, cắt CNC |
| **Sơ đồ Web chỉnh tay tiếp trên trình duyệt & VS Code** | **Draw.io** hoặc **Excalidraw** | `.drawio` (XML) / `.excalidraw` (JSON) | Kéo thả chỉnh lại từng khối/mũi tên dễ dàng |
| **Lưu đồ / kiến trúc dạng text gắn Git/Markdown** | **Mermaid** hoặc **D2** | Khối code + `.svg`/`.png` | **D2** căn bố cục sơ đồ lớn đẹp hơn Mermaid |
| **Giao diện Web / Dashboard / HMI SCADA / Vector tùy biến** | **HTML5 + SVG / Canvas** (kèm browser screenshot) | `.html`, `.svg`, `.png` | Mở headless browser chụp PNG kiểm tràn chữ trước khi chốt |

---

## 2. Quy trình cho Mảng AutoCAD (`ezdxf` & AutoLISP)

### Bước 1: Dùng khung giấy & layer chuẩn từ bộ tool có sẵn

```powershell
python tools/draw/tao_khung_a3_dxf.py --kho A3 --ten "SO DO NGUYEN LY MACH DONG LUC" --ma-so "E-01" --nguoi-ve "Nguyen Van A" --out "./out/ban-ve.dxf"
```

*(Hoặc `import` hàm `tao_khung_chuan()` từ `tools/draw/tao_khung_a3_dxf.py` trong script vẽ chi tiết.)*

**Layer & Font chuẩn (chống lỗi khi mở trên AutoCAD):**
- `KHUNG_TEN` (`7`, nét `0.50 mm`), `THIET_BI` (`5` xanh dương, `0.35 mm`), `DONG_LUC_L1` (`1` Đỏ), `DONG_LUC_L2` (`40` Cam/Vàng), `DONG_LUC_L3` (`5` Xanh dương), `TRUNG_TINH_N` (`8` Xám), `TIEP_DIA_PE` (`3` Xanh lá, `DASHDOT`), `DIEU_KHIEN` (`1` Đỏ, `0.25 mm`), `CHU_THICH` (`7`), `KICH_THUOC` (`3`).
- Luôn dùng TextStyle Unicode **`ARIAL_VN`** (`arial.ttf`) để không bị vỡ dấu tiếng Việt thành `?` khi mở AutoCAD.

### Bước 2: Vẽ theo "Lưới + Chân đấu nối (`Pin-based`)"

1. Khai báo thông số lưới đầu file (`X_LEFT`, `Y_TOP`, `COL_STEP`, `ROW_STEP`).
2. Mỗi khí cụ điện / khối viết thành hàm nhận tâm `(cx, cy)` và trả về `dict` tọa độ chân nối (`pins`).
3. Nối dây 100% từ `pins` theo góc vuông 90° (`add_lwpolyline`), đặt chấm nối tại ngã ba thật, giữ khoảng cách tối thiểu `3–5 mm` giữa chữ và dây, chiều cao chữ ≥ `2.2 mm` (không nhỏ hơn `1.8 mm`).

### Bước 3: Kiểm tra hình học + Render PNG + Nhìn bằng mắt (Bắt buộc)

```powershell
python tools/draw/kiem_tra_dxf.py "./out/ban-ve.dxf"
python tools/draw/dxf_to_png.py "./out/ban-ve.dxf" --out "./out/ban-ve-preview.png" --dpi 200
```

Mở `ban-ve-preview.png` xem bằng mắt: kiểm tra đè chữ, hở chân dây, tràn khung tên; có lỗi thì sửa script → render lại → xem lại trước khi giao.

---

## 3. Quy trình cho Mảng Revit & BIMvision (`Revit API / pyRevit / IFC / OpenBIM`)

### Nhánh A — Kiểm tra & xử lý file `.ifc` dùng chung cho cả Revit và BIMvision

1. Trước khi gửi/mở mô hình trong **BIMvision** hoặc import vào **Revit**, kiểm nhanh cấu trúc bằng:
   ```powershell
   python tools/draw/kiem_tra_ifc.py "./model.ifc"
   ```
   *(Cần `pip install ifcopenshell` — công cụ kiểm schema `IFC2X3`/`IFC4`, số tầng `IfcBuildingStorey`, thống kê đối tượng MEP/điện/kiến trúc, kiểm `GlobalId` & thuộc tính thiếu `Name`.)*
2. Khi sinh hoặc vá dữ liệu BIM hàng loạt không cần mở Revit nặng: dùng Python **`ifcopenshell`** để thêm/sửa Property Sets (`Pset_*`), gắn thẻ mã thiết bị hoặc xuất bảng khối lượng CSV/Excel cho dự toán & báo cáo.
3. Khi kiểm lỗi mô hình tự động (QA/IDS): tổng hợp danh sách phần tử lỗi kèm `GlobalId` → xuất file **`.bcf`** (qua `ifcopenshell.bcf`) để nạp vào BIMvision (*IFC Comments / BCF* / *IDS Checker*) mở đúng góc nhìn từng lỗi.

### Nhánh B — Điều khiển trực tiếp Revit (`pyRevit` / `Revit-MCP`)

- **Nếu nối qua `pyRevit` (MCP / IronPython) hoặc `Revit-MCP`:**
  1. Đọc trước danh sách Levels, Grids, Families/Types và Parameters đang có trong project trước khi đặt lệnh tạo đối tượng (không đoán tên Family không tồn tại).
  2. Mọi thao tác tạo/sửa đối tượng Revit API bắt buộc bọc trong **`Transaction` rõ ràng**, ghi chú đơn vị (**lưu ý đơn vị nội bộ Revit API là feet thập phân; phải quy đổi từ mm sang feet `/ 304.8`** khi tạo hình học).
  3. Chia từng bước kiểm chứng (ví dụ tạo lưới/tầng trước → kiểm tra view mặt bằng → mới đặt ống/máng cáp/tủ điện MEP) và để người dùng xem trước khi lưu file `.rvt`.

### Nhánh C — Tự động hóa trực tiếp trên BIMvision đang mở (`Python API Bridge`)

- Khi người dùng cài plugin **BIMvision Python API Bridge** (mở REST server mặc định tại `http://localhost:5000` khi BIMvision đang chạy):
  - Agent viết script Python (`requests`) để đọc danh sách đối tượng (`/elements`), lọc theo tầng/loại/Pset, tự động chọn & highlight các phần tử cần chú ý qua `GlobalId` (`/select`), hoặc đọc thuộc tính (`/element/properties`) đối chiếu với bảng thiết bị/điện trên Excel/Word.

---

## 4. Quy trình cho Mảng Đồ họa Ứng dụng Web

- **Draw.io (`.drawio` XML) & Excalidraw (`.excalidraw` JSON):** đặt node theo lưới bội số `20 px`/`40 px`, tăng chiều rộng box +25 % để chữ tiếng Việt có dấu không rớt dòng xấu; dùng `.drawio` cho sơ đồ SCADA/kỹ thuật trang trọng, `.excalidraw` cho sơ đồ ý tưởng/trình bày.
- **Mermaid & D2:** dùng cho sơ đồ luồng, tuần tự, kiến trúc trong Markdown; nhớ bọc ngoặc kép `id["Nhãn (có dấu ngoặc)"]`.
- **HTML5 + SVG / Canvas:** khai báo `viewBox="0 0 W H"`, tách `<g id="...">` theo tầng chức năng, chụp screenshot qua headless browser kiểm tra thực tế trước khi bàn giao.

---

## 5. Checklist bàn giao cho người dùng

- [ ] Đúng định dạng đích (`.dxf`/`.lsp`, `.ifc`/`.bcf`/script `pyRevit`, `.drawio`, `.excalidraw`, `.svg`/`.html`, kèm `.png` xem trước nếu có).
- [ ] Nếu là `.dxf`: `kiem_tra_dxf.py` không lỗi `FAIL`, đã render `.png` và mở kiểm tra trực quan.
- [ ] Nếu là `.ifc` cho Revit/BIMvision: đã kiểm qua `kiem_tra_ifc.py` (đủ tầng, đủ `Name`/Pset cơ bản).
- [ ] Nếu dùng thư viện tùy chọn (`ezdxf`, `schemdraw`, `ifcopenshell`), ghi rõ lệnh cài ngắn gọn.
