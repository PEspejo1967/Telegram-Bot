import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configurar el logging para ver mensajes en la consola de Render
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Obtener el token desde la variable de entorno
TOKEN = os.getenv("7626661581:AAEP4q1QAvsprXh-WMTNew1-UYtdBqmxWmU")

# Verificar que el token existe
if not TOKEN:
    logger.error("El TOKEN no está configurado correctamente.")
    exit(1)

# Función para responder al comando /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("¡Hola! Soy un bot de Telegram funcionando en Render 🚀.")

# Función para responder mensajes de texto
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Has dicho: {update.message.text}")

# Configurar la aplicación de Telegram
def main():
    app = Application.builder().token(TOKEN).build()

    # Agregar manejadores de comandos y mensajes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Iniciar el bot
    logger.info("Bot en funcionamiento...")
    app.run_polling()

# Ejecutar el bot
if __name__ == "__main__":
    main()
