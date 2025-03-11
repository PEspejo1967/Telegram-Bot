from telethon import TelegramClient, events
import asyncio

# No necesitas ingresar manualmente el número, solo usa el archivo de sesión
api_id = 26404425
api_hash = "fc0c129e052be978536a586d60f05dbf"

# Cargar sesión previamente creada
client = TelegramClient("fabrica_session", api_id, api_hash)

# Mensajes automáticos
mensaje_fuera_de_horario = """¡Hola! 👋

Gracias por escribirnos a P. Espejo. Actualmente, estamos fuera de nuestro horario laboral, pero hemos recibido tu mensaje y lo atenderemos en cuanto volvamos a estar disponibles.

Nuestro horario de atención es:
- *Lunes a jueves*: 9:00h a 13:00h y 15:30h a 18:30h.
- *Viernes*: 8:00h a 14:00h.

Te responderemos a la brevedad posible dentro de estos horarios. ¡Gracias por tu comprensión! Que tengas un excelente día. 😊"""

mensaje_fuera_de_linea = """Hola! 👋

Gracias por contactarnos. Nos pondremos en contacto contigo lo antes posible.
- *Ainoha Ortega*: ainoha@grupoespejo.net
- *Daniel Ortega*: daniel@grupoespejo.net
- *Nuria Ortega*: nuria@grupoespejo.net
- *Ana Paula Montes*: anapaula@grupoespejo.net
- *Manuel Ibáñez*: manuel@grupoespejo.net
- *Rafael Gutiérrez*: rafa@grupoespejo.net
- *María Dolores*: mariadolores@grupoespejo.net

¡Que tengas un excelente día! 😊"""




# Función para comprobar si estamos dentro del horario de oficina
def dentro_de_horario():
    ahora = datetime.datetime.now()
    dia = ahora.weekday()
    hora = ahora.hour
    minuto = ahora.minute

    # Lunes a jueves: 9:00h a 13:00h y 15:30h a 18:30h
    if dia in [0, 1, 2, 3]:  # Lunes a jueves
        if (9 <= hora < 13) or (15 <= hora < 18) or (hora == 13 and minuto == 0) or (hora == 18 and minuto == 30):
            return True
    # Viernes: 8:00h a 14:00h
    if dia == 4:  # Viernes
        if 8 <= hora < 14:
            return True
    return False

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
            
            if dentro_de_horario():
                # Enviar mensaje si estamos dentro del horario y no estamos en línea
                if not client.is_connected():
                    await event.respond(mensaje_fuera_de_linea)
            else:
                # Enviar mensaje fuera de horario
                await event.respond(mensaje_fuera_de_horario)

    print("Esperando mensajes...")
    await client.run_until_disconnected()

asyncio.run(main())