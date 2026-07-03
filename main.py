"""
RESERVATION_MANAGER - Arquitectura (Versión Básica)

Objetivo: Aplicación de ejemplo para gestionar reservas de salas,
alquiler de equipos y servicios especializados. No utiliza bases de
datos; toda la información se almacena temporalmente en listas,
diccionarios y matrices.

reservation_manager/
 │ 
 ├── main.py 
	│ - Punto de entrada de la aplicación. 
	│ - Inicia la interfaz gráfica.
 │ ├── ui.py 
	│ - Interfaz Tkinter. 
	│ - Formularios. 
	│ - Botones. 
	│ - Tablas. 
	│ - Menús.
 │
 ├──customers.py 
	│ - Registrar cliente. 
	│ - Buscar cliente. 
	│ - Actualizar cliente. 
	│ - Eliminar cliente. 
	│ - Validar cliente.
│ 
├── services.py
	│ - Catálogo de salas. 
	│ - Catálogo de equipos. 
	│ - Catálogo de	servicios. 
	│ - Consultar disponibilidad.
│ 
├── reservations.py 
	│ - Crear - reserva. 
	│ - Cancelar reserva. 
	│ - Consultar reservas. 
│ 
├── logger.py
	│ - Registrar errores. 
	│ - Registrar advertencias. 
	│ - Guardar eventos en un archivo log. 
│ 
└── data.py - Contiene las estructuras de datos del programa.
Flujo del programa

main.py ↓ ui.py ↓ customers.py (valida cliente) ↓ services.py (consulta
disponibilidad) ↓ reservations.py (crea o cancela la reserva) ↓
logger.py (registra errores si ocurren)

Notas

-   No utiliza bases de datos.
-   No utiliza SQL.
-   Toda la información se maneja con listas, diccionarios y matrices.
-   Arquitectura sencilla para un proyecto académico o de muestra.

"""

# Importar la función para iniciar la interfaz gráfica
from ui import iniciar_aplicacion

# Punto de entrada de la aplicación
if __name__ == "__main__":
    print("Iniciando Reservation Manager...")
    iniciar_aplicacion()
