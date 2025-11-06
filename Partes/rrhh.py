from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date
import subprocess 
from tkcalendar import Calendar 
import time

# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "", # Asegúrate de que esta sea tu contraseña, si tienes una.
    "database": "fiter"
}
                                                                            
# --- Variables Globales para Control de Ventanas Toplevel Únicas ---
lista_empleados_window = None 
lista_candidatos_window = None

# --- CONSTANTE para el Placeholder del OptionMenu ---
DEPARTAMENTO_PLACEHOLDER = "Seleccionar Departamento"

# --- ALMACENAMIENTO GLOBAL DE DEPARTAMENTOS ---
# Almacena {Nombre: ID} para convertir la selección del usuario (Nombre) a la FK (ID).
DEPARTAMENTOS_MAP = {} 

def conectar_bd():
    """Establece y devuelve una conexión a una conexión de la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {err}")
        return None

# ----------------- Funciones Auxiliares para Datos -----------------

def obtener_nombres_departamentos():
    """
    Consulta la tabla DEPARTAMENTOS y devuelve un diccionario de {Nombre: ID} y la lista de Nombres.
    Actualiza la variable global DEPARTAMENTOS_MAP.
    """
    global DEPARTAMENTOS_MAP
    conn = conectar_bd()
    DEPARTAMENTOS_MAP = {}
    departamentos_nombres = []
    
    if conn:
        cursor = conn.cursor()
        try:
            # Selecciona el ID y el Nombre para el mapeo
            cursor.execute("SELECT ID_Departamento, Nombre FROM DEPARTAMENTOS ORDER BY Nombre") 
            
            for id_dept, nombre_dept in cursor.fetchall():
                DEPARTAMENTOS_MAP[nombre_dept] = id_dept
                departamentos_nombres.append(nombre_dept)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar departamentos: {err}")
        finally:
            cursor.close()
            conn.close()
    
    return departamentos_nombres

# ----------------------------------------------------
# --- FUNCIÓN AUXILIAR DE CALENDARIO (CORRECCIÓN READONLY) ---
# ----------------------------------------------------
def open_calendar(target_entry, parent_window):
    """
    Abre la ventana del calendario al hacer clic en el Entry.
    """
    def select_date():
        fecha_seleccionada = cal.selection_get().isoformat()
        
        target_entry.config(state='normal') 
        target_entry.delete(0, END)
        target_entry.insert(0, fecha_seleccionada)
        target_entry.config(state='readonly')
        
        top_cal.destroy()

    top_cal = Toplevel(parent_window)
    top_cal.title("Seleccionar Fecha")
    top_cal.resizable(False, False) 
    top_cal.grab_set() 

    x = parent_window.winfo_x() + (parent_window.winfo_width() // 2) - 150 
    y = parent_window.winfo_y() + (parent_window.winfo_height() // 2) - 150 
    top_cal.geometry(f'+{x}+{y}')

    cal = Calendar(top_cal, selectmode='day',
                   date_pattern='yyyy-mm-dd',
                   font="Arial 10", locale='es_ES',
                   background="#0089a1", foreground="white",
                   headersbackground="#006779", headersforeground="white",
                   normalbackground="#1dc1dd", weekendbackground="#1dc1dd", 
                   bordercolor="#006779")
    cal.pack(pady=10, padx=10)

    Button(top_cal, text="Aceptar", command=select_date, 
           bg="#0089a1", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

# ----------------- GESTIÓN DE EMPLEADOS -----------------

def guardar_nuevo_empleado(top, entry_widgets):
    """
    Recoge los datos del formulario, convierte el Nombre del Departamento a ID 
    y ejecuta la inserción.
    """
    try:
        PLACEHOLDERS = {
            'nombre': "Nombre:*",
            'apellido': "Apellido:*",
            'puesto': "Puesto:*",
            'departamento': DEPARTAMENTO_PLACEHOLDER,
            'fecha_contratacion': date.today().isoformat(),
            'fecha_nacimiento': "Click para seleccionar fecha",
            'direccion': "Dirección:",
            'telefono': "Teléfono:",
            'email': "Email:"
        }
        
        datos_entrada = {}
        for key, widget in entry_widgets.items():
            datos_entrada[key] = widget.get().strip() 

        # --- Obtención del ID de Departamento (FK) ---
        departamento_nombre = datos_entrada['departamento']
        id_departamento_fk = None
        
        # Si el valor seleccionado es válido, obtenemos su ID del mapeo global
        if departamento_nombre != DEPARTAMENTO_PLACEHOLDER and departamento_nombre in DEPARTAMENTOS_MAP:
            id_departamento_fk = DEPARTAMENTOS_MAP[departamento_nombre]
        
        # Limpiar placeholders para otros campos
        for key, value in datos_entrada.items():
            if key != 'departamento':
                placeholder_text = PLACEHOLDERS.get(key, "").replace('*', '').strip()
                if value == placeholder_text or value == "Click para seleccionar fecha":
                    datos_entrada[key] = ""
        
        nombre = datos_entrada['nombre']
        apellido = datos_entrada['apellido']
        puesto = datos_entrada['puesto']
        fecha_contratacion_str = datos_entrada['fecha_contratacion']
        
        # 2. Validación de campos obligatorios
        if not all([nombre, apellido, puesto, fecha_contratacion_str]):
            messagebox.showwarning("Advertencia", "Los campos Nombre, Apellido, Puesto y Fecha de Contratación son obligatorios.")
            return

        # 3. Validación y conversión de fechas
        fecha_nacimiento = None
        try:
            if datos_entrada['fecha_nacimiento']:
                fecha_nacimiento = date.fromisoformat(datos_entrada['fecha_nacimiento'])
            fecha_contratacion = date.fromisoformat(fecha_contratacion_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "Asegúrate de que las fechas estén en formato YYYY-MM-DD.")
            return
            
        # 4. Conexión y Ejecución de la Inserción
        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                # SQL ADAPTADO: Usa ID_Departamento como Clave Foránea
                sql = """
                    INSERT INTO Empleados_RRHH (Nombre, Apellido, ID_Departamento, Fecha_Nacimiento, 
                                                Direccion, Telefono, Email, Fecha_Contratacion, Puesto) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                datos = (
                    nombre, 
                    apellido, 
                    id_departamento_fk, # <-- Clave Foránea (ID)
                    fecha_nacimiento, 
                    datos_entrada['direccion'] if datos_entrada['direccion'] else None, 
                    datos_entrada['telefono'] if datos_entrada['telefono'] else None, 
                    datos_entrada['email'] if datos_entrada['email'] else None, 
                    fecha_contratacion, 
                    puesto
                )
                
                cursor.execute(sql, datos)
                conn.commit()
                
                nuevo_id = cursor.lastrowid
                messagebox.showinfo("Éxito", f"Empleado {nombre} {apellido} registrado con éxito.\nID Generado: {nuevo_id}")
                top.destroy() 
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al insertar el empleado. Asegúrate que la Clave Foránea (ID) existe: {err}")
            except Exception as e:
                messagebox.showerror("Error Inesperado", f"Ocurrió un error al guardar: {e}")
            finally:
                cursor.close()
                conn.close()

    except Exception as e:
        messagebox.showerror("Error Interno", f"Ocurrió un error inesperado en la validación: {e}")

