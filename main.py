from telethon import TelegramClient, events
import asyncio

# No necesitas ingresar manualmente el número, solo usa el archivo de sesión
api_id = TU_API_ID
api_hash = "TU_API_HASH"

# Cargar sesión previamente creada
client = TelegramClient("fabrica_session", api_id, api_hash)

mensaje_auto = """Hola! 👋

Gracias por contactarnos. Nos pondremos en contacto contigo lo antes posible.
- *Ainoha Ortega*: ainoha@grupoespejo.net
- *Daniel Ortega*: daniel@grupoespejo.net
- *Nuria Ortega*: nuria@grupoespejo.net
- *Ana Paula Montes*: anapaula@grupoespejo.net
- *Manuel Ibáñez*: manuel@grupoespejo.net
- *Rafael Gutiérrez*: rafa@grupoespejo.net
- *María Dolores*: mariadolores@grupoespejo.net

¡Que tengas un excelente día! 😊"""

async def main():
    await client.start()  # Carga la sesión guardada
    print("✅ Bot iniciado correctamente.")

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        if event.is_private:
            sender = await event.get_sender()
            print(f"📩 Mensaje recibido de {sender.first_name}")
            await event.respond(mensaje_auto)

    await client.run_until_disconnected()

asyncio.run(main())


