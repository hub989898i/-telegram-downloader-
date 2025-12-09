import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

# مدیریت ADMIN_ID
admin_id_str = os.getenv("ADMIN_ID", "").strip()
ADMIN_ID = int(admin_id_str) if admin_id_str else 0

def start(update, context):
    update.message.reply_text("🤖 ربات فعال شد! لینک بفرستید.")

def handle_message(update, context):
    user_id = update.message.from_user.id
    
    if ADMIN_ID == 0:
        update.message.reply_text("⚠️ لطفاً ابتدا ADMIN_ID را تنظیم کنید!")
        return
        
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ دسترسی ندارید!")
        return
    
    text = update.message.text
    update.message.reply_text(f"📩 دریافت شد: {text[:50]}...\n\n✅ ربات آماده است!")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN تنظیم نشده!")
        return
    
    # برای نسخه 13.15
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.Filters.text, handle_message))
    
    print(f"🤖 ربات در حال اجرا...")
    print(f"📊 ADMIN_ID: {ADMIN_ID}")
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
