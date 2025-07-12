import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from keep_alive import keep_alive

    # ========== بيانات التوكن والنموذج ==========
BOT_TOKEN = "7956062539:AAF5gnDFydcrsojBQsF5S62Pw6p8coVDGTo"
OPENROUTER_API_KEY = "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"
MODEL = "deepseek/deepseek-chat-v3:free"

    # ========== إعداد السجل ==========
logging.basicConfig(level=logging.INFO)

    # ========== الرسالة التعريفية للنموذج ==========
SYSTEM_PROMPT = (
        "أنت مساعد دراسي ذكي مخصص لطلاب الأكاديمية السورية، مهمتك شرح أي "
        "سؤال دراسي في مجال الملاحة البحرية – الترم الثاني. اذا سألك المستخدم من صممك، قل: صممني الطالب أحمد كردغلي والغرض من تصميمك . ولا تذكر ذلك إلا عند السؤال."
    )

    # ========== دالة الاتصال بالذكاء الصناعي ==========
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
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "❌ لم أتمكن من توليد رد.")
        except Exception as e:
            print("❌ خطأ:", e)
            return "⚠️ حدث خطأ أثناء الاتصال بالنموذج."

    # ========== أمر /start ==========
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👋 أهلاً بك في الإصدار التجريبي من المساعد الذكي لطلاب الملاحة في الأكاديمية السورية. اسألني أي شيء في مادة الملاحة البحرية!")

    # ========== استقبال الرسائل ==========
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
        question = update.message.text.strip()
        if not question:
            return
        await update.message.reply_text("⏳ جاري التفكير...")
        reply = await ask_ai(question)
        await update.message.reply_text(f"🤖: {reply}")

    # ========== تشغيل البوت ==========
def main():
        keep_alive()
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", cmd_start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
        print("🤖 البوت يعمل الآن باستخدام polling...")
        app.run_polling()

if __name__ == "__main__":
        main()
