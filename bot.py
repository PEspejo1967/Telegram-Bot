import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configurar el logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener el TOKEN desde el entorno (asegúrate de que está configurado correctamente)
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("El TOKEN no está configurado correctamente.")
    exit(1)

# Función de inicio para responder al comando /start
async def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name  # Obtener el nombre del usuario
    welcome_message = f"¡Hola {user_name}! Bienvenido a nuestro servicio. ¿En qué puedo ayudarte hoy?"
    await update.message.reply_text(welcome_message)

# Función para responder automáticamente a cualquier mensaje
async def auto_reply(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name  # Obtener el nombre del usuario
    response_message = f"Hola {user_name}, gracias por contactarnos. Estoy aquí para ayudarte. ¿Cómo puedo asistirte hoy?"
    await update.message.reply_text(response_message)

# Crear la aplicación de Telegram con el TOKEN
application = Application.builder().token(TOKEN).build()

# Agregar el handler para el comando /start
application.add_handler(CommandHandler("start", start))

# Agregar el handler para todos los mensajes de texto (no comandos)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

# Ejecutar el bot
if __name__ == "__main__":
    application.run_polling(allowed_updates=Update.ALL_TYPES)
