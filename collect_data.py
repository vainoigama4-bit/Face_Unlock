import cv2 as cv
import os

# ============================================================
#  BƯỚC 1 & 2: Tạo folder chứa mẫu dữ liệu + nhập user name
# ============================================================
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)  # Tạo folder gốc nếu chưa có

user_name = input("Nhập tên người dùng (user_name): ").strip()
if not user_name:
    print("Tên không được để trống!")
    exit()

# ============================================================
#  BƯỚC 3: Tạo thư mục trùng tên với user_name
# ============================================================
save_path = os.path.join(DATA_FOLDER, user_name)

if os.path.exists(save_path):
    print(f"[!] Người dùng '{user_name}' đã tồn tại. Vui lòng chọn tên khác.")
    exit()

os.makedirs(save_path)
print(f"[✓] Đã tạo thư mục: {save_path}")

# ============================================================
#  BƯỚC 4: Thu thập 100 ảnh khuôn mặt của user
# ============================================================
cap = cv.VideoCapture(0)  # 0 = camera tích hợp, 1 = webcam ngoài
face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0
TOTAL_SAMPLES = 100

print(f"\n[*] Bắt đầu thu thập dữ liệu cho '{user_name}'...")
print(f"    Nhìn thẳng vào camera. Nhấn 'q' để thoát sớm.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc từ camera!")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    faces = face_cascade.detectMultiScale(blur, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Lưu ảnh khuôn mặt (grayscale, đã blur)
        face_img = blur[y:y+h, x:x+w]
        cv.imwrite(os.path.join(save_path, f"{count}.jpg"), face_img)
        count += 1

        # Vẽ khung và tiến trình lên frame hiển thị
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 0), 2)
        cv.putText(frame, f"Mau: {count}/{TOTAL_SAMPLES}",
                   (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)

    # Thanh tiến trình ở góc màn hình
    cv.putText(frame, f"Thu thap du lieu: {user_name}",
               (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"[{count}/{TOTAL_SAMPLES}] Nhan 'q' de thoat",
               (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv.imshow("Thu thap du lieu khuon mat", frame)

    if cv.waitKey(1) & 0xFF == ord('q') or count >= TOTAL_SAMPLES:
        break

cap.release()
cv.destroyAllWindows()

if count >= TOTAL_SAMPLES:
    print(f"\n[✓] Đã thu thập đủ {TOTAL_SAMPLES} mẫu cho '{user_name}'!")
    print(f"    Chạy 'train_model.py' để huấn luyện mô hình.")
else:
    print(f"\n[!] Chỉ thu thập được {count} mẫu. Cần ít nhất 100 ảnh.")
