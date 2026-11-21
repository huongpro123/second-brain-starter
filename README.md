# Second Brain Starter + Bộ công cụ Báo cáo CTUT

Một starter kit kết hợp **hai phần dùng chung ngay**:

1. **Bộ não thứ hai (Obsidian + AI Agent Workflow):** cấu trúc vault tách `raw/` (nguồn thô) và `wiki/` (tri thức chưng cất), có `AGENTS.md`, `CLAUDE.md`, `index.md`, script kiểm tra sức khỏe vault (`health-check.ps1`), cùng bộ quy trình làm việc cho agent (3 chế độ Vibe/Spike/Spec, DoR 5 câu, DoD, quyền hạn agent, 10 giai đoạn xây web/app, GitHub + Spec Kit).
2. **Bộ công cụ Báo cáo học thuật chuẩn CTUT (`bao-cao-ctut`):** 5 mẫu Word `.docx` chuẩn **QĐ 345/QĐ-ĐHKTCN (08/4/2025)** (Đồ án, ĐATN/KLTN, TTTN) và **QĐ 886/2022 mẫu SV04** (NCKH sinh viên), 8 script Python tự động tạo bìa, chuẩn hóa style, kiểm định dạng (`kiem-tra.py`), soát nội dung chống ảo giác (`kiem-tra-noi-dung.py`), đồng bộ mục lục và xuất PDF, cùng 10 ảnh xem trước mẫu.

---

## Cài đặt nhanh

### 1. Clone repo về máy

```powershell
git clone <URL_REPO_CUA_BAN> second-brain
cd second-brain
```

Mở thư mục `second-brain` bằng **Obsidian** (nếu dùng Obsidian), **VS Code**, **Cursor**, **Claude Code**, **Codex** hoặc **Antigravity**. Giao diện tím khói đã cấu hình sẵn trong `.obsidian/snippets/second-brain-pretty.css`.

### 2. Cài thư viện Python (cho bộ công cụ Word)

Khuyến nghị tạo virtual environment:

```powershell
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

**Lưu ý theo hệ điều hành & tính năng:**

| Công cụ | Phụ thuộc | Ghi chú |
|---|---|---|
| `du-an-moi.py`, `bia-sv04.py`, `kiem-tra.py`, `kiem-tra-noi-dung.py`, `chuan-hoa.py`, `cham-loat.py` | `python-docx` | Chạy được trên Windows, macOS, Linux |
| Render ảnh bìa `bia-preview.png` (trong `du-an-moi.py`) & `dong-bo-muc-luc.py` | `pymupdf` + LibreOffice (`soffice`) | Tùy chọn; nếu chưa cài LibreOffice vẫn tạo file `.docx` bình thường |
| `word-hoan-tat.py` (cập nhật TOC/field & xuất PDF chuẩn in) | **Windows + Microsoft Word desktop + `pywin32`** | Khuyên dùng làm bước cuối trước khi in/nộp |
| `tools/health-check.ps1`, `new-note.ps1`, `push-vault.ps1` | PowerShell 5.1+ (Windows) hoặc `pwsh` | Chạy đa nền tảng nếu cài PowerShell 7 (`pwsh`) |

---

## Sử dụng nhanh

### A. Dùng làm Bộ não thứ hai cho AI Agent

1. Cập nhật thông tin của bạn vào `wiki/con-nguoi/ho-so-mau.md` (hoặc tạo note mới bằng `tools/new-note.ps1`).
2. Thêm các dự án đang làm vào `wiki/du-an/` và liệt kê vào `index.md`.
3. Khi mở phiên chat với AI Agent, yêu cầu agent đọc `AGENTS.md` và `index.md` trước (không quét toàn bộ thư mục).
4. Kiểm tra sức khỏe vault (note mồ côi, link gãy, note cũ, thiếu frontmatter):

```powershell
powershell -ExecutionPolicy Bypass -File tools\health-check.ps1
```

5. Tạo note mới đúng chuẩn frontmatter & tự gắn vào `index.md`:

```powershell
powershell -ExecutionPolicy Bypass -File tools\new-note.ps1 -Title "Ghi chu moi" -Area he-thong -Tags tool,setup
```

### B. Dùng bộ công cụ Báo cáo CTUT

Tạo khung báo cáo mới (bìa chính + bìa phụ + trang xác nhận + cấu trúc chương + `CHECK-LIST.md`):

```powershell
python tools/word/du-an-moi.py `
  --loai do-an `
  --ten "Tên đề tài của bạn" `
  --nganh "Công nghệ kỹ thuật điều khiển và tự động hóa" `
  --sv "Nguyễn Văn A" --mssv "MSSV001" --lop "LOP01" `
  --gvhd "TS. Giảng Viên A" `
  --out "./out/BaoCaoDoAn.docx"
