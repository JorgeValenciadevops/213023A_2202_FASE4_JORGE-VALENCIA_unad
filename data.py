"""
data.py - Estructuras de datos del programa

Contiene las estructuras de datos principales (listas, diccionarios y matrices)
para almacenar información de clientes, servicios y reservas.
"""

# Diccionario para almacenar clientes
# Formato: {id_cliente: {"nombre": str, "email": str, "telefono": str, "activo": bool}}
clientes = {}

# Diccionario para almacenar salas
# Formato: {id_sala: {"nombre": str, "capacidad": int, "precio_hora": float}}
salas = {
    1: {"nombre": "Sala de Conferencias A", "capacidad": 20, "precio_hora": 50.0},
    2: {"nombre": "Sala de Conferencias B", "capacidad": 30, "precio_hora": 70.0},
    3: {"nombre": "Sala de Reuniones", "capacidad": 10, "precio_hora": 30.0},
}

# Diccionario para almacenar equipos
# Formato: {id_equipo: {"nombre": str, "descripcion": str, "precio_dia": float}}
equipos = {
    1: {"nombre": "Proyector", "descripcion": "Proyector de alta resolución", "precio_dia": 25.0},
    2: {"nombre": "Pantalla LED", "descripcion": "Pantalla LED 4K", "precio_dia": 40.0},
    3: {"nombre": "Micrófono", "descripcion": "Sistema de audio profesional", "precio_dia": 15.0},
}

# Diccionario para almacenar servicios adicionales
# Formato: {id_servicio: {"nombre": str, "descripcion": str, "precio": float}}
servicios = {
    1: {"nombre": "Catering", "descripcion": "Servicio de alimentos y bebidas", "precio": 100.0},
    2: {"nombre": "Estacionamiento", "descripcion": "Acceso a parqueadero", "precio": 20.0},
    3: {"nombre": "Limpieza", "descripcion": "Limpieza post-evento", "precio": 50.0},
}

# Lista para almacenar reservas
# Formato: {"id_reserva": int, "id_cliente": int, "tipo": str, "id_servicio": int, 
#          "fecha_inicio": str, "fecha_fin": str, "cantidad": int, "estado": str, "precio_total": float}
reservas = []

# Contador para generar IDs únicos
id_cliente_contador = 1
id_reserva_contador = 1
