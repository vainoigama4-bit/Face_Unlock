
# 🔓 Mở Khoá Bằng Khuôn Mặt (Face Unlock)

Hệ thống nhận diện khuôn mặt sử dụng **OpenCV LBPH** để xác thực chủ sở hữu và
gửi email thông báo khi mở khoá thành công.

---

## 📁 Cấu trúc file

```
face_unlock/
├── config.py          # Cấu hình owner & email  ← CHỈNH TRƯỚC
├── collect_data.py    # Bước 1: Thu thập ảnh khuôn mặt
├── train_model.py     # Bước 2: Huấn luyện mô hình LBPH
├── unlock.py          # Bước 3: Ứng dụng mở khoá + gửi email
├── data/              # Thư mục chứa ảnh mẫu (tự tạo)
├── face_recognizer_model.yml   # Mô hình sau khi train
└── label_dict.npy              # Bảng ánh xạ nhãn → tên
```

---

## ⚙️ Cài đặt

```bash
pip install opencv-contrib-python numpy
```

---

## 🚀 Hướng dẫn sử dụng (theo thứ tự)

### Bước 0 – Cấu hình `config.py`

Mở file `config.py` và chỉnh:

| Biến              | Ý nghĩa                                      |
|-------------------|----------------------------------------------|
| `OWNER_NAME`      | Tên của chủ sở hữu (phải khớp tên đã nhập khi thu thập dữ liệu) |
| `EMAIL_SENDER`    | Gmail dùng để gửi thông báo                  |
| `EMAIL_PASSWORD`  | **App Password** của Gmail (không phải mật khẩu thường) |
| `EMAIL_RECEIVER`  | Email nhận thông báo                         |

> **Lấy App Password Gmail:**  
> Tài khoản Google → Bảo mật → Xác minh 2 bước → Mật khẩu ứng dụng

---

### Bước 1 – Thu thập dữ liệu

```bash
python collect_data.py
```
- Nhập tên người dùng khi được hỏi
- Nhìn thẳng vào camera, xoay mặt nhẹ để đa dạng góc độ
- Chương trình tự dừng sau khi đủ **100 ảnh**
- Lặp lại cho từng người cần đăng ký (ít nhất 5 người theo yêu cầu)

---

### Bước 2 – Huấn luyện mô hình

```bash
python train_model.py
```
- Tự động đọc tất cả ảnh trong thư mục `data/`
- Huấn luyện mô hình LBPH và lưu vào `face_recognizer_model.yml`

---

### Bước 3 – Mở khoá

```bash
python unlock.py
```
- Camera bật, nhận diện liên tục
- ✅ Nhận diện đúng chủ sở hữu → hiển thị **"ĐÃ MỞ KHOÁ"** + gửi email
- ❌ Không nhận ra → hiển thị **"Unknown"** (khung đỏ)
- Nhấn `r` để reset khoá, nhấn `q` để thoát

---

## 📧 Nội dung email thông báo

```
Chủ đề: 🔓 Thông báo: Hệ thống đã mở khoá thành công

👤 Người dùng : your_name
🕐 Thời gian   : 04/03/2026 14:35:22
✅ Trạng thái  : ĐÃ MỞ KHOÁ THÀNH CÔNG
```

---

## 🛠️ Tùy chỉnh nâng cao (`config.py`)

| Biến                   | Mặc định | Ý nghĩa                              |
|------------------------|----------|--------------------------------------|
| `CONFIDENCE_THRESHOLD` | `50`     | Ngưỡng độ tin cậy (thấp = chính xác hơn) |
| `EMAIL_COOLDOWN`       | `30`     | Giây chờ giữa 2 lần gửi email        |
