from telethon import TelegramClient, events
import asyncio
import socket 

# No necesitas ingresar manualmente el número, solo usa el archivo de sesión
api_id = 26404425
api_hash = "fc0c129e052be978536a586d60f05dbf"

# Cargar sesión previamente creada
client = TelegramClient("fabrica_session", api_id, api_hash)

# Obtener el nombre del equipo donde se está ejecutando el bot
nombre_equipo = socket.gethostname()

# Mensajes automáticos
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

    # Obtener tu información (id) para identificarte
    me = await client.get_me()

    @client.on(events.NewMessage(outgoing=True))  # Mensajes enviados por ti
    async def handler_outgoing(event):
        # Modificar el mensaje para incluir el nombre del equipo
        mensaje_modificado = f"{event.message.text} (Enviado desde: {nombre_equipo})"
        await event.edit(mensaje_modificado)  # Editamos el mensaje original

    @client.on(events.NewMessage(incoming=True))  # Mensajes recibidos
    async def handler_incoming(event):
        if event.is_private:
            sender = await event.get_sender()
            print(f"📩 Mensaje recibido de {sender.first_name}")
            
            # Si el mensaje no es de ti, responde automáticamente
            if event.sender_id != me.id:
                await event.respond(mensaje_auto)

    await client.run_until_disconnected()

asyncio.run(main())