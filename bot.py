from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7626661581:AAEP4q1QAvsprXh-WMTNew1-UYtdBqmxWmU"

async def start(update: Update, context: CallbackContext):
    """Responde cuando el usuario inicia una conversación con /start."""
    await update.message.reply_text("¡Hola! Soy el bot de la empresa. ¿En qué puedo ayudarte?")

async def echo(update: Update, context: CallbackContext):
    """Repite cualquier mensaje que reciba."""
    await update.message.reply_text(update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot en funcionamiento...")
    app.run_polling()

if __name__ == "__main__":
    main()
