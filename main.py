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

    # Obtener tu información (id) para usarla en la comparación
    me = await client.get_me()

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        if event.is_private:
            sender = await event.get_sender()
            print(f"📩 Mensaje recibido de {sender.first_name}")
            
            # Si el mensaje no es de ti, el bot responde automáticamente
            if event.sender_id != me.id:  # Si el mensaje no es de ti
                await event.respond(mensaje_auto)
                await event.respond(mensaje_modificado)
            else:
                # Si es un mensaje tuyo (estás enviando), agregar el nombre del equipo
                mensaje_modificado = f"Este mensaje fue enviado desde el equipo: {nombre_equipo}. {event.message.text}"
                
                # Responder con el mensaje modificado
                await event.respond(mensaje_modificado)

    await client.run_until_disconnected()

asyncio.run(main())