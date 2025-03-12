from telethon import TelegramClient, events
import asyncio
import datetime
import requests
import time
import re

# Configuración del cliente de Telegram
api_id = 26404425
api_hash = "fc0c129e052be978536a586d60f05dbf"

# Cargar sesión previamente creada
client = TelegramClient("fabrica_session", api_id, api_hash)

# Diccionario de etiquetas por equipo
etiquetas_por_equipo = {
    "1": "Ainoha Ortega",
    "2": "Daniel Ortega️",
    "3": "Nuria Ortega",
    "4": "Ana Paula Montes"
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

# Función para enviar un "ping" cada cierto tiempo para mantener vivo el bot
def keep_alive():
    while True:
        try:
            # Aquí puedes usar un endpoint de un servicio web para mantener vivo el bot
            requests.get("https://www.render.com")  # Cambia por tu URL
            print("🔄 Ping enviado para mantener vivo el bot.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error enviando ping: {e}")
        time.sleep(60 * 10)  # Enviar ping cada 10 minutos

async def main():
    await client.start()
    print("✅ Bot iniciado en Render.")

    me = await client.get_me()

    @client.on(events.NewMessage(outgoing=True))  # Mensajes enviados manualmente
    async def handler_outgoing(event):
        sender = await event.get_sender()

        # Verificar si el mensaje es automático
        if event.message.text not in [mensaje_auto, mensaje_fuera_de_horario]:
            # Asigna la etiqueta por defecto si no hay un equipo asignado
            equipo = getattr(sender, 'username', 'PC-DESCONOCIDO')  # Nombre de usuario, si está disponible
            etiqueta = etiquetas_por_equipo.get(equipo)  # Obtiene la etiqueta para el equipo

            mensaje_modificado = f"{etiqueta} {event.message.text} (primero: {equipo})"
            await event.edit(mensaje_modificado)  # Edita el mensaje para incluir el equipo y la etiqueta

    @client.on(events.NewMessage(incoming=True))  # Mensajes entrantes
    async def handler_incoming(event):
        if event.is_private:
            sender = await event.get_sender()
            print(f"📩 Mensaje recibido de {sender.first_name}")

            if event.sender_id != me.id:
                if esta_fuera_de_horario():
                    await event.respond(mensaje_fuera_de_horario)
                else:
                    # Buscar el hashtag en el mensaje
                    match = re.search(r"#(\d+)", event.message.text)  # Busca el hashtag seguido de números
                    if match:
                        equipo_numero = match.group(1)  # Obtiene el número del hashtag
                        etiqueta = etiquetas_por_equipo.get(equipo_numero, "Equipo desconocido")
                        mensaje_con_etiqueta = f"{etiqueta}: {event.message.text}"
                        await event.respond(mensaje_con_etiqueta)
                    else:
                        await event.respond(mensaje_auto)

    # Ejecuta el keep-alive en un hilo separado para que no bloquee el bot
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, keep_alive)

    await client.run_until_disconnected()

asyncio.run(main())
