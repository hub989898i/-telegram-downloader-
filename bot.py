import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    await update.message.reply_text("🤖 ربات فعال شد! لینک بفرستید.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام"""
    user_id = update.effective_user.id
    
    if ADMIN_ID == 0:
        await update.message.reply_text("⚠️ لطفاً ابتدا ADMIN_ID را تنظیم کنید!")
        return
        
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ دسترسی ندارید!")
        return
    
    text = update.message.text
    await update.message.reply_text(f"📩 دریافت شد: {text[:50]}...\n\n✅ ربات آماده است!")

def main():
    """تابع اصلی"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN تنظیم نشده!")
        return
    
    # ساخت اپلیکیشن
    app = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print(f"🤖 ربات در حال اجرا...")
    print(f"📊 ADMIN_ID: {ADMIN_ID}")
    
    # شروع پولینگ
    app.run_polling()

if __name__ == "__main__":
    main()
