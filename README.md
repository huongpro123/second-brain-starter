# Second Brain Starter + Bộ công cụ Báo cáo CTUT & Vẽ Kỹ Thuật

Một starter kit kết hợp đầy đủ các mảng làm việc với AI Agent, kèm **chế độ Phòng Thời Gian (`setup.py` + Onboarding)** giúp agent hoàn toàn mới tự cài môi trường, nạp trọn bộ quy tắc thực chiến và phỏng vấn cá nhân hóa vault chỉ trong một phiên:

1. **Bộ não thứ hai (Obsidian + AI Agent Workflow):** cấu trúc vault tách `raw/` (nguồn thô) và `wiki/` (tri thức chưng cất), có `AGENTS.md`, `CLAUDE.md`, `index.md`, script kiểm tra sức khỏe vault (`health-check.ps1`), git `pre-commit` hook chống lộ secret, cùng bộ quy trình làm việc (Vibe/Spike/Spec, DoR 5 câu, DoD, quyền hạn agent, 10 giai đoạn xây web/app, Spec Kit).
2. **Bộ công cụ Báo cáo học thuật chuẩn CTUT (`bao-cao-ctut` + `phan-bien-bao-cao`):** 5 mẫu Word `.docx` chuẩn **QĐ 345/QĐ-ĐHKTCN (08/4/2025)** (Đồ án, ĐATN/KLTN, TTTN) và **QĐ 886/2022 mẫu SV04** (NCKH sinh viên), 8 script Python tự động tạo bìa, chuẩn hóa style, kiểm định dạng (`kiem-tra.py`), soát nội dung chống ảo giác (`kiem-tra-noi-dung.py`), đồng bộ mục lục và xuất PDF, kèm skill phản biện đối nghịch trước khi nộp.
3. **Bộ kỹ năng Vẽ Kỹ Thuật (AutoCAD · Revit · BIMvision) & Đồ họa Web (`ve-ky-thuat-va-web`):** tạo bản vẽ DXF A3/A4 chuẩn layer IEC/TCVN (`ezdxf`), tự kiểm tra hình học (`kiem_tra_dxf.py`), render PNG không cần mở AutoCAD (`dxf_to_png.py`), chuẩn hóa luồng Revit (`pyRevit` / `Revit-MCP` / `ifcopenshell`), kiểm tra file `.ifc` cho BIMvision (`kiem_tra_ifc.py` + API Bridge + BCF), vẽ mạch điện (`schemdraw`) và xuất sơ đồ web chỉnh sửa được (`Draw.io`, `Excalidraw`, `D2`, `Mermaid`, `HTML/SVG`).

---

## Chế độ "Phòng Thời Gian": Setup cho Agent hoàn toàn mới

### Cách 1: Giao thẳng cho AI Agent mới

Clone repo, mở bằng **Antigravity / Claude Code / Codex / Cursor**, rồi nhắn đúng 1 câu:

> *"Đọc `AGENTS.md` và chạy luồng Phòng Thời Gian để setup vault + nạp toàn bộ kiến thức cho tôi."*

Agent mới sẽ tự động:
1. Chạy `python tools/setup.py` (tạo `.venv`, cài `requirements.txt`, bật `.githooks/pre-commit`, chạy `health-check.ps1` và kiểm 5/5 mẫu Word đạt 100/100).
2. Đọc tuần tự **6 trụ cột tri thức cốt lõi** (cách dùng vault, quy trình 3 chế độ, chuẩn CTUT QĐ 345 + SV04, luật chống ảo giác, phản biện báo cáo, và chuẩn vẽ AutoCAD/Web).
3. Hỏi bạn 4 câu ngắn để điền `wiki/con-nguoi/ho-so-mau.md` và note dự án đầu tiên.
4. Xuất sẵn đoạn Prompt toàn cục đã điền đúng đường dẫn thư mục máy bạn để dán cho các repo khác.

### Cách 2: Tự chạy tay trên terminal

```powershell
git clone <URL_REPO_CUA_BAN> second-brain
cd second-brain

# Tự động dựng .venv + cài thư viện + bật hook + kiểm tra toàn bộ + in prompt toàn cục:
python tools/setup.py
```

Nếu chỉ muốn kiểm tra môi trường mà chưa cài đặt gì:

