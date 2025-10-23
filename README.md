# 🤖 FB UID Checker Bot (Chạy trên GitHub Actions - Tiếng Việt)
Bot Telegram kiểm tra UID Facebook (live/die) qua Graph API.

## 🚀 Tính năng
- Nhận nhiều UID cùng lúc
- Kiểm tra song song nhanh
- Trả kết quả Alive ✅ / Dead ❌
- Chạy auto 24/7 bằng GitHub Actions

## ⚙️ Cách cài
1. Tạo repo mới trên [GitHub](https://github.com/new)
2. Upload toàn bộ file từ gói này
3. Vào **Settings → Secrets → Actions** thêm:
```
TELEGRAM_TOKEN=Token từ @BotFather
FB_TOKEN=APP_ID|APP_SECRET hoặc user token
```
4. Vào tab **Actions** → chọn workflow → **Run workflow**.

Bot auto chạy lại mỗi 6 tiếng.

## 💬 Dùng bot
- `/start`
- Gửi danh sách UID: `123,456,789`
- Hoặc file `uids.txt` (1 dòng 1 UID)
- Bot trả kết quả chi tiết.

## ⚠️ Lưu ý
- Token Facebook có thể hết hạn, cần cập nhật.
- Không nên spam quá nhiều UID liên tục.