# -----------------------------------------------
# --- FUNCIÓN PRINCIPAL DEL FORMULARIO DE ALTA ---
# -----------------------------------------------
def formulario_alta_empleado(parent_window):
    """
    Crea y muestra la ventana Toplevel con el formulario completo.
    """
    top = Toplevel(parent_window)
    top.title("Formulario de Alta de Empleado")
    top.geometry('700x750+400+100') 
    top.configure(bg="#1dc1dd")
    top.grab_set()

    # Funciones de ayuda para el placeholder (solo para campos de texto NO fecha)
    def on_enter(e, entry, placeholder):
        if entry.get().strip() == placeholder.strip():
            entry.delete(0, 'end')

    def on_leave(e, entry, placeholder):
        if entry.get().strip() == '':
            entry.insert(0, placeholder.strip())
            
    # --- CONFIGURACIÓN DE WIDGETS ---
    labels_config = [
        ("Nombre:*", "nombre", False, 'Entry'),
        ("Apellido:*", "apellido", False, 'Entry'),
        ("Puesto:*", "puesto", False, 'Entry'),
        ("Departamento:", "departamento", False, 'Menu'), # OptionMenu
        ("Fecha Contratación:", "fecha_contratacion", True, 'Entry'), # Calendario
        ("Fecha Nacimiento:", "fecha_nacimiento", True, 'Entry'),      # Calendario
        ("Dirección:", "direccion", False, 'Entry'),
        ("Teléfono:", "telefono", False, 'Entry'),
        ("Email:", "email", False, 'Entry'),
    ]

    entry_widgets = {}
    FONT_STYLE_LABEL = ('Arial', 11, 'bold')
    FONT_STYLE_ENTRY = ('Arial', 11)
    FRAME_BG = "#1dc1dd"
    ROW_START = 3

    # Frame central
    frame = Frame(top, bg=FRAME_BG)
    frame.pack(expand=True, fill='both', padx=50, pady=20) 
    
    frame.grid_columnconfigure(0, weight=1, uniform="group")
    frame.grid_columnconfigure(1, weight=2, uniform="group") 
    
    for i in range(ROW_START, ROW_START + len(labels_config)):
        frame.grid_rowconfigure(i, weight=1) 

    # Encabezado
    heading = Label(frame, text='Alta de Nuevo Empleado', fg='white', bg=FRAME_BG, font=('Arial', 20, 'bold'))
    heading.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')
    
    Frame(frame, height=2, bg='white').grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)


    # Bucle para crear etiquetas y campos de entrada/calendario/menú
    for i, (label_text, key, use_calendar, widget_type) in enumerate(labels_config):
        row_num = ROW_START + i
        
        # Etiqueta (en Negrita)
        display_label = label_text.replace(':', '').replace('*', '').strip()
        Label(frame, text=display_label + (":*" if key in ['nombre', 'apellido', 'puesto', 'fecha_contratacion'] else ":"), 
              fg='white', bg=FRAME_BG, font=FONT_STYLE_LABEL, anchor='w').grid(
            row=row_num, column=0, padx=(30, 10), pady=10, sticky='ew'
        )
        
        if widget_type == 'Menu':
            # --- IMPLEMENTACIÓN DEL MENÚ DESPLEGABLE (OptionMenu) ---
            # OBTENEMOS SOLO LOS NOMBRES VALIDOS
            departamentos_nombres = obtener_nombres_departamentos()
            
            dept_var = StringVar(frame)
            dept_var.set(DEPARTAMENTO_PLACEHOLDER) 

            if departamentos_nombres:
                # Las opciones del menú son solo los nombres válidos de la BD
                dept_menu = OptionMenu(frame, dept_var, *departamentos_nombres)
            else:
                 # Si no hay departamentos válidos
                dept_menu = OptionMenu(frame, dept_var, "ERROR: No hay departamentos en BD")
                dept_menu.config(state=DISABLED) 

            dept_menu.config(fg='black', bg='white', font=FONT_STYLE_ENTRY, border=0, highlightthickness=0, width=20)
            
            dept_menu.grid(row=row_num, column=1, padx=(10, 30), pady=10, sticky='ew')
            
            entry_widgets[key] = dept_var
            
            Frame(frame, height=2, bg='black').grid(row=row_num, column=1, padx=(10, 30), sticky='swe', ipady=0)


        elif use_calendar:
            # --- IMPLEMENTACIÓN DE ENTRADAS CON CALENDARIO (Entry) ---
            entry = Entry(frame, fg='black', border=0, bg='white', font=FONT_STYLE_ENTRY)
            entry.grid(row=row_num, column=1, padx=(10, 30), pady=10, sticky='ew')
            entry_widgets[key] = entry 

            entry.bind('<Button-1>', lambda e, en=entry: open_calendar(en, top))
            entry.config(state='readonly') 
            
            if key == "fecha_contratacion":
                entry.config(state='normal')
                entry.insert(0, date.today().isoformat())
                entry.config(state='readonly')
            else:
                placeholder_text = "Click para seleccionar fecha"
                entry.config(state='normal')
                entry.insert(0, placeholder_text)
                entry.config(state='readonly')

            Frame(frame, height=2, bg='black').grid(row=row_num, column=1, padx=(10, 30), sticky='swe', ipady=0)

        else:
            # --- IMPLEMENTACIÓN DE ENTRADAS REGULARES (Entry) ---
            entry = Entry(frame, fg='black', border=0, bg='white', font=FONT_STYLE_ENTRY)
            entry.grid(row=row_num, column=1, padx=(10, 30), pady=10, sticky='ew')
            entry_widgets[key] = entry 
            
            placeholder_text = label_text.replace('*', '').strip()
            entry.insert(0, placeholder_text)
            
            entry.bind('<FocusIn>', lambda e, en=entry, txt=placeholder_text: on_enter(e, en, txt))
            entry.bind('<FocusOut>', lambda e, en=entry, txt=placeholder_text: on_leave(e, en, txt))
            
            Frame(frame, height=2, bg='black').grid(row=row_num, column=1, padx=(10, 30), sticky='swe', ipady=0)


    # --- Botones y Notas ---
    last_row = ROW_START + len(labels_config)
    frame.grid_rowconfigure(last_row, weight=1) 

    Label(frame, text="(*) Campos obligatorios", fg='yellow', bg=FRAME_BG, font=('Arial', 9, 'italic'), anchor='w').grid(
        row=last_row, column=0, columnspan=2, padx=30, pady=(10, 0), sticky='w'
    )
    
    button_frame = Frame(frame, bg=FRAME_BG)
    button_frame.grid(row=last_row + 1, column=0, columnspan=2, pady=(10, 20), sticky='n')
    
    enter = Button(button_frame, width=15, text='Guardar Empleado', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", 
                   font=('Arial', 12, 'bold'), command=lambda: guardar_nuevo_empleado(top, entry_widgets))
    enter.pack(side=LEFT, padx=30)

    cancel_btn = Button(button_frame, width=15, text='Cancelar', border=0, bg="#ff4d4d", cursor='hand2', fg="#ffffff", 
                        font=('Arial', 12, 'bold'), command=top.destroy)
    cancel_btn.pack(side=LEFT, padx=30)

