import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# تنظیمات محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS_ENV = os.getenv("ADMIN_IDS", "")  # مثلاً: 123456789,987654321

# تبدیل رشته ادمین‌ها به لیست عدد صحیح
ADMIN_IDS = []
if ADMIN_IDS_ENV:
    try:
        ADMIN_IDS = [int(uid.strip()) for uid in ADMIN_IDS_ENV.split(",") if uid.strip()]
    except ValueError as e:
        print(f"خطا در تبدیل ADMIN_IDS: {e}")
        exit(1)

# لاگینگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    await update.message.reply_text("ربات فعال شد! لینک یا هر متنی که می‌خواهید بفرستید.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش تمام پیام‌های متنی (به جز دستورات)"""
    user_id = update.effective_user.id

    # اگر هیچ ادمینی تنظیم نشده بود
    if not ADMIN_IDS:
        await update.message.reply_text("⚠️ ADMIN_IDS تنظیم نشده است!")
        return

    # چک کردن دسترسی
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ شما دسترسی استفاده از این ربات را ندارید.")
        return

    text = update.message.text or "پیام بدون متن"

    # برای جلوگیری از اسپم خیلی طولانی
    preview = text if len(text) <= 100 else text[:100] + "..."

    await update.message.reply_text(
        f"دریافت شد:\n\n<pre>{preview}</pre>\n\n"
        f"طول پیام: {len(text)} کاراکتر\n"
        f"ربات آمادهٔ پردازش بعدی است!",
        parse_mode="HTML",
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """لاگ کردن خطاها"""
    logger.error(msg="خطایی رخ داد:", exc_info=context.error)

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN تنظیم نشده است!")
        return

    if not ADMIN_IDS:
        print("⚠️  هیچ ADMIN_IDS تنظیم نشده! ربات فقط به ادمین‌های مشخص‌شده پاسخ می‌دهد.")
        print("   برای تنظیم چند ادمین از کاما استفاده کنید، مثال:")
        print("   ADMIN_IDS=123456789,987654321")

    app = Application.builder().token(BOT_TOKEN).build()

    # هندلرها
    app.add_handler(CommandHandler("start", start))
    # فقط پیام‌های متنی که دستور نیستند
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # هندلر خطا
    app.add_error_handler(error_handler)

    print("ربات در حال اجرا است...")
    print(f"ادمین‌های مجاز: {ADMIN_IDS or 'هیچ‌کس'}")

    # شروع پولینگ
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
