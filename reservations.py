"""
reservations.py - Gestión de reservas

Funciones para:
- Crear reservas
- Cancelar reservas
- Consultar reservas
"""

from datetime import datetime

from data import reservas, id_reserva_contador
from customers import validar_cliente_existente
from services import sala_disponible, equipo_disponible, calcular_precio
import logger


def validar_rango_fechas(fecha_inicio, fecha_fin):
    """Valida que la fecha de fin sea mayor que la de inicio."""
    if isinstance(fecha_inicio, str):
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d %H:%M")
    else:
        fecha_inicio_dt = fecha_inicio

    if isinstance(fecha_fin, str):
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d %H:%M")
    else:
        fecha_fin_dt = fecha_fin

    if fecha_fin_dt <= fecha_inicio_dt:
        raise ValueError("La fecha de fin debe ser mayor que la fecha de inicio.")

    return True


def crear_reserva(id_cliente, tipo_servicio, id_servicio, fecha_inicio, fecha_fin, cantidad=1):
    """
    Crea una nueva reserva.
    
    Args:
        id_cliente (int): ID del cliente
        tipo_servicio (str): Tipo de servicio ("sala", "equipo", "servicio")
        id_servicio (int): ID del servicio a reservar
        fecha_inicio (str): Fecha de inicio (formato: YYYY-MM-DD HH:MM)
        fecha_fin (str): Fecha de fin (formato: YYYY-MM-DD HH:MM)
        cantidad (int): Cantidad o duración
    
    Returns:
        int: ID de la reserva o -1 si hay error
    """
    try:
        validar_rango_fechas(fecha_inicio, fecha_fin)

        # Validar cliente
        if not validar_cliente_existente(id_cliente):
            logger.registrar_error(f"Cliente {id_cliente} no existe o no está activo")
            return -1
        
        # Validar disponibilidad
        if tipo_servicio == "sala":
            if not sala_disponible(id_servicio, fecha_inicio, fecha_fin):
                logger.registrar_advertencia(f"Sala {id_servicio} no disponible")
                return -1
        
        elif tipo_servicio == "equipo":
            if not equipo_disponible(id_servicio, fecha_inicio, fecha_fin):
                logger.registrar_advertencia(f"Equipo {id_servicio} no disponible")
                return -1
        
        # Calcular precio
        precio_total = calcular_precio(tipo_servicio, id_servicio, cantidad, fecha_inicio, fecha_fin)
        if precio_total < 0:
            logger.registrar_error(f"Error al calcular precio para {tipo_servicio} {id_servicio}")
            return -1
        
        # Crear reserva
        from data import id_reserva_contador as contador
        nueva_reserva = {
            "id_reserva": contador,
            "id_cliente": id_cliente,
            "tipo": tipo_servicio,
            "id_servicio": id_servicio,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "cantidad": cantidad,
            "estado": "activa",
            "precio_total": precio_total
        }
        
        reservas.append(nueva_reserva)
        logger.registrar_evento(f"Reserva creada: ID {contador}, Cliente {id_cliente}, {tipo_servicio} {id_servicio}")
        
        return contador
    
    except Exception as e:
        logger.registrar_error(f"Error al crear reserva: {str(e)}")
        return -1

def cancelar_reserva(id_reserva):
    """
    Cancela una reserva existente.
    
    Args:
        id_reserva (int): ID de la reserva a cancelar
    
    Returns:
        bool: True si se canceló exitosamente
    """
    try:
        for reserva in reservas:
            if reserva["id_reserva"] == id_reserva:
                if reserva["estado"] == "cancelada":
                    logger.registrar_advertencia(f"Reserva {id_reserva} ya está cancelada")
                    return False
                
                reserva["estado"] = "cancelada"
                logger.registrar_evento(f"Reserva cancelada: ID {id_reserva}")
                return True
        
        logger.registrar_error(f"Reserva {id_reserva} no encontrada")
        return False
    
    except Exception as e:
        logger.registrar_error(f"Error al cancelar reserva: {str(e)}")
        return False

def obtener_reserva(id_reserva):
    """
    Obtiene información de una reserva específica.
    
    Args:
        id_reserva (int): ID de la reserva
    
    Returns:
        dict: Datos de la reserva o None si no existe
    """
    for reserva in reservas:
        if reserva["id_reserva"] == id_reserva:
            return reserva
    return None

def obtener_reservas_cliente(id_cliente):
    """
    Obtiene todas las reservas de un cliente.
    
    Args:
        id_cliente (int): ID del cliente
    
    Returns:
        list: Lista de reservas del cliente
    """
    return [r for r in reservas if r["id_cliente"] == id_cliente]

def obtener_reservas_activas():
    """
    Obtiene todas las reservas activas.
    
    Returns:
        list: Lista de reservas activas
    """
    return [r for r in reservas if r["estado"] == "activa"]

def obtener_reservas_canceladas():
    """
    Obtiene todas las reservas canceladas.
    
    Returns:
        list: Lista de reservas canceladas
    """
    return [r for r in reservas if r["estado"] == "cancelada"]

def listar_reservas():
    """
    Lista todas las reservas.
    
    Returns:
        list: Lista de todas las reservas
    """
    return reservas

def obtener_reservas_por_tipo(tipo_servicio):
    """
    Obtiene todas las reservas de un tipo específico.
    
    Args:
        tipo_servicio (str): Tipo de servicio ("sala", "equipo", "servicio")
    
    Returns:
        list: Lista de reservas del tipo especificado
    """
    return [r for r in reservas if r["tipo"] == tipo_servicio]