def alta_empleado(parent_window):
    """Función de enlace: abre el formulario de alta."""
    formulario_alta_empleado(parent_window)

def baja_empleado(parent_window):
    """Flujo: ¿Desea dar de baja un empleado? -> Seleccionar empleado -> Actualizar BD"""
    id_a_borrar = simpledialog.askinteger("Baja Empleado", "Ingresa el ID del empleado a dar de baja:", parent=parent_window)
    if id_a_borrar is None: return

    confirm = messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de dar de BAJA al empleado con ID {id_a_borrar}?", icon='warning')
    if not confirm: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM Empleados_RRHH WHERE ID_Empleado = %s"
            cursor.execute(sql, (id_a_borrar,))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Empleado con ID {id_a_borrar} dado de baja (eliminado).")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró empleado con ID {id_a_borrar}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al dar de baja: {err}")
        finally:
            cursor.close()
            conn.close()

def modificar_empleado(parent_window):
    """Flujo: ¿Desea modificar datos? -> Seleccionar -> Modificar Puesto"""
    id_modificar = simpledialog.askinteger("Modificar Empleado", "Ingresa el ID del empleado a modificar:", parent=parent_window)
    if id_modificar is None: return

    nuevo_puesto = simpledialog.askstring("Modificar Empleado", f"Nuevo Puesto para ID {id_modificar}:", parent=parent_window)
    if not nuevo_puesto: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "UPDATE Empleados_RRHH SET Puesto = %s WHERE ID_Empleado = %s"
            cursor.execute(sql, (nuevo_puesto, id_modificar))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Puesto del empleado ID {id_modificar} actualizado a '{nuevo_puesto}'.")
            else:
                messagebox.showwarning("Advertencia", f"No se encontró empleado con ID {id_modificar}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al modificar: {err}")
        finally:
            cursor.close()
            conn.close()

