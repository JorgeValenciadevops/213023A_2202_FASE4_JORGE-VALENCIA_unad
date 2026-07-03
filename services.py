"""
services.py - Gestión de servicios

Funciona para:
- Catálogo de salas
- Catálogo de equipos
- Catálogo de servicios adicionales
- Consultar disponibilidad
"""

from data import salas, equipos, servicios, reservas
import logger

# ============== SALAS ==============

def obtener_salas():
    """
    Obtiene el catálogo de salas disponibles.
    
    Returns:
        dict: Diccionario con todas las salas
    """
    return salas

def obtener_sala(id_sala):
    """
    Obtiene información de una sala específica.
    
    Args:
        id_sala (int): ID de la sala
    
    Returns:
        dict: Datos de la sala o None si no existe
    """
    return salas.get(id_sala, None)

def sala_disponible(id_sala, fecha_inicio, fecha_fin):
    """
    Verifica si una sala está disponible en un rango de fechas.
    
    Args:
        id_sala (int): ID de la sala
        fecha_inicio (str): Fecha de inicio (formato: YYYY-MM-DD HH:MM)
        fecha_fin (str): Fecha de fin (formato: YYYY-MM-DD HH:MM)
    
    Returns:
        bool: True si la sala está disponible
    """
    if id_sala not in salas:
        logger.registrar_error(f"Sala {id_sala} no existe")
        return False
    
    # Verificar conflictos con reservas existentes
    for reserva in reservas:
        if (reserva["tipo"] == "sala" and 
            reserva["id_servicio"] == id_sala and 
            reserva["estado"] != "cancelada"):
            
            # Comparación simple de fechas
            if not (fecha_fin <= reserva["fecha_inicio"] or 
                    fecha_inicio >= reserva["fecha_fin"]):
                return False
    
    return True

# ============== EQUIPOS ==============

def obtener_equipos():
    """
    Obtiene el catálogo de equipos disponibles.
    
    Returns:
        dict: Diccionario con todos los equipos
    """
    return equipos

def obtener_equipo(id_equipo):
    """
    Obtiene información de un equipo específico.
    
    Args:
        id_equipo (int): ID del equipo
    
    Returns:
        dict: Datos del equipo o None si no existe
    """
    return equipos.get(id_equipo, None)

def equipo_disponible(id_equipo, fecha_inicio, fecha_fin):
    """
    Verifica si un equipo está disponible en un rango de fechas.
    
    Args:
        id_equipo (int): ID del equipo
        fecha_inicio (str): Fecha de inicio
        fecha_fin (str): Fecha de fin
    
    Returns:
        bool: True si el equipo está disponible
    """
    if id_equipo not in equipos:
        logger.registrar_error(f"Equipo {id_equipo} no existe")
        return False
    
    # Verificar conflictos con reservas existentes
    for reserva in reservas:
        if (reserva["tipo"] == "equipo" and 
            reserva["id_servicio"] == id_equipo and 
            reserva["estado"] != "cancelada"):
            
            if not (fecha_fin <= reserva["fecha_inicio"] or 
                    fecha_inicio >= reserva["fecha_fin"]):
                return False
    
    return True

# ============== SERVICIOS ADICIONALES ==============

def obtener_servicios():
    """
    Obtiene el catálogo de servicios adicionales.
    
    Returns:
        dict: Diccionario con todos los servicios
    """
    return servicios

def obtener_servicio(id_servicio):
    """
    Obtiene información de un servicio específico.
    
    Args:
        id_servicio (int): ID del servicio
    
    Returns:
        dict: Datos del servicio o None si no existe
    """
    return servicios.get(id_servicio, None)

# ============== CONSULTAS DE DISPONIBILIDAD ==============

def obtener_disponibilidad(tipo_servicio, fecha_inicio, fecha_fin):
    """
    Obtiene lista de servicios disponibles en un rango de fechas.
    
    Args:
        tipo_servicio (str): Tipo de servicio ("sala", "equipo", "servicio")
        fecha_inicio (str): Fecha de inicio
        fecha_fin (str): Fecha de fin
    
    Returns:
        list: Lista de IDs de servicios disponibles
    """
    disponibles = []
    
    try:
        if tipo_servicio == "sala":
            for id_sala in salas.keys():
                if sala_disponible(id_sala, fecha_inicio, fecha_fin):
                    disponibles.append(id_sala)
        
        elif tipo_servicio == "equipo":
            for id_equipo in equipos.keys():
                if equipo_disponible(id_equipo, fecha_inicio, fecha_fin):
                    disponibles.append(id_equipo)
        
        elif tipo_servicio == "servicio":
            disponibles = list(servicios.keys())
        
        logger.registrar_evento(f"Consulta de disponibilidad: {tipo_servicio}")
        return disponibles
    
    except Exception as e:
        logger.registrar_error(f"Error en consulta de disponibilidad: {str(e)}")
        return []

def calcular_precio(tipo_servicio, id_servicio, cantidad, fecha_inicio, fecha_fin):
    """
    Calcula el precio de un servicio.
    
    Args:
        tipo_servicio (str): Tipo de servicio
        id_servicio (int): ID del servicio
        cantidad (int): Cantidad o duración
        fecha_inicio (str): Fecha de inicio
        fecha_fin (str): Fecha de fin
    
    Returns:
        float: Precio total o -1 si hay error
    """
    try:
        if tipo_servicio == "sala" and id_servicio in salas:
            precio_hora = salas[id_servicio]["precio_hora"]
            # Simplificación: calcular horas (cantidad)
            return precio_hora * cantidad
        
        elif tipo_servicio == "equipo" and id_servicio in equipos:
            precio_dia = equipos[id_servicio]["precio_dia"]
            return precio_dia * cantidad
        
        elif tipo_servicio == "servicio" and id_servicio in servicios:
            precio = servicios[id_servicio]["precio"]
            return precio * cantidad
        
        return -1
    
    except Exception as e:
        logger.registrar_error(f"Error al calcular precio: {str(e)}")
        return -1
