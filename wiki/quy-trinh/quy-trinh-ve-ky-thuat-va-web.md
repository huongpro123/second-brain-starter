---
title: Quy trình & Xu hướng vẽ kỹ thuật (AutoCAD · Revit · BIMvision) và Đồ họa Web
updated: 2026-11-21
status: active
tags: [quy-trinh, autocad, revit, bimvision, ifc, dxf, ezdxf, diagram, svg, web]
sources:
  - "Skill skills/ve-ky-thuat-va-web/SKILL.md"
---

# Quy trình vẽ kỹ thuật (AutoCAD · Revit · BIMvision) & đồ họa web

Ghi chú chưng cất các nguyên tắc quan trọng nhất để AI agent làm việc hiệu quả với bản vẽ 2D AutoCAD, mô hình BIM Revit/BIMvision và sơ đồ trên các ứng dụng web.

---

## 1. Xu hướng cốt lõi: Code / Giao thức chuẩn + Kiểm chứng trực quan

Thay vì để LLM đoán tọa độ mù một lần hoặc click chuột chậm chạp trên giao diện đồ họa, quy trình 2026 tách làm 3 lớp rõ ràng:

1. **Sinh hoặc sửa bằng định dạng chuẩn / API:** Python (`ezdxf`, `schemdraw`, `ifcopenshell`), script AutoLISP/pyRevit/Revit-MCP, BIMvision Python API Bridge (`localhost:5000`), hoặc file mở trực tiếp trên web (`.drawio`, `.excalidraw`, `D2`, `Mermaid`, `SVG`).
2. **Kiểm tra cấu trúc bằng script:** bắt lỗi layer, cỡ chữ quá nhỏ, thiếu thuộc tính Pset/`GlobalId`, đối tượng tràn khung giấy.
3. **Render ra PNG hoặc mở viewport nhìn kiểm lỗi:** sửa 1–3 vòng cho hết đè chữ / lệch chân nối trước khi bàn giao.

---

## 2. Bản đồ chọn công cụ theo phần mềm