```

Các giá trị `--loai`: `do-an` | `luan-van` | `nckh` (với báo cáo tổng kết NCKH SV04, dùng mẫu `templates/word/nckh/mau-bao-cao-tong-ket-sv04.docx` và dựng bìa Mẫu 1 bằng `tools/word/bia-sv04.py`).

Kiểm tra trước khi nộp:

```powershell
python tools/word/kiem-tra.py "./out/BaoCaoDoAn.docx"
python tools/word/kiem-tra-noi-dung.py "./out/BaoCaoDoAn.docx"
python tools/word/word-hoan-tat.py "./out/BaoCaoDoAn.docx" --pdf "./out/BaoCaoDoAn.pdf"
```

---

## Cấu trúc thư mục

```text
.
├── AGENTS.md                 # Bộ luật đọc/ghi vault và quy trình làm việc của agent
├── CLAUDE.md                 # Tóm tắt 3 dòng trỏ tới AGENTS.md
├── index.md                  # Bản đồ toàn bộ wiki (MOC)
├── log.md                    # Nhật ký thay đổi có ghi rõ "vì sao"
├── requirements.txt          # Thư viện Python cho bộ tool Word
├── LICENSE                   # MIT License (cho code & cấu trúc mẫu)
├── raw/                      # Nguồn thô (PDF, transcript, web...) — không nhồi thẳng vào context
├── wiki/                     # Tri thức đã chưng cất
│   ├── con-nguoi/            # Hồ sơ người dùng / nhóm
│   ├── du-an/                # Note trạng thái từng dự án
│   ├── he-thong/             # Môi trường máy, tool, cấu hình agent
│   ├── quy-trinh/            # Quy trình AI agent (3 chế độ, DoR, Spec Kit) & chuẩn CTUT
│   └── y-tuong/              # Ghi chú phương pháp (Second Brain, kỹ năng viết Word)
├── skills/                   # Định nghĩa skill dùng cho AI Agent (bao-cao-ctut v1.5.1)
├── templates/
│   ├── note.md               # Mẫu frontmatter note
│   └── word/                 # 5 mẫu .docx chuẩn CTUT + ảnh logo/khung bìa + hướng dẫn
├── assets/word/              # 10 ảnh xem trước các trang bìa/mẫu chuẩn (không dính dữ liệu cá nhân)
└── tools/
    ├── health-check.ps1      # Kiểm tra link gãy, note mồ côi, frontmatter
    ├── new-note.ps1          # Tạo note mới đúng chuẩn
    ├── push-vault.ps1        # Add + commit + push nhánh git hiện tại
    └── word/                 # 8 script xử lý & chấm điểm báo cáo Word
```

---

## Tích hợp toàn cục với AI Agent

Xem chi tiết cách gắn `skills/bao-cao-ctut` và `AGENTS.md` vào Claude Code, Codex CLI, Cursor hoặc Antigravity tại [skills/README.md](skills/README.md) và [wiki/quy-trinh/prompt-lam-bao-cao.md](wiki/quy-trinh/prompt-lam-bao-cao.md).

---

## Ghi chú bản quyền & miễn trừ

- Code Python, PowerShell, CSS, cấu trúc vault và quy trình Markdown được phát hành theo giấy phép **MIT** trong file [LICENSE](LICENSE).
- Các biểu mẫu, kích thước định dạng và quy chế học thuật tham chiếu theo văn bản công bố của **Trường Đại học Kỹ thuật – Công nghệ Cần Thơ (CTUT)** (QĐ 345/QĐ-ĐHKTCN 08/4/2025 và QĐ 886/QĐ-ĐHKTCN 2022). Hãy luôn đối chiếu lại thông báo mới nhất của Khoa/Trường khi nộp chính thức.
