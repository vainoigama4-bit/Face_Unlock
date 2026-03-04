import cv2 as cv
import numpy as np
import os

# ============================================================
#  BƯỚC 5: Huấn luyện mô hình nhận diện bằng LBPHFaceRecognizer
# ============================================================
DATA_FOLDER = "data"
MODEL_FILE  = "face_recognizer_model.yml"
LABEL_FILE  = "label_dict.npy"

if not os.path.exists(DATA_FOLDER):
    print("[!] Chưa có dữ liệu. Hãy chạy 'collect_data.py' trước.")
    exit()

recognizer = cv.face.LBPHFaceRecognizer_create()

faces       = []
labels      = []
label_dict  = {}     # { label_số: "tên_user" }
label_index = 0

print("[*] Đang tải dữ liệu huấn luyện...\n")

for user_name in sorted(os.listdir(DATA_FOLDER)):
    user_path = os.path.join(DATA_FOLDER, user_name)
    if not os.path.isdir(user_path):
        continue

    images_in_folder = [
        f for f in os.listdir(user_path)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    if len(images_in_folder) == 0:
        print(f"  [!] Bỏ qua '{user_name}' – không có ảnh.")
        continue

    label_dict[label_index] = user_name
    count = 0

    for img_file in images_in_folder:
        img_path = os.path.join(user_path, img_file)
        img_gray = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        if img_gray is None:
            continue
        faces.append(img_gray)
        labels.append(label_index)
        count += 1

    print(f"  [✓] {user_name:20s} → label {label_index} | {count} ảnh")
    label_index += 1

if len(faces) == 0:
    print("\n[!] Không có dữ liệu để huấn luyện!")
    exit()

print(f"\n[*] Đang huấn luyện với {len(faces)} ảnh / {label_index} người...")

# ============================================================
#  BƯỚC 5 (tiếp): Huấn luyện và lưu mô hình
# ============================================================
recognizer.train(faces, np.array(labels))

# BƯỚC 6: Lưu mô hình đã huấn luyện
recognizer.save(MODEL_FILE)
np.save(LABEL_FILE, label_dict)

print(f"\n[✓] Mô hình đã lưu vào '{MODEL_FILE}'")
print(f"[✓] Nhãn đã lưu vào   '{LABEL_FILE}'")
print(f"\n    Chạy 'unlock.py' để sử dụng ứng dụng mở khoá.")
