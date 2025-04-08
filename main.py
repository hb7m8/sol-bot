import logging
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

token = "7274703997:AAFeiFY2OOVH5lKf4f7Y3jbWAtJRPeDJNeM"
data_file = "solbot_data.json"

def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"status": "جاهز", "progress": "0%"}

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك في سول بوت! ارسل /help لعرض الأوامر.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
أوامر سول بوت:
/start - بدء البوت
/status - عرض الحالة الحالية
/setprogress <نسبة> - تحديث التقدم
/setstatus <نص> - تحديث الحالة
""")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"الحالة: {data['status']}, التقدم: {data['progress']}")

async def setprogress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("اكتب النسبة بعد الأمر مثل: /setprogress 50%")
        return
    data['progress'] = context.args[0]
    save_data(data)
    await update.message.reply_text(f"تم تحديث التقدم إلى: {data['progress']}")

async def setstatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("اكتب الحالة بعد الأمر مثل: /setstatus قيد العمل")
        return
    data['status'] = " ".join(context.args)
    save_data(data)
    await update.message.reply_text(f"تم تحديث الحالة إلى: {data['status']}")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("setprogress", setprogress))
app.add_handler(CommandHandler("setstatus", setstatus))

if __name__ == '__main__':
    print("تم تشغيل سول بوت...")
    app.run_polling()