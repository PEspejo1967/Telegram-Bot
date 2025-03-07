from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "7626661581:AAEP4q1QAvsprXh-WMTNew1-UYtdBqmxWmU"

async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Soy el bot de P. Espejo. ¿En qué puedo ayudarte?")

async def responder(update: Update, context):
    texto = update.message.text
    await update.message.reply_text(f"Has escrito: {texto}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    app.run_polling()

if __name__ == "__main__":
    main()
