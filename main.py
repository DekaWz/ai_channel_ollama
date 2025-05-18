from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import ai

inteleg = ai.ai()

BOT_TOKEN = ""
CHANNEL_ID = ""
YOUR_USER_ID = int()


async def send_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_USER_ID:
        await update.message.reply_text("🚫 Доступ запрещен!")
        return
    
    context.user_data["awaiting_message"] = True
    await update.message.reply_text(
        "📝 Отправьте текст сообщения, которое нужно опубликовать в канале\n"
        "❌ Чтобы отменить, отправьте /cancel"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (
        update.effective_user.id == YOUR_USER_ID
        and context.user_data.get("awaiting_message")
        and update.message.text
    ):
        try:

            text = await inteleg.chat(update.message.text)

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=text,
		parse_mode = "markdown"
            )
            await update.message.reply_text("✅ Сообщение успешно опубликовано!")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        
        context.user_data.pop("awaiting_message", None)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == YOUR_USER_ID:
        context.user_data.pop("awaiting_message", None)
        await update.message.reply_text("❌ Операция отменена")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("send", send_command))
    app.add_handler(CommandHandler("cancel", cancel_command))

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))

    app.run_polling()

if __name__ == "__main__":
    main()