def ver_lista_empleados():
    """
    Consulta BD y Muestra la lista de empleados en una ventana Toplevel ÚNICA.
    Usa JOIN para obtener el Nombre del departamento (D.Nombre) a partir de la FK (E.ID_Departamento).
    """
    global lista_empleados_window
    
    if lista_empleados_window and lista_empleados_window.winfo_exists():
        lista_empleados_window.lift()
        return

    top = Toplevel()
    lista_empleados_window = top
    top.title("Lista de Empleados")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")
    
    def on_close():
        global lista_empleados_window
        lista_empleados_window = None
        top.destroy()
        
    top.protocol("WM_DELETE_WINDOW", on_close)

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # SQL ADAPTADO: LEFT JOIN para obtener el nombre del departamento
            sql_query = """
                SELECT E.ID_Empleado, E.Nombre, E.Apellido, E.Puesto, D.Nombre, E.Fecha_Contratacion
                FROM Empleados_RRHH E
                LEFT JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento;
            """
            cursor.execute(sql_query)
            empleados = cursor.fetchall()
            
            header = "ID | Nombre | Apellido | Puesto | Departamento | Contratación"
            Label(top, text=header, bg="#ffffff", fg="#000000", font=("Arial", 12, "bold")).pack(fill=X, padx=10, pady=5)

            if empleados:
                for emp in empleados:
                    id_emp, nombre, apellido, puesto, nombre_depto, fecha_contratacion = emp
                    
                    nombre_depto_display = nombre_depto if nombre_depto else "Sin Asignar"
                    fecha_contratacion_str = fecha_contratacion.strftime("%Y-%m-%d") if isinstance(fecha_contratacion, date) else str(fecha_contratacion)
                    
                    emp_str = f"{id_emp} | {nombre} | {apellido} | {puesto} | {nombre_depto_display} | {fecha_contratacion_str}"
                    Label(top, text=emp_str, bg="#f0f0ff", fg="black",
                          font=("Arial", 10), anchor="w").pack(fill=X, padx=10, pady=1)
            else:
                Label(top, text="No hay empleados registrados.", bg="#ffffff", fg="black", font=("Arial", 12)).pack(padx=10, pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar empleados: {err}")
        finally:
            cursor.close()
            conn.close()

# ----------------- RECLUTAMIENTO -----------------

def ver_posibles_candidatos():
    """Flujo: Muestra la lista de procesos de reclutamiento en una ventana Toplevel ÚNICA."""
    global lista_candidatos_window
    
    if lista_candidatos_window and lista_candidatos_window.winfo_exists():
        lista_candidatos_window.lift()
        return
        
    top = Toplevel()
    lista_candidatos_window = top
    top.title("Procesos de Reclutamiento (Candidatos)")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")

    def on_close():
        global lista_candidatos_window
        lista_candidatos_window = None
        top.destroy()
        
    top.protocol("WM_DELETE_WINDOW", on_close)

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql_reclutamiento = "SELECT ID_Reclutamiento, Descripcion_Puesto, Salario_Ofrecido, Estado_Proceso FROM Reclutamiento WHERE Estado_Proceso != 'Cerrado'"
            cursor.execute(sql_reclutamiento)
            procesos = cursor.fetchall()

            header = "ID | Puesto | Salario Ofrecido | Estado"
            Label(top, text=header, bg="#ffffff", fg="#000000", font=("Arial", 12, "bold")).pack(fill=X, padx=10, pady=5)

            if procesos:
                for proc in procesos:
                    salario_formateado = f"${proc[2]:,.2f}" if proc[2] is not None else "N/A"
                    proc_str = f"{proc[0]} | {proc[1][:30]}... | {salario_formateado} | {proc[3]}"
                    Label(top, text=proc_str, bg="#f0f0ff", fg="black",
                          font=("Arial", 10), anchor="w").pack(fill=X, padx=10, pady=1)
            else:
                Label(top, text="No hay procesos de reclutamiento abiertos.", bg="#ffffff", fg="black", font=("Arial", 12)).pack(padx=10, pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar reclutamiento: {err}")
        finally:
            cursor.close()
            conn.close()

# ----------------- CONEXIÓN FINANZAS (SIMULACIÓN) -----------------

def actualizar_maestros():
    """Simulación del botón de Finanzas que actualiza los maestros de RR.HH."""
    messagebox.showinfo("Actualizar Maestros",
                          "RR.HH. es el origen de los datos. La lista de Empleados está actualizada.\n"
                          "Si el módulo de Finanzas necesita la lista, debe consultarla aquí.")


# --- Función Principal de la Ventana de RR.HH. ---

def abrir_rrhh(parent_window, nombre_usuario):
    
    root = Toplevel()
    root.title(f"Recursos Humanos - Usuario: {nombre_usuario}")
    root.state("zoomed")
    root.configure(bg="#1dc1dd") # Fondo Turquesa
    
    parent_window.withdraw()

    def cerrar_sesion():
        global lista_empleados_window, lista_candidatos_window
        if lista_empleados_window and lista_empleados_window.winfo_exists():
            lista_empleados_window.destroy()
        if lista_candidatos_window and lista_candidatos_window.winfo_exists():
            lista_candidatos_window.destroy()
            
        root.destroy()
        parent_window.quit() 
        
        try:
            # Lanza el Home (home_deslog.py) como un nuevo proceso.
            subprocess.Popen(["python", "home_deslog.py"]) 
        except FileNotFoundError:
            messagebox.showerror("Error de Inicio", "Asegúrate de que 'home_deslog.py' exista y Python esté en el PATH.")
        
    root.protocol("WM_DELETE_WINDOW", cerrar_sesion)


    # --- Contenedores ---
    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)
    
    Button(frame_top, text="❌ Cerrar Sesión", bg="#ff4d4d", fg="white",
           font=("Arial", 12, "bold"), command=cerrar_sesion).pack(pady=5, padx=20, fill=X)
    
    Label(frame_top, text="Módulo de Recursos Humanos (RR.HH.)", bg="#1dc1dd", fg="white",
               font=("Arial", 18, "bold")).pack(pady=10)

    frame_acciones = Frame(root, bg="#1dc1dd")
    frame_acciones.pack(pady=20, fill=X)
    
    # --- Fila 1: Gestión de Empleados ---
    frame_empleados = Frame(frame_acciones, bg="#1dc1dd")
    frame_empleados.pack(pady=5)
    Label(frame_empleados, text="Gestión de Empleados", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_emp = Frame(frame_empleados, bg="#1dc1dd")
    frame_botones_emp.pack()

    Button(frame_botones_emp, text="Dar de Alta (Formulario)", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: alta_empleado(root)).pack(side=LEFT, padx=5)

    Button(frame_botones_emp, text="Dar de Baja", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: baja_empleado(root)).pack(side=LEFT, padx=5)

    Button(frame_botones_emp, text="Modificar Datos", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: modificar_empleado(root)).pack(side=LEFT, padx=5)

    Button(frame_botones_emp, text="Ver Empleados", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=ver_lista_empleados).pack(side=LEFT, padx=5)
    
    # --- Fila 2: Reclutamiento y Conexión ---
    frame_reclutamiento = Frame(frame_acciones, bg="#1dc1dd")
    frame_reclutamiento.pack(pady=5)
    Label(frame_reclutamiento, text="Reclutamiento y Conexión de Datos", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_rec = Frame(frame_reclutamiento, bg="#1dc1dd")
    frame_botones_rec.pack()

    Button(frame_botones_rec, text="Ver Candidatos", bg="#006779", fg="white", font=("Arial", 12, "bold"),
           width=25, command=ver_posibles_candidatos).pack(side=LEFT, padx=10)
    
    Button(frame_botones_rec, text="Actualizar Maestros (Finanzas)", bg="#006779", fg="white", font=("Arial", 12, "bold"),
           width=25, command=actualizar_maestros).pack(side=LEFT, padx=10)


    root.mainloop()

# ----------------- INICIO DEL PROGRAMA -----------------
if __name__ == '__main__':
    # Creamos la ventana principal (Root) de Tkinter. Es esencial para el mainloop.
    main_root = Tk()
    main_root.withdraw() # La ocultamos
    main_root.title("Ventana Raíz Oculta")
    
    # Iniciamos el módulo de RR.HH.
    abrir_rrhh(main_root, "Gerente RRHH")
    
    # El mainloop se mantiene hasta que cerrar_sesion lo termine.
    main_root.mainloop()