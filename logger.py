"""
logger.py - Sistema de logging

Gestiona el registro de errores, advertencias y eventos del programa.
Mantiene un archivo log con timestamps para seguimiento de actividades.
"""

from datetime import datetime
import os

# Archivo de log
LOG_FILE = "reservation_manager.log"

def _crear_archivo_log():
    """Crea el archivo de log si no existe."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=== RESERVATION MANAGER - LOG DE EVENTOS ===\n")
            f.write(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

def registrar_error(mensaje):
    """
    Registra un error en el archivo de log.
    
    Args:
        mensaje (str): Descripción del error
    """
    _crear_archivo_log()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = f"[ERROR] [{timestamp}] {mensaje}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entrada)
    
    print(entrada)

def registrar_advertencia(mensaje):
    """
    Registra una advertencia en el archivo de log.
    
    Args:
        mensaje (str): Descripción de la advertencia
    """
    _crear_archivo_log()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = f"[ADVERTENCIA] [{timestamp}] {mensaje}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entrada)
    
    print(entrada)

def registrar_evento(mensaje):
    """
    Registra un evento en el archivo de log.
    
    Args:
        mensaje (str): Descripción del evento
    """
    _crear_archivo_log()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = f"[EVENTO] [{timestamp}] {mensaje}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entrada)
    
    print(entrada)

def limpiar_log():
    """Limpia el archivo de log."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    _crear_archivo_log()
