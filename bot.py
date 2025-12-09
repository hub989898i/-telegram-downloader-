import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# تنظیمات
BOT_TOKEN = os.getenv("BOT_TOKEN")

# مدیریت ADMIN_ID
admin_id_str = os.getenv("ADMIN_ID", "").strip()
ADMIN_ID = int(admin_id_str) if admin_id_str else 0

# لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update, context):
    """دستور /start"""
    update.message.reply_text("🤖 ربات فعال شد! لینک بفرستید.")

def handle_message(update, context):
    """پردازش پیام"""
    user_id = update.message.from_user.id
    
    if ADMIN_ID == 0:
        update.message.reply_text("⚠️ ADMIN_ID تنظیم نشده!")
        return
        
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ دسترسی ندارید!")
        return
    
    text = update.message.text
    update.message.reply_text(f"📩 دریافت شد: {text[:50]}...")

def error(update, context):
    """لاگ کردن خطاها"""
    logger.warning(f'خطا برای کاربر {update.effective_user.id}: {context.error}')

def main():
    """تابع اصلی"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN تنظیم نشده!")
        return
    
    # ساخت آپدیت‌کننده برای نسخه ۱۳.۷
    updater = Updater(BOT_TOKEN)
    
    # گرفتن دیسپچر
    dp = updater.dispatcher
    
    # اضافه کردن هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    # مدیریت خطا
    dp.add_error_handler(error)
    
    print(f"🤖 ربات در حال اجرا... ADMIN_ID: {ADMIN_ID}")
    
    # شروع پولینگ
    updater.start_polling()
    
    # اجرا تا Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()