```powershell
python tools/setup.py --check
```

**Lưu ý theo hệ điều hành & tính năng:**

| Công cụ | Phụ thuộc | Ghi chú |
|---|---|---|
| `tools/word/*.py` (`du-an-moi`, `bia-sv04`, `kiem-tra`, `kiem-tra-noi-dung`, `chuan-hoa`, `cham-loat`) | `python-docx` | Chạy được trên Windows, macOS, Linux |
| `tools/draw/*.py` (`tao_khung_a3_dxf`, `kiem_tra_dxf`, `dxf_to_png`, `kiem_tra_ifc`) | `ezdxf`, `matplotlib` *(+ `ifcopenshell` tùy chọn cho BIM)* | Tạo `.dxf`, kiểm lỗi và render `.png` **không cần mở AutoCAD**; kiểm tra `.ifc` cho Revit/BIMvision |
| Vẽ mạch nguyên lý gọn nhúng báo cáo | `schemdraw` | Xuất `.svg` / `.png` 300 DPI |
| Render ảnh bìa `bia-preview.png` (trong `du-an-moi.py`) & `dong-bo-muc-luc.py` | `pymupdf` + LibreOffice (`soffice`) | Tùy chọn; nếu chưa cài LibreOffice vẫn tạo file `.docx` bình thường |
| `word-hoan-tat.py` (cập nhật TOC/field & xuất PDF chuẩn in) | **Windows + Microsoft Word desktop + `pywin32`** | Khuyên dùng làm bước cuối trước khi in/nộp |
| `tools/health-check.ps1`, `new-note.ps1`, `push-vault.ps1` | PowerShell 5.1+ (Windows) hoặc `pwsh` | Chạy đa nền tảng nếu cài PowerShell 7 (`pwsh`) |

---

## Sử dụng nhanh hàng ngày

### A. Quản lý Bộ não thứ hai

- Tạo note mới đúng chuẩn frontmatter & tự gắn vào `index.md`:
  ```powershell
  powershell -ExecutionPolicy Bypass -File tools\new-note.ps1 -Title "Ghi chu moi" -Area du-an -Tags plc,note
  ```
- Kiểm tra note mồ côi / link gãy / frontmatter:
  ```powershell
  powershell -ExecutionPolicy Bypass -File tools\health-check.ps1
  ```
- Mở bằng Obsidian: chọn *Open folder as vault* trỏ vào thư mục repo này để dùng sẵn theme tím khói (`.obsidian/snippets/second-brain-pretty.css`).

### B. Tạo & kiểm tra báo cáo CTUT

```powershell
# 1. Tạo khung báo cáo mới (bìa chính + bìa phụ + xác nhận + 4 chương + CHECK-LIST.md)
.venv\Scripts\python.exe tools\word\du-an-moi.py `
  --loai do-an `
  --ten "Tên đề tài của bạn" `
  --nganh "Công nghệ kỹ thuật điều khiển và tự động hóa" `
  --sv "Nguyễn Văn A" --mssv "MSSV001" --lop "LOP01" `
  --gvhd "TS. Giảng Viên A" `
  --out "./out/BaoCaoDoAn.docx"

# 2. Chấm định dạng (≥ 90), soát ảo giác (≥ 90) và xuất PDF bằng Word thật
.venv\Scripts\python.exe tools\word\kiem-tra.py "./out/BaoCaoDoAn.docx"
.venv\Scripts\python.exe tools\word\kiem-tra-noi-dung.py "./out/BaoCaoDoAn.docx"
.venv\Scripts\python.exe tools\word\word-hoan-tat.py "./out/BaoCaoDoAn.docx" --pdf "./out/BaoCaoDoAn.pdf"
```

### C. Tạo khung bản vẽ AutoCAD DXF & Render kiểm lỗi

```powershell
# 1. Tạo khung A3 chuẩn TCVN + layer IEC + khung tên Unicode tiếng Việt
.venv\Scripts\python.exe tools\draw\tao_khung_a3_dxf.py --kho A3 --ten "SO DO NGUYEN LY MACH DONG LUC" --ma-so "E-01" --out "./out/ban-ve.dxf"

# 2. Kiểm tra layer, cỡ chữ, phạm vi khổ giấy và render PNG kiểm bằng mắt
.venv\Scripts\python.exe tools\draw\kiem_tra_dxf.py "./out/ban-ve.dxf"
.venv\Scripts\python.exe tools\draw\dxf_to_png.py "./out/ban-ve.dxf" --out "./out/ban-ve-preview.png"
```

