import cv2 as cv
import numpy as np
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Import cấu hình
from config import (
    OWNER_NAME,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECEIVER,
    CONFIDENCE_THRESHOLD,
    EMAIL_COOLDOWN,
)

MODEL_FILE = "face_recognizer_model.yml"
LABEL_FILE = "label_dict.npy"

if not os.path.exists(MODEL_FILE) or not os.path.exists(LABEL_FILE):
    print("[!] Chưa có mô hình. Hãy chạy 'train_model.py' trước.")
    exit()

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_FILE)
label_dict = np.load(LABEL_FILE, allow_pickle=True).item()

face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_frontalface_default.xml"
)

print(f"[✓] Đã tải mô hình. Chủ sở hữu (owner): '{OWNER_NAME}'")
print(f"[*] Bắt đầu nhận diện. Nhấn 'q' để thoát, 'r' để reset.\n")


def send_unlock_email(person_name: str):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    subject = "🔓 Thông báo: Hệ thống đã mở khoá thành công"
    body = f"""
Xin chào,

Hệ thống nhận diện khuôn mặt vừa xác nhận:

  👤 Người dùng : {person_name}
  🕐 Thời gian   : {timestamp}
  ✅ Trạng thái  : ĐÃ MỞ KHOÁ THÀNH CÔNG

---
Email này được gửi tự động từ hệ thống mở khoá bằng khuôn mặt.
"""
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print(f"  [✉] Email thông báo đã gửi đến {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"  [!] Không thể gửi email: {e}")


cap = cv.VideoCapture(0)

last_email_time = 0
is_unlocked     = False
UNLOCK_HOLD_FRAMES = 5   # Giảm từ 10 xuống 5 frame cho dễ unlock
unlock_frame_count  = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("[!] Lỗi camera!")
        break

    gray  = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    dblur = cv.GaussianBlur(gray, (5, 5), 0)
    faces = face_cascade.detectMultiScale(dblur, scaleFactor=1.3, minNeighbors=5)

    detected_owner = False

    for (x, y, w, h) in faces:
        face_img = dblur[y:y+h, x:x+w]
        label_id, confidence = recognizer.predict(face_img)

        if confidence < CONFIDENCE_THRESHOLD:
            person_name = label_dict.get(label_id, "Unknown")
            color       = (0, 255, 0)
            text        = f"{person_name} ({confidence:.1f})"

            if person_name == OWNER_NAME:
                detected_owner     = True
                unlock_frame_count += 1
                print(f"  [~] Nhận diện đúng: frame {unlock_frame_count}/{UNLOCK_HOLD_FRAMES}")
            else:
                unlock_frame_count = 0
        else:
            person_name        = "Unknown"
            color              = (0, 0, 255)
            text               = f"Unknown ({confidence:.1f})"
            unlock_frame_count = 0

        cv.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv.putText(frame, text, (x, y - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    # Kiểm tra điều kiện mở khoá
    if unlock_frame_count >= UNLOCK_HOLD_FRAMES:
        is_unlocked = True

    # Hiển thị trạng thái — KHÔNG cần detected_owner để show banner
    if is_unlocked:
        h_frame, w_frame = frame.shape[:2]
        banner_text = "DA MO KHOA"
        font_scale  = 2.0
        thickness   = 4
        (tw, th), _ = cv.getTextSize(banner_text, cv.FONT_HERSHEY_DUPLEX, font_scale, thickness)
        tx = (w_frame - tw) // 2
        ty = (h_frame + th) // 2

        cv.rectangle(frame, (tx - 20, ty - th - 20), (tx + tw + 20, ty + 20),
                     (0, 180, 0), -1)
        cv.putText(frame, banner_text, (tx, ty),
                   cv.FONT_HERSHEY_DUPLEX, font_scale, (255, 255, 255), thickness)

        # Gửi email (cooldown)
        now = time.time()
        if now - last_email_time > EMAIL_COOLDOWN:
            print(f"[🔓] MỞ KHOÁ THÀNH CÔNG cho '{OWNER_NAME}'! Đang gửi email...")
            send_unlock_email(OWNER_NAME)
            last_email_time = now
    else:
        # Hiển thị tiến trình đang quét
        progress = f"DANG KIEM TRA... ({unlock_frame_count}/{UNLOCK_HOLD_FRAMES})"
        cv.putText(frame, progress, (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

    # Thanh trạng thái phía dưới
    status_color = (0, 200, 0) if is_unlocked else (0, 80, 200)
    status_text  = "TRANG THAI: MO KHOA" if is_unlocked else "TRANG THAI: KHOA"
    cv.putText(frame, status_text, (10, frame.shape[0] - 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)

    cv.imshow("Mo khoa bang khuon mat", frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        is_unlocked        = False
        unlock_frame_count = 0
        print("[*] Đã reset khoá.")

cap.release()
cv.destroyAllWindows()
print("\n[*] Đã tắt ứng dụng.")