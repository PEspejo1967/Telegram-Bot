from telethon import TelegramClient, events
import asyncio

# Reemplaza con tus credenciales
api_id = 26404425
api_hash = "fc0c129e052be978536a586d60f05dbf"
phone_number = "+34630420866"

# Mensaje automático
mensaje_auto = "Hola, gracias por contactarnos. En breve te responderemos."

async def main():
    # Iniciar cliente con sesión de tu cuenta
    client = TelegramClient("fabrica_session", api_id, api_hash)

    await client.start(phone_number)

    # Escuchar mensajes privados recibidos
    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        # Verificar que sea un mensaje de un usuario y no de un grupo
        if event.is_private:
            sender = await event.get_sender()
            print(f"Mensaje recibido de {sender.first_name}")
            await event.respond(mensaje_auto)

    print("Esperando mensajes...")
    await client.run_until_disconnected()

asyncio.run(main())
