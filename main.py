from telethon import TelegramClient, events
import asyncio
import datetime

# Configuración del cliente de Telegram
api_id = 26404425
api_hash = "fc0c129e052be978536a586d60f05dbf"

# Cargar sesión previamente creada
client = TelegramClient("fabrica_session", api_id, api_hash)

# Mapeo de IDs de usuario a nombres de equipo o persona
usuarios_telegram = {
    529061298: "Valcárcel"
}

# Mensajes automáticos
mensaje_fuera_de_horario = """¡Hola! 👋  

Gracias por escribirnos a P. Espejo. Actualmente, estamos fuera de nuestro horario laboral, pero hemos recibido tu mensaje y lo atenderemos en cuanto volvamos a estar disponibles.  

Nuestro horario de atención es:  
- *Lunes a jueves*: 9:00h a 13:00h y 15:30h a 18:30h.  
- *Viernes*: 8:00h a 14:00h.

Te responderemos a la brevedad posible dentro de estos horarios. ¡Gracias por tu comprensión! Que tengas un excelente día. 😊"""

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

# Función para verificar si estamos fuera del horario laboral
def esta_fuera_de_horario():
    ahora = datetime.datetime.now()
    dia_semana = ahora.weekday()  # Lunes = 0, Domingo = 6
    hora_actual = ahora.hour + ahora.minute / 60  # Convierte en decimal

    # Horario laboral
    if dia_semana in [0, 1, 2, 3]:  # Lunes a jueves
        if (9 <= hora_actual < 13) or (15.5 <= hora_actual < 18.5): 
            return False  # Dentro del horario
    elif dia_semana == 4:  # Viernes
        if 8 <= hora_actual < 14:
            return False  # Dentro del horario

    return True  # Fuera de horario

async def main():
    await client.start()
    print("✅ Bot iniciado en Render.")

    me = await client.get_me()

    @client.on(events.NewMessage(outgoing=True))  # Mensajes enviados manualmente
    async def handler_outgoing(event):
        sender_id = event.sender_id
        nombre_usuario = usuarios_telegram.get(sender_id, "PC-DESCONOCIDO")
        
        mensaje_modificado = f"{event.message.text} (Enviado desde: {nombre_usuario})"
        await event.edit(mensaje_modificado)  # Edita el mensaje para incluir el equipo

    @client.on(events.NewMessage(incoming=True))  # Mensajes entrantes
    async def handler_incoming(event):
        if event.is_private:
            sender = await event.get_sender()
            print(f"📩 Mensaje recibido de {sender.first_name}")

            if event.sender_id != me.id:
                if esta_fuera_de_horario():
                    await event.respond(mensaje_fuera_de_horario)
                else:
                    await event.respond(mensaje_auto)

    await client.run_until_disconnected()

asyncio.run(main())
