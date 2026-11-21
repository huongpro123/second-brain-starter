# Bộ mẫu báo cáo Word — CTUT

Chuẩn hiện hành: **QĐ 345/QĐ-ĐHKTCN ngày 08/4/2025** (đồ án, ĐATN/KLTN, TTTN) và **QĐ 886/QĐ-ĐHKTCN (2022) cho NCKH sinh viên**
+ **Hướng dẫn định dạng báo cáo Đồ án (ĐA1/2/3)** của Khoa. Quy trình đầy đủ:
`wiki/quy-trinh/quy-trinh-bao-cao-ctut.md`. Skill cho agent: `skills/bao-cao-ctut/SKILL.md`.

## 1. Mẫu có gì

| Loại | Mẫu | In giấy | Bìa cứng | Số trang tối thiểu |
|---|---|---|---|---|
| Đồ án / Đồ án 2 | `do-an/mau-bao-cao-do-an.docx` | **hai mặt** | **xanh dương + gáy xanh dương** | **30** |
| ĐATN / Khóa luận tốt nghiệp | `luan-van/mau-luan-van-tot-nghiep.docx` | một mặt | xanh dương | 40 |
| NCKH — báo cáo tổng kết (SV04) | `nckh/mau-bao-cao-tong-ket-sv04.docx` | một mặt | xanh dương | **50–100** |
| NCKH — báo cáo tổng kết (bản cũ, form đồ án) | `nckh/mau-bao-cao-nckh.docx` | một mặt | xanh dương | theo đơn vị |
| NCKH — đề cương | `nckh/mau-de-cuong-nckh.docx` | — | — | bản tham khảo đề cương |

Mỗi mẫu đã có: **bìa chính + bìa phụ + trang xác nhận** (BM 2.1/2.2/2.3 — đồ án dùng bảng xác nhận
của đơn vị + "Ngày nộp báo cáo"), front matter (số La Mã), thân bài (số Ả Rập), header/footer đúng loại,
mục lục TOC field, style chuẩn. Các mẫu báo cáo đều đạt **100/100** theo `kiem-tra.py`.

## 2. Khác biệt giữa 3 loại (quan trọng nhất)

| | Đồ án | ĐATN / KLTN | TTTN |
|---|---|---|---|
| In giấy | **hai mặt** | một mặt | một mặt |
| Bìa cứng | **xanh dương** | xanh dương | **xanh lá** |
| Khung bìa | **không** | có (xanh `1F3864`) | có |
| Số trang | **giữa, dưới** (footer trái: tên SV nghiêng; header: tiêu đề phần nghiêng) | **giữa, trên** | giữa, trên |
| Danh mục | bảng biểu → hình ảnh | hình vẽ → bảng biểu | hình → bảng |
| Số chương | 4 (Tổng quan → Cơ sở lý thuyết → Thiết kế & chế tạo → Kết luận) | 4 (Tổng quan lý thuyết & cơ sở NC → Phương tiện & PP NC → Kết quả & thảo luận → Kết luận & đề xuất) | 4 (Giới thiệu tổng quan → Cơ sở lý thuyết → Kết quả & thảo luận → Kết luận & đề xuất) |

## 3. Quy chuẩn định dạng (QĐ 345 + HD Đồ án)

- Khổ **A4** (21 × 29,7 cm); **lề Trái 3,0 · Phải 2,0 · Trên 2,0 · Dưới 2,0 cm**; header/footer **1,0 cm**
- Times New Roman **13 pt**; **giãn dòng 1,2**; cách đoạn **6 pt (before + after)**; thụt đầu dòng **1 cm**; justify
- **TÊN CHƯƠNG** 14 in hoa đậm giữa · cấp 1 (1., 2.) 13 in hoa đậm · cấp 2 13 đậm · **cấp 3 13 đậm nghiêng**
- **Tên bảng** 13 đậm, trái, **trên** bảng · chú thích bảng 11 nghiêng · **tên hình** 13 đậm, giữa, **dưới** hình
- Đánh số bảng/hình theo chương (`Bảng 4.1`, `Hình 3.2`); nên dùng **bảng 3 dòng**; ô trống ghi "-"
- Số trang: La Mã cho mục mở đầu (i, ii…), Ả Rập từ nội dung chính; mục lục field TOC (**Ctrl+A → F9**)

## 4. Tạo báo cáo mới trong 5 phút

