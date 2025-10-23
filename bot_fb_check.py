import os
import re
import aiohttp
import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("8318723160:AAHyS6Ak0zRvqCD5GkchzEWHGjWorrrke7U")
FB_ACCESS_TOKEN = os.getenv("EAAGNO4a7r2wBPyLgahrnYRBnA4qQKZAlY5aofyumyBqHRhPZCwOzCSevSOiaaGpWCxZABbm9OMeYMghSZA4q3KPfnmcw396tQPGI9cTZAqF9feQn33HJtjj4QqGa3ZCiD7EXZCGZCgxbwPpWFvLCywzZCY74Gd9Aa8xOoWkphBvZAUFrUsap7GrcnOoOjfsWmYSHCJtwZDZD")
GRAPH_API_BASE = "https://graph.facebook.com"

def extract_fb_id(text: str) -> str | None:
    text = text.strip()
    match = re.search(r"facebook\.com/(?:pg/|people/)?([^/?#&]+)", text)
    if match:
        return match.group(1)
    if " " not in text:
        return text
    return None

async def fetch_fb_info(session: aiohttp.ClientSession, fb_id: str) -> dict:
    fields = "id,name,about,link,fan_count,followers_count,category,picture"
    params = {"fields": fields, "access_token": FB_ACCESS_TOKEN}
    async with session.get(f"{GRAPH_API_BASE}/{fb_id}", params=params) as resp:
        return await resp.json(), resp.status

async def cmd_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not FB_ACCESS_TOKEN:
        await update.message.reply_text("⚠️ Chưa cấu hình FB_ACCESS_TOKEN.")
        return

    if not context.args:
        await update.message.reply_text("❓ Dùng: /check <link hoặc id Facebook>")
        return

    fb_id = extract_fb_id(context.args[0])
    if not fb_id:
        await update.message.reply_text("Không nhận diện được link hoặc ID Facebook.")
        return

    await update.message.reply_text(f"🔍 Đang kiểm tra `{fb_id}`...", parse_mode="Markdown")

    async with aiohttp.ClientSession() as session:
        data, status = await fetch_fb_info(session, fb_id)

    if status != 200:
        err = data.get("error", {}).get("message", "Không rõ lỗi.")
        await update.message.reply_text(f"❌ Lỗi Facebook API ({status}): {err}")
        return

    name = data.get("name", "Không có")
    about = data.get("about", "Không có mô tả")
    link = data.get("link", f"https://facebook.com/{fb_id}")
    fans = data.get("fan_count", "N/A")
    followers = data.get("followers_count", "N/A")
    category = data.get("category", "Không rõ")
    picture = data.get("picture", {}).get("data", {}).get("url", None)

    caption = (
        f"*{name}*\n"
        f"📂 Thể loại: {category}\n"
        f"👍 Lượt like: {fans}\n"
        f"👥 Lượt theo dõi: {followers}\n"
        f"📝 Mô tả: {about}\n"
        f"🔗 [Xem trang]({link})"
    )

    if picture:
        await update.message.reply_photo(photo=picture, caption=caption, parse_mode="Markdown")
    else:
        await update.message.reply_text(caption, parse_mode="Markdown")

def main():
    if not TELEGRAM_TOKEN:
        print("Thiếu TELEGRAM_TOKEN")
        return
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("check", cmd_check))
    print("✅ Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
