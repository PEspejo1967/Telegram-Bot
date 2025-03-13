from telethon import TelegramClient, events
import asyncio
import datetime
import re
from fastapi import FastAPI
import uvicorn
import threading

# Configuración del cliente de Telegram
api_id = 26404425
api_hash = "fc0c129e052be978536a586d60f05dbf"

# Cargar sesión previamente creada
client = TelegramClient("fabrica_session", api_id, api_hash)

# Servidor FastAPI para UptimeRobot
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot activo 🚀"}

# Ejecutar el servidor en un hilo separado
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Diccionario de etiquetas por equipo
etiquetas_por_equipo = {
    "1": "Ainoha Ortega",
    "2": "Daniel Ortega️",
    "3": "Nuria Ortega",
    "4": "Ana Paula Montes",
    "5": "Manuel Ibáñez",
    "6": "Rafael Gutiérrez",
    "7": "María Dolores"    
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

# Diccionario para registrar la última vez que se envió el mensaje automático a cada usuario
ultima_interaccion = {}

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

    # Escuchar mensajes enviados por empleados
    @client.on(events.NewMessage(outgoing=True))  
    async def handler_outgoing(event):
        # Buscar un hashtag seguido de un número en el mensaje enviado
        match = re.search(r"#(\d+)\s+(.*)", event.message.text)  
        if match:
            equipo_numero = match.group(1)  # Número del hashtag
            mensaje_original = match.group(2)  # Mensaje sin el hashtag

            # Buscar el nombre del empleado que responde
            nombre_empleado = etiquetas_por_equipo.get(equipo_numero, "Empleado desconocido")

            # Formatear el mensaje para incluir la referencia
            mensaje_modificado = f"{mensaje_original} (respondió {nombre_empleado})"

            # Editar el mensaje original
            await event.edit(mensaje_modificado)

    # Escuchar mensajes entrantes de clientes
    @client.on(events.NewMessage(incoming=True))  
    async def handler_incoming(event):
        if event.is_private:
            sender = await event.get_sender()
            sender_id = event.sender_id
            print(f"📩 Mensaje recibido de {sender.first_name}")

            if event.sender_id != me.id:
                hoy = datetime.datetime.now().strftime("%Y-%m-%d")  # Fecha en formato YYYY-MM-DD

                # Verificar si el usuario ya recibió el mensaje hoy
                if sender_id not in ultima_interaccion or ultima_interaccion[sender_id] != hoy:
                    if esta_fuera_de_horario():
                        await event.respond(mensaje_fuera_de_horario)
                    else:
                        await event.respond(mensaje_auto)
                    
                    # Guardar la fecha de última interacción
                    ultima_interaccion[sender_id] = hoy

    await client.run_until_disconnected()

asyncio.run(main())
