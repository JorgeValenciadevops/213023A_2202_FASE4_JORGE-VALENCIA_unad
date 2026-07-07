"""
customers.py - Gestión de clientes

Funciones para:
- Registrar clientes
- Buscar clientes
- Actualizar clientes
- Eliminar clientes
- Validar clientes
"""

from data import clientes, id_cliente_contador
import logger


def validar_datos_cliente(nombre, email, telefono):
    """Valida los datos de un cliente antes de registrarlo."""
    nombre_limpio = (nombre or "").strip()
    email_limpio = (email or "").strip()
    telefono_limpio = (telefono or "").strip()

    if not nombre_limpio:
        raise ValueError("El campo nombre no puede estar vacío. Ingrese su nombre completo usando solo letras.")

    if not all(car.isalpha() or car.isspace() for car in nombre_limpio):
        raise ValueError("El campo nombre solo puede contener letras y espacios. Por favor, no ingrese números ni caracteres especiales.")

    if not email_limpio:
        raise ValueError("El campo Email no puede estar vacío. Ingrese un correo válido.")

    if "@" not in email_limpio or "." not in email_limpio.split("@", 1)[1]:
        raise ValueError("El campo Email no es válido. Ejemplo: nombre@dominio.com")

    if not telefono_limpio:
        raise ValueError("El campo Teléfono no puede estar vacío. Ingrese solo números.")

    if not telefono_limpio.isdigit():
        raise ValueError("El campo Teléfono solo puede contener números. Evite letras, espacios o signos.")

    return nombre_limpio, email_limpio, telefono_limpio


def registrar_cliente(nombre, email, telefono):
    """
    Registra un nuevo cliente.
    
    Args:
        nombre (str): Nombre del cliente
        email (str): Email del cliente
        telefono (str): Teléfono del cliente
    
    Returns:
        int: ID del cliente registrado o -1 si hay error
    """
    try:
        nombre_limpio, email_limpio, telefono_limpio = validar_datos_cliente(nombre, email, telefono)

        if not validar_cliente_nuevo(nombre_limpio, email_limpio, telefono_limpio):
            logger.registrar_error(f"Validación fallida para cliente: {nombre_limpio}")
            return -1
        
        from data import id_cliente_contador as contador
        nuevo_id = contador
        
        clientes[nuevo_id] = {
            "nombre": nombre_limpio,
            "email": email_limpio,
            "telefono": telefono_limpio,
            "activo": True
        }
        
        logger.registrar_evento(f"Cliente registrado: {nombre_limpio} (ID: {nuevo_id})")
        return nuevo_id
    
    except ValueError as e:
        logger.registrar_advertencia(f"Validación de cliente fallida: {str(e)}")
        raise
    except Exception as e:
        logger.registrar_error(f"Error al registrar cliente: {str(e)}")
        return -1

def buscar_cliente(id_cliente):
    """
    Busca un cliente por ID.
    
    Args:
        id_cliente (int): ID del cliente
    
    Returns:
        dict: Datos del cliente o None si no existe
    """
    return clientes.get(id_cliente, None)

def buscar_cliente_por_email(email):
    """
    Busca un cliente por email.
    
    Args:
        email (str): Email del cliente
    
    Returns:
        dict: Datos del cliente o None si no existe
    """
    for id_cliente, datos in clientes.items():
        if datos["email"] == email:
            return {"id": id_cliente, **datos}
    return None

def actualizar_cliente(id_cliente, nombre=None, email=None, telefono=None):
    """
    Actualiza los datos de un cliente.
    
    Args:
        id_cliente (int): ID del cliente
        nombre (str, optional): Nuevo nombre
        email (str, optional): Nuevo email
        telefono (str, optional): Nuevo teléfono
    
    Returns:
        bool: True si la actualización fue exitosa
    """
    try:
        if id_cliente not in clientes:
            logger.registrar_error(f"Cliente con ID {id_cliente} no encontrado")
            return False
        
        if nombre:
            clientes[id_cliente]["nombre"] = nombre
        if email:
            clientes[id_cliente]["email"] = email
        if telefono:
            clientes[id_cliente]["telefono"] = telefono
        
        logger.registrar_evento(f"Cliente actualizado: ID {id_cliente}")
        return True
    
    except Exception as e:
        logger.registrar_error(f"Error al actualizar cliente: {str(e)}")
        return False

def eliminar_cliente(id_cliente):
    """
    Elimina un cliente (marca como inactivo).
    
    Args:
        id_cliente (int): ID del cliente
    
    Returns:
        bool: True si se eliminó exitosamente
    """
    try:
        if id_cliente not in clientes:
            logger.registrar_error(f"Cliente con ID {id_cliente} no encontrado")
            return False
        
        clientes[id_cliente]["activo"] = False
        logger.registrar_evento(f"Cliente eliminado: ID {id_cliente}")
        return True
    
    except Exception as e:
        logger.registrar_error(f"Error al eliminar cliente: {str(e)}")
        return False

def validar_cliente_nuevo(nombre, email, telefono):
    """
    Valida los datos de un nuevo cliente.
    
    Args:
        nombre (str): Nombre del cliente
        email (str): Email del cliente
        telefono (str): Teléfono del cliente
    
    Returns:
        bool: True si los datos son válidos
    """
    if not nombre or len(nombre.strip()) == 0:
        logger.registrar_advertencia("Nombre vacío")
        return False
    
    if not email or "@" not in email:
        logger.registrar_advertencia(f"Email inválido: {email}")
        return False
    
    if buscar_cliente_por_email(email):
        logger.registrar_advertencia(f"Email ya registrado: {email}")
        return False
    
    if not telefono or len(telefono.strip()) == 0:
        logger.registrar_advertencia("Teléfono vacío")
        return False
    
    return True

def validar_cliente_existente(id_cliente):
    """
    Valida si un cliente existe y está activo.
    
    Args:
        id_cliente (int): ID del cliente
    
    Returns:
        bool: True si el cliente existe y está activo
    """
    if id_cliente not in clientes:
        return False
    return clientes[id_cliente]["activo"]

def listar_clientes():
    """
    Lista todos los clientes activos.
    
    Returns:
        list: Lista de clientes
    """
    return [(id_c, datos) for id_c, datos in clientes.items() if datos["activo"]]