*(Trên macOS/Linux thay `.venv\Scripts\python.exe` bằng `.venv/bin/python`.)*

---

## Cấu trúc thư mục

```text
.
├── AGENTS.md                 # Bộ luật + quy trình Phòng Thời Gian cho mọi AI Agent
├── CLAUDE.md                 # Tóm tắt nhanh trỏ tới AGENTS.md & setup.py
├── index.md                  # Bản đồ toàn bộ wiki (MOC)
├── log.md                    # Nhật ký thay đổi có ghi rõ "vì sao"
├── requirements.txt          # Thư viện Python cho bộ tool Word + Vẽ kỹ thuật
├── LICENSE                   # MIT License (cho code & cấu trúc mẫu)
├── .githooks/pre-commit      # Hook chặn lộ API key / kiểm tra link vault khi commit
├── raw/                      # Nguồn thô (PDF, transcript, web...) — không nhồi thẳng vào context
├── wiki/                     # Tri thức đã chưng cất
│   ├── con-nguoi/            # Hồ sơ người dùng / nhóm
│   ├── du-an/                # Note trạng thái từng dự án
│   ├── he-thong/             # Môi trường máy, tool, cấu hình agent
│   ├── quy-trinh/            # Phòng Thời Gian, Vibe/Spike/Spec, Spec Kit, chuẩn CTUT & Vẽ kỹ thuật
│   └── y-tuong/              # Ghi chú phương pháp (Second Brain, kỹ năng viết Word)
├── skills/
│   ├── bao-cao-ctut/         # Skill v1.5.1 tạo & chuẩn hóa báo cáo QĐ 345 + SV04
│   ├── phan-bien-bao-cao/    # Skill v1.0.0 kiểm chứng đối nghịch trước khi nộp
│   └── ve-ky-thuat-va-web/   # Skill v1.1.0 vẽ AutoCAD, Revit, BIMvision, schemdraw & sơ đồ web
├── templates/
│   ├── note.md               # Mẫu frontmatter note
│   └── word/                 # 5 mẫu .docx chuẩn CTUT + ảnh logo/khung bìa + hướng dẫn
├── assets/word/              # 10 ảnh xem trước các trang bìa/mẫu chuẩn (không dính dữ liệu cá nhân)
└── tools/
    ├── setup.py / setup.ps1  # Bộ khởi tạo tự động 1 lệnh (Phòng Thời Gian)
    ├── health-check.ps1      # Kiểm tra link gãy, note mồ côi, frontmatter
    ├── new-note.ps1          # Tạo note mới đúng chuẩn
    ├── push-vault.ps1        # Add + commit + push nhánh git hiện tại
    ├── draw/                 # 4 script AutoCAD DXF & openBIM IFC (khung A3/A4, kiểm DXF/IFC, render PNG)
    └── word/                 # 8 script xử lý & chấm điểm báo cáo Word
```

---

## Tích hợp toàn cục với AI Agent

Xem chi tiết cách gắn `skills/` và `AGENTS.md` vào Claude Code, Codex CLI, Cursor hoặc Antigravity tại [skills/README.md](skills/README.md) (hoặc chạy `python tools/setup.py --check` để in sẵn đoạn cấu hình đúng đường dẫn máy bạn).

---

## Ghi chú bản quyền & miễn trừ

- Code Python, PowerShell, Shell, CSS, cấu trúc vault và quy trình Markdown được phát hành theo giấy phép **MIT** trong file [LICENSE](LICENSE).
- Các biểu mẫu, kích thước định dạng và quy chế học thuật tham chiếu theo văn bản công bố của **Trường Đại học Kỹ thuật – Công nghệ Cần Thơ (CTUT)** (QĐ 345/QĐ-ĐHKTCN 08/4/2025 và QĐ 886/QĐ-ĐHKTCN 2022). Hãy luôn đối chiếu lại thông báo mới nhất của Khoa/Trường khi nộp chính thức.
