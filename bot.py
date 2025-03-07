from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

# Habilitar el logging para errores
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Función que maneja el comando /start
def start(update, context):
    update.message.reply_text('¡Hola! Soy tu bot de Telegram.')

# Función para manejar mensajes
def echo(update, context):
    update.message.reply_text(update.message.text)

# Manejo de errores
def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # Obtén el token de las variables de entorno (asegúrate de que esté configurado correctamente)
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        print("El TOKEN no está configurado. Por favor, configura la variable de entorno TELEGRAM_TOKEN.")
        return

    # Crea el Updater y pasa el token del bot
    updater = Updater(token, use_context=True)
    
    # Obtén el dispatcher para registrar los handlers
    dispatcher = updater.dispatcher
    
    # Agregar los manejadores de comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Registra el manejador de errores
    dispatcher.add_error_handler(error)

    # Inicia el bot
    updater.start_polling()

    # Corre el bot hasta que lo detengas
    updater.idle()

if __name__ == '__main__':
    main()
