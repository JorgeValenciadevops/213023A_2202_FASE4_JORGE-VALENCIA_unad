"""
ui.py - Interfaz Gráfica Tkinter

Gestiona:
- Interfaz Tkinter
- Formularios
- Botones
- Tablas/listados
- Menús
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
  
try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

import customers
import services
import reservations
import logger


def formatear_fecha_hora_seleccionada(fecha, hora, minuto, meridiem):
    """Convierte una fecha y hora seleccionadas a formato de reserva."""
    if hasattr(fecha, "strftime"):
        fecha_obj = fecha
    else:
        fecha_obj = datetime.strptime(str(fecha), "%Y-%m-%d").date()

    hora_valor = int(hora)
    if meridiem == "PM" and hora_valor != 12:
        hora_valor += 12
    elif meridiem == "AM" and hora_valor == 12:
        hora_valor = 0

    return datetime(
        fecha_obj.year,
        fecha_obj.month,
        fecha_obj.day,
        hora_valor,
        int(minuto)
    ).strftime("%Y-%m-%d %H:%M")


class ReservationManagerUI:
    """Interfaz gráfica principal del Reservation Manager"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica.
        
        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.root.title("Reservation Manager")
        self.root.geometry("900x600")
        
        # Configurar menú
        self._crear_menu()
        
        # Frame principal
        self.frame_principal = ttk.Frame(root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pantalla inicial
        self._mostrar_inicio()
        
        logger.registrar_evento("Interfaz gráfica iniciada")
    
    def _crear_menu(self):
        """Crea el menú principal."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        # Menú Clientes
        menu_clientes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Clientes", menu=menu_clientes)
        menu_clientes.add_command(label="Registrar Cliente", command=self._mostrar_registro_cliente)
        menu_clientes.add_command(label="Listar Clientes", command=self._mostrar_clientes)
        
        # Menú Servicios
        menu_servicios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Servicios", menu=menu_servicios)
        menu_servicios.add_command(label="Ver Salas", command=self._mostrar_salas)
        menu_servicios.add_command(label="Ver Equipos", command=self._mostrar_equipos)
        menu_servicios.add_command(label="Ver Servicios", command=self._mostrar_servicios)
        
        # Menú Reservas
        menu_reservas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reservas", menu=menu_reservas)
        menu_reservas.add_command(label="Nueva Reserva", command=self._mostrar_nueva_reserva)
        menu_reservas.add_command(label="Ver Reservas", command=self._mostrar_reservas)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de...", command=self._mostrar_acerca_de)
    
    def _limpiar_frame(self):
        """Limpia el frame principal."""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
    
    def _mostrar_inicio(self):
        """Muestra la pantalla de inicio."""
        self._limpiar_frame()
        
        label_titulo = ttk.Label(self.frame_principal, text="RESERVATION MANAGER", 
                                 font=("Arial", 24, "bold"))
        label_titulo.pack(pady=20)
        
        label_descripcion = ttk.Label(self.frame_principal, 
                                      text="Sistema de gestión de reservas de salas, equipos y servicios",
                                      font=("Arial", 12))
        label_descripcion.pack(pady=10)
        
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.pack(pady=20)
        
        ttk.Button(frame_botones, text="Registrar Cliente", 
                   command=self._mostrar_registro_cliente).pack(pady=5)
        ttk.Button(frame_botones, text="Nueva Reserva", 
                   command=self._mostrar_nueva_reserva).pack(pady=5)
        ttk.Button(frame_botones, text="Ver Reservas", 
                   command=self._mostrar_reservas).pack(pady=5)
    
    def _mostrar_registro_cliente(self):
        """Muestra formulario para registrar cliente."""
        self._limpiar_frame()
        
        ttk.Label(self.frame_principal, text="REGISTRAR CLIENTE", 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        frame_form = ttk.Frame(self.frame_principal)
        frame_form.pack(padx=20, pady=10)
        
        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        entry_nombre = ttk.Entry(frame_form, width=30)
        entry_nombre.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        entry_email = ttk.Entry(frame_form, width=30)
        entry_email.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        entry_telefono = ttk.Entry(frame_form, width=30)
        entry_telefono.grid(row=2, column=1, pady=5)
        
        def guardar():
            try:
                nombre = entry_nombre.get()
                email = entry_email.get()
                telefono = entry_telefono.get()

                if customers.registrar_cliente(nombre, email, telefono) != -1:
                    messagebox.showinfo("Éxito", "Cliente registrado correctamente")
                    self._mostrar_clientes()
                else:
                    messagebox.showerror("Error", "No se pudo registrar el cliente")
            except ValueError as error:
                messagebox.showwarning("Validación", str(error))
            except Exception as error:
                logger.registrar_error(f"Error inesperado al registrar cliente: {error}")
                messagebox.showerror("Error", "Ocurrió un error inesperado. Intente nuevamente.")
        
        ttk.Button(frame_form, text="Guardar", command=guardar).grid(row=3, column=0, pady=15)
        ttk.Button(frame_form, text="Volver", command=self._mostrar_inicio).grid(row=3, column=1)
    
    def _mostrar_clientes(self):
        """Muestra lista de clientes."""
        self._limpiar_frame()
        
        ttk.Label(self.frame_principal, text="CLIENTES REGISTRADOS", 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        frame_tabla = ttk.Frame(self.frame_principal)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear tabla
        cols = ("ID", "Nombre", "Email", "Teléfono")
        tree = ttk.Treeview(frame_tabla, columns=cols, height=15)
        tree.column("#0", width=0, stretch=tk.NO)
        
        for col in cols:
            tree.column(col, anchor=tk.W, width=200)
            tree.heading(col, text=col, anchor=tk.W)
        
        # Llenar datos
        for id_cliente, datos in customers.listar_clientes():
            tree.insert(parent='', index='end', iid=id_cliente,
                       values=(id_cliente, datos["nombre"], datos["email"], datos["telefono"]))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(self.frame_principal, text="Volver", 
                   command=self._mostrar_inicio).pack(pady=10)
    
    def _mostrar_salas(self):
        """Muestra catálogo de salas."""
        self._mostrar_servicio("SALAS DISPONIBLES", services.obtener_salas())
    
    def _mostrar_equipos(self):
        """Muestra catálogo de equipos."""
        self._mostrar_servicio("EQUIPOS DISPONIBLES", services.obtener_equipos())
    
    def _mostrar_servicios(self):
        """Muestra catálogo de servicios."""
        self._mostrar_servicio("SERVICIOS DISPONIBLES", services.obtener_servicios())
    
    def _mostrar_servicio(self, titulo, items):
        """Muestra un catálogo de servicios."""
        self._limpiar_frame()
        
        ttk.Label(self.frame_principal, text=titulo, 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        frame_lista = ttk.Frame(self.frame_principal)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for id_item, datos in items.items():
            precio = datos.get("precio_hora") or datos.get("precio_dia") or datos.get("precio")
            if precio is not None:
                etiqueta = f"ID: {id_item} - {datos['nombre']} - Precio: ${precio:,.0f}"
            else:
                etiqueta = f"ID: {id_item} - {datos['nombre']}"
            ttk.Label(frame_lista, text=etiqueta, font=("Arial", 11)).pack(anchor="w", pady=5)
        
        ttk.Button(self.frame_principal, text="Volver", 
                   command=self._mostrar_inicio).pack(pady=10)
    
    def _mostrar_nueva_reserva(self):
        """Muestra formulario para nueva reserva."""
        self._limpiar_frame()
        
        ttk.Label(self.frame_principal, text="NUEVA RESERVA", 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        frame_form = ttk.Frame(self.frame_principal)
        frame_form.pack(padx=20, pady=10)
        
        ttk.Label(frame_form, text="ID Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        entry_cliente = ttk.Entry(frame_form, width=30)
        entry_cliente.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Tipo Servicio:").grid(row=1, column=0, sticky="w", pady=5)
        combo_tipo = ttk.Combobox(frame_form, values=["sala", "equipo", "servicio"], width=27, state="readonly")
        combo_tipo.current(0)
        combo_tipo.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame_form, text="ID Servicio:").grid(row=2, column=0, sticky="w", pady=5)
        entry_servicio = ttk.Entry(frame_form, width=30)
        entry_servicio.grid(row=2, column=1, pady=5)
        
        def crear_selector_fecha_hora(row, texto):
            ttk.Label(frame_form, text=texto).grid(row=row, column=0, sticky="w", pady=5)
            selector_frame = ttk.Frame(frame_form)
            selector_frame.grid(row=row, column=1, sticky="w", pady=5)

            if DateEntry is not None:
                fecha_widget = DateEntry(selector_frame, width=18, date_pattern="yyyy-mm-dd")
                fecha_widget.set_date(date.today())
                fecha_widget.pack(side=tk.LEFT)
            else:
                fecha_widget = ttk.Entry(selector_frame, width=18)
                fecha_widget.insert(0, date.today().strftime("%Y-%m-%d"))
                fecha_widget.pack(side=tk.LEFT)

            horas = [f"{i:02d}" for i in range(1, 13)]
            minutos = [f"{i:02d}" for i in range(60)]
            combo_hora = ttk.Combobox(selector_frame, values=horas, width=5, state="readonly")
            combo_hora.current(0)
            combo_hora.pack(side=tk.LEFT, padx=(5, 0))

            ttk.Label(selector_frame, text=":").pack(side=tk.LEFT)

            combo_minuto = ttk.Combobox(selector_frame, values=minutos, width=5, state="readonly")
            combo_minuto.current(0)
            combo_minuto.pack(side=tk.LEFT)

            combo_meridiem = ttk.Combobox(selector_frame, values=["AM", "PM"], width=5, state="readonly")
            combo_meridiem.current(0)
            combo_meridiem.pack(side=tk.LEFT, padx=(5, 0))

            return fecha_widget, combo_hora, combo_minuto, combo_meridiem

        fecha_inicio_widget, combo_inicio_hora, combo_inicio_minuto, combo_inicio_meridiem = crear_selector_fecha_hora(3, "Fecha y hora inicio:")
        fecha_fin_widget, combo_fin_hora, combo_fin_minuto, combo_fin_meridiem = crear_selector_fecha_hora(4, "Fecha y hora fin:")
        
        ttk.Label(frame_form, text="Cantidad/Duración:").grid(row=5, column=0, sticky="w", pady=5)
        entry_cantidad = ttk.Entry(frame_form, width=30)
        entry_cantidad.insert(0, "1")
        entry_cantidad.grid(row=5, column=1, pady=5)
        
        def guardar():
            try:
                fecha_inicio = formatear_fecha_hora_seleccionada(
                    fecha_inicio_widget.get_date() if hasattr(fecha_inicio_widget, "get_date") else fecha_inicio_widget.get(),
                    combo_inicio_hora.get(),
                    combo_inicio_minuto.get(),
                    combo_inicio_meridiem.get()
                )
                fecha_fin = formatear_fecha_hora_seleccionada(
                    fecha_fin_widget.get_date() if hasattr(fecha_fin_widget, "get_date") else fecha_fin_widget.get(),
                    combo_fin_hora.get(),
                    combo_fin_minuto.get(),
                    combo_fin_meridiem.get()
                )

                id_reserva = reservations.crear_reserva(
                    int(entry_cliente.get()),
                    combo_tipo.get(),
                    int(entry_servicio.get()),
                    fecha_inicio,
                    fecha_fin,
                    int(entry_cantidad.get())
                )
                
                if id_reserva != -1:
                    messagebox.showinfo("Éxito", f"Reserva creada con ID: {id_reserva}")
                    self._mostrar_reservas()
                else:
                    messagebox.showerror("Error", "No se pudo crear la reserva")
            except ValueError as error:
                logger.registrar_advertencia(f"Reserva inválida: {error}")
                messagebox.showwarning("Validación", str(error))
            except Exception as error:
                logger.registrar_error(f"Error inesperado al crear reserva: {error}")
                messagebox.showerror("Error", "Ocurrió un error inesperado al crear la reserva.")
        
        ttk.Button(frame_form, text="Guardar", command=guardar).grid(row=6, column=0, pady=15)
        ttk.Button(frame_form, text="Volver", command=self._mostrar_inicio).grid(row=6, column=1)
    
    def _mostrar_reservas(self):
        """Muestra lista de reservas."""
        self._limpiar_frame()
        
        ttk.Label(self.frame_principal, text="RESERVAS", 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        frame_tabla = ttk.Frame(self.frame_principal)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        cols = ("ID", "Cliente", "Tipo", "Servicio", "Inicio", "Fin", "Estado", "Precio")
        tree = ttk.Treeview(frame_tabla, columns=cols, height=12)
        tree.column("#0", width=0, stretch=tk.NO)
        
        for col in cols:
            tree.column(col, anchor=tk.W, width=100)
            tree.heading(col, text=col, anchor=tk.W)
        
        for reserva in reservations.listar_reservas():
            tree.insert(parent='', index='end', iid=reserva["id_reserva"],
                       values=(reserva["id_reserva"], reserva["id_cliente"], 
                              reserva["tipo"], reserva["id_servicio"],
                              reserva["fecha_inicio"], reserva["fecha_fin"],
                              reserva["estado"], f"${reserva['precio_total']:.2f}"))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(self.frame_principal, text="Volver", 
                   command=self._mostrar_inicio).pack(pady=10)
    
    def _mostrar_acerca_de(self):
        """Muestra diálogo de acerca de."""
        messagebox.showinfo("Acerca de", 
                           "RESERVATION MANAGER v1.0\n\n"
                           "Sistema de gestión de reservas\n"
                           "Salas, equipos y servicios\n\n"
                           "Arquitectura de componentes modulares")

def iniciar_aplicacion():
    """Inicia la aplicación."""
    root = tk.Tk()
    app = ReservationManagerUI(root)
    root.mainloop()