```powershell
# Đồ án 2 (in 2 mặt)
python tools/word/du-an-moi.py --loai do-an --ten "Hệ thống giám sát và điều khiển ..." --nganh "Công nghệ kỹ thuật điều khiển và tự động hóa" `
  --sv "Nguyễn Văn A" --mssv "MSSV001" --lop "LOP01" --gvhd "TS. Giảng Viên A" `
  --out "./out/BaoCaoDoAn2.docx" --mo
```

Tool sẽ: điền bìa chính + bìa phụ + trang xác nhận + header/footer → lưu `.docx` → render `bia-preview.png` (nếu có LibreOffice + `pymupdf`)
→ ghi `CHECK-LIST.md` riêng theo loại. **Mở `bia-preview.png` hoặc trang 1 xem bằng mắt trước khi viết nội dung.**

- Kiểm tra định dạng: `python tools/word/kiem-tra.py file.docx` (≥90 mới in; mẫu chuẩn = 100).
- Soát nội dung: `python tools/word/kiem-tra-noi-dung.py file.docx` (chống ảo giác: placeholder, số %
  không dẫn chứng, trích dẫn lệch, số liệu TÓM TẮT ≠ KẾT LUẬN). Luật chi tiết: `wiki/quy-trinh/luat-viet-noi-dung.md`.
- Chuẩn hóa file cũ: `python tools/word/chuan-hoa.py file.docx` (tự sửa style, báo phần không sửa được).
- Chấm hàng loạt: `python tools/word/cham-loat.py "./folder-word" --md bao-cao-cham.md`.

## 5. Ghi chú

- Số trang của **đồ án**: văn bản ghi "giữa, phía dưới"; mẫu trong bộ này đặt **giữa-dưới** theo văn bản,
  có footer trái = tên sinh viên *in nghiêng*, header = *tiêu đề phần đang trình bày*.
- Khi in: bìa cứng đúng màu, dán gáy cùng màu; ĐATN/KLTN in một mặt; sau bảo vệ 7 ngày nộp 2 bản in + 1 PDF.
- Nguồn chuẩn có thể đổi: kiểm tra `https://khoaddt.ctuet.edu.vn/` trước khi dùng.

## 6. Công cụ nâng cao

- `python tools/word/bia-sv04.py --file "<file.docx>" --ten "TÊN ĐỀ TÀI" --gvhd "ThS. Giảng Viên A" --sv "Nguyễn Văn A" --mssv MSSV001 --nganh "..." --thang 11 --nam 2026`
  — dựng lại **bìa Mẫu 1** cho báo cáo NCKH: khung trang, logo 3,3cm, TRƯỜNG/KHOA 13, BÁO CÁO 16, tên đề tài 16–22,
  hai khối GVHD | SVTH không kẻ bảng, ngày 13. Có `--template` để dựng mẫu trắng.
- `python tools/word/dong-bo-muc-luc.py "<file.docx>"` — cập nhật số trang MỤC LỤC theo bố cục thật (TOC field là cache);
  kiểm lại bằng `--dry-run` (phải 0 dòng lệch).
- `python tools/word/kiem-tra-noi-dung.py "<file.docx>"` — có thêm check `TIEU_MUC_MONG` (tiểu mục <2 đoạn văn).
- `python tools/word/word-hoan-tat.py "<file.docx>" --pdf "<file.pdf>"` — **bước cuối chuẩn nhất trên Windows**:
  mở Microsoft Word thật (COM), cập nhật mọi field (PAGE, TOC, danh mục bảng/hình), repaginate, lưu `.docx` rồi xuất PDF.
  Cần `python -m pip install pywin32`. Không có Word thì dùng `dong-bo-muc-luc.py` cho số trang mục lục.
- Nếu cài công cụ kiểm cấu trúc OpenXML (`openxml-audit`): `openxml-audit "<file.docx>" -f microsoft365 -q`
  (exit 0 + không in gì = không lỗi cấu trúc).
- **Field TOC lạc**: nếu `.docx` còn một field TOC rỗng ở cuối tài liệu (di sản của lần copy/chuyển đổi), Word sẽ
  đổ cả mục lục vào cuối → xoá field đó; giữ **một** field TOC thật ngay dưới tiêu đề MỤC LỤC. Và hạ các tiêu đề
  form (Mẫu 2, Mẫu 3, tiêu đề "MỤC LỤC") khỏi style Heading để chúng không bị liệt kê trong mục lục.
- **Khung bìa NCKH**: là ảnh nền `templates/word/img/khung-bia-sv04.png` (nét mảnh đen ngoài + nét đậm navy
  trong + 4 góc trang trí), chèn bằng `chen_khung_bia()` — muốn đổi viền chỉ cần thay file PNG này.
- **Gạch đầu dòng**: dùng `- ` chứ không dùng `●`/`•`.