| Phần mềm / Nhu cầu | Công cụ AI dùng | Đầu ra |
|---|---|---|
| **AutoCAD 2D** (tủ điện, sơ đồ nguyên lý, chi tiết 2D không cần mở AutoCAD) | Python **`ezdxf`** + `tools/draw/` | `.dxf` + `.png`/`.pdf` |
| **AutoCAD Desktop đang mở (Windows)** | **AutoLISP (`.lsp`) / `.scr`** hoặc COM (`pywin32`) | Lệnh vẽ thẳng vào `.dwg` |
| **Revit đang mở (`.rvt`)** | **pyRevit (MCP / Python routes)** hoặc **Revit-MCP (C#/.NET)** | Tạo/sửa element qua `Transaction` |
| **OpenBIM giữa Revit ↔ BIMvision (không cần mở Revit)** | Python **`ifcopenshell`** + `tools/draw/kiem_tra_ifc.py` | `.ifc` (`IFC4`/`IFC2X3`), `.bcf`, CSV khối lượng |
| **BIMvision đang mở trên máy** | **BIMvision Python API Bridge** (`http://localhost:5000`) | Script Python lọc/chọn `GlobalId`, đọc Psets, kiểm lỗi |
| **Mạch điện tử / nguyên lý gọn cho báo cáo Word** | Python **`schemdraw`** | `.svg` / `.png` 300 DPI |
| **Chi tiết 3D tham số** | **`build123d`** / **`CadQuery`** | `.step`, `.stl`, `.dxf` |
| **Sơ đồ kéo thả tiếp trên Web & VS Code** | **Draw.io (`.drawio` XML)** / **Excalidraw (`.excalidraw` JSON)** | File sơ đồ mở sửa lại được ngay |
| **Lưu đồ / kiến trúc trong Markdown** | **Mermaid** / **D2** | Text + `.svg`/`.png` |
| **Giao diện Web / Dashboard / HMI SCADA** | **HTML5 + SVG / Canvas** + headless screenshot | `.html`, `.svg`, `.png` |

---

## 3. Sáu bẫy kỹ thuật hay gặp (CAD · Revit · BIMvision · Web)

1. **Vỡ dấu tiếng Việt trong AutoCAD DXF:**
   - *Nguyên nhân:* `TextStyle` mặc định trỏ font SHX không đủ bảng mã Unicode.
   - *Khắc phục:* Tạo `ARIAL_VN` trỏ `arial.ttf` (đã dựng sẵn trong `tools/draw/tao_khung_a3_dxf.py`).
2. **Đứt dây / lệch chân khí cụ điện trong bản vẽ 2D:**
   - *Khắc phục:* Mỗi thiết bị trả về `dict` tọa độ các chân cắm (`pins`); mọi dây nối nối theo `pins` trên lưới tọa độ chung.
3. **AutoCAD tự hít nhầm điểm khi chạy `.lsp` / `.scr`:**
   - *Khắc phục:* Luôn lưu `OSMODE`, đặt `OSMODE = 0` trong khi script vẽ rồi trả lại giá trị cũ ở cuối script.
4. **Sai đơn vị 304,8 lần trong Revit API (`pyRevit` / `Revit-MCP`):**
   - *Nguyên nhân:* Giao diện Revit hiển thị mm/m, nhưng đơn vị nội bộ của **Revit API** là **decimal feet (`1 ft = 304,8 mm`)**. Quên quy đổi sẽ tạo ống/tủ/cột to gấp 304,8 lần!
5. **Xuất IFC từ Revit sang BIMvision bị thiếu thông số hoặc mất nhóm tầng:**
   - *Khắc phục:* Dùng `kiem_tra_ifc.py` rà nhanh schema (`IFC4` / `IFC2X3`), kiểm tra đủ `IfcBuildingStorey`, `GlobalId`, `Name` và Property Sets; nếu thiếu Pset hàng loạt, vá tự động bằng `ifcopenshell` rồi xuất danh sách lỗi dạng `.bcf` nạp vào BIMvision.
6. **Chữ tiếng Việt tràn khung trong `.drawio` / `.excalidraw` / `SVG`:**
   - *Khắc phục:* Tính chiều rộng box dư ~25 % và luôn mở ảnh PNG xem lại bằng mắt trước khi bàn giao.

---

## 4. Quy chuẩn Layer AutoCAD mặc định (`tools/draw/`)

| Tên Layer | Màu AutoCAD | Nét mặc định | Mục đích |
|---|---|---|---|
| `KHUNG_TEN` | `7` (Trắng/Đen) | `0.50 mm` | Khung bản vẽ TCVN + khung tên |
| `THIET_BI` | `5` (Xanh dương) | `0.35 mm` | Thân thiết bị điện, vỏ tủ, đường bao chi tiết |
| `DONG_LUC_L1` | `1` (Đỏ) | `0.35 mm` | Dây pha L1 / động lực chính |
| `DONG_LUC_L2` | `40` (Cam) | `0.35 mm` | Dây pha L2 (dễ nhìn trên cả nền đen lẫn giấy trắng) |
| `DONG_LUC_L3` | `5` (Xanh dương) | `0.35 mm` | Dây pha L3 |
| `TRUNG_TINH_N` | `8` (Xám) | `0.25 mm` | Dây trung tính N |
| `TIEP_DIA_PE` | `3` (Xanh lá) | `0.25 mm` (`DASHDOT`) | Dây bảo vệ tiếp địa PE |
| `DIEU_KHIEN` | `1` (Đỏ) | `0.25 mm` | Mạch điều khiển, tín hiệu PLC / relay |
| `CHU_THICH` | `7` (Trắng/Đen) | `0.18 mm` | Ký hiệu thiết bị (`Q1`, `KM1`), thông số, ghi chú |
| `KICH_THUOC` | `3` (Xanh lá) | `0.18 mm` | Đường gióng, đường kích thước |

## Liên quan

- `skills/ve-ky-thuat-va-web/SKILL.md`
- [[quy-trinh-3-che-do]]
- [[phong-thoi-gian-khoi-tao]]
- `tools/draw/` (`tao_khung_a3_dxf.py`, `kiem_tra_dxf.py`, `dxf_to_png.py`, `kiem_tra_ifc.py`)
