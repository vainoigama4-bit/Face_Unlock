# ============================================================
#  CẤU HÌNH HỆ THỐNG MỞ KHOÁ BẰNG KHUÔN MẶT
# ============================================================

# --- Chủ sở hữu (owner) ---
# Đây là tên user_name đã dùng khi thu thập dữ liệu.
# Chỉ khi nhận diện đúng người này, hệ thống mới mở khoá.
OWNER_NAME = "HaGiaBao"   # <--- ĐỔI thành tên của bạn

# --- Cấu hình gửi email thông báo ---
EMAIL_SENDER   = "sukamona3@gmail.com"       # <--- Email của bạn (người gửi)
EMAIL_RECEIVER = "sukamona3@gmail.com"       # <--- Email nhận thông báo (có thể giống người gửi)

# --- Ngưỡng tin cậy của LBPH (thấp = chắc hơn) ---
CONFIDENCE_THRESHOLD = 50   # Dưới 50 → nhận diện được; trên 50 → Unknown

# --- Thời gian chờ giữa các lần gửi email (giây) ---
EMAIL_COOLDOWN = 30   # Tránh gửi liên tục mỗi frame
