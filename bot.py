import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

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

def start(update: Update, context):
    """دستور /start"""
    update.message.reply_text("🤖 ربات فعال شد! لینک بفرستید.")

def handle_message(update: Update, context):
    """پردازش پیام"""
    user_id = update.effective_user.id
    
    if ADMIN_ID == 0:
        update.message.reply_text("⚠️ ADMIN_ID تنظیم نشده!")
        return
        
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ دسترسی ندارید!")
        return
    
    text = update.message.text
    update.message.reply_text(f"📩 دریافت شد: {text[:50]}...")

def main():
    """تابع اصلی"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN تنظیم نشده!")
        return
    
    # ساخت آپدیت‌کننده
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # گرفتن دیسپچر
    dp = updater.dispatcher
    
    # اضافه کردن هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print(f"🤖 ربات در حال اجرا... ADMIN_ID: {ADMIN_ID}")
    
    # شروع پولینگ
    updater.start_polling()
    
    # اجرا تا Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()
