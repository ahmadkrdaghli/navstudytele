import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# بيانات التوكن والنموذج
BOT_TOKEN = "B0T_TOKEN"
OPENROUTER_API_KEY = "OPENROUTER_API_KEY"
MODEL = "deepseek/deepseek-chat-v3:free"

# تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# رسالة النظام
SYSTEM_PROMPT = (
    "أنت مساعد دراسي ذكي مخصص لطلاب الأكاديمية السورية، مهمتك شرح أي "
    "سؤال دراسي في مجال الملاحة البحرية – الترم الثاني. "
    "إذا سألك المستخدم من صممك، قل: صممني الطالب أحمد كردغلي. ولا تذكر ذلك إلا عند السؤال."
)

# دالة الاتصال بالنموذج
async def ask_ai(question: str) -> str:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ]
            },
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "❌ لم أتمكن من توليد رد.")
    except Exception as e:
        print("❌ استثناء أثناء الاتصال:", e)
        return "⚠️ حدث خطأ أثناء الاتصال بالنموذج."

# أمر البدء
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في الإصدار التجريبي من المساعد الذكي لطلاب الملاحة في الأكاديمية السورية. اسألني أي شيء!"
    )

# التعامل مع الرسائل
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text.strip()
    if not question:
        return
    await update.message.reply_text("⏳ جاري التفكير...")
    reply = await ask_ai(question)
    await update.message.reply_text(f"🤖: {reply}")

# تشغيل البوت باستخدام polling
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

    print("🤖 البوت يعمل الآن باستخدام polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
