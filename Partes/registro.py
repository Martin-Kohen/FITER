from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
from tkcalendar import Calendar
from datetime import datetime
import hashlib
import re

root = Tk()
root.title('Registro')
root.geometry('1200x600+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False, False)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Asegúrate de poner tu contraseña de MySQL si tienes una
    "database": "fiter"
}
# -------------------------------------

# Variable global para mapear Nombre de Área a ID
DEPARTAMENTOS_MAP = {}

def hash_password(password):
    """Genera el hash SHA-256 de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

def validar_correo(correo):
    """Valida el formato básico del correo electrónico."""
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo) is not None

def conectar_bd():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        # Aquí no mostramos error crítico si es solo al inicio, lo manejamos en get_areas_from_db
        return None

def get_areas_from_db():
    """Obtiene los nombres y IDs de los departamentos y los guarda en DEPARTAMENTOS_MAP."""
    global DEPARTAMENTOS_MAP
    db = conectar_bd()
    areas_nombres = []
    
    # Resetear el mapa antes de cargar
    DEPARTAMENTOS_MAP = {}
    
    if db:
        cursor = db.cursor()
        try:
            # Consulta la tabla 'departamentos'
            cursor.execute("SELECT ID_Departamento, Nombre FROM departamentos ORDER BY Nombre")
            for (id_dep, nombre) in cursor:
                DEPARTAMENTOS_MAP[nombre] = id_dep # Mapeamos Nombre -> ID
                areas_nombres.append(nombre)
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"No se pudo leer la tabla 'departamentos': {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
    
    if not areas_nombres:
        return ["Error al cargar (BD desconectada)"]
        
    return areas_nombres

def recargar_areas():
    """Recarga la lista de áreas disponibles y actualiza el OptionMenu."""
    global areas_disponibles
    # Obtener la nueva lista de áreas de la BD
    nuevas_areas = get_areas_from_db()
    
    # 1. Quitar el OptionMenu anterior
    global area_menu 
    area_menu.destroy()
    
    # 2. Crear un nuevo OptionMenu con las opciones actualizadas
    areas_disponibles = nuevas_areas
    area_var.set("Seleccionar Área") # Resetear selección

    # Recrea el OptionMenu con las nuevas opciones. Se usa un * para desempaquetar la lista.
    area_menu = OptionMenu(frame, area_var, *areas_disponibles)
    area_menu.config(width=14, font=('Billie DEMO Light', 11), bg="white", fg="black")
    area_menu.place(x=200, y=y_start+5*y_gap)
    
    if "Error al cargar" in areas_disponibles[0] if areas_disponibles else "":
         messagebox.showwarning("Recarga", "No se pudo conectar a la base de datos o cargar las áreas.")
    else:
        messagebox.showinfo("Recarga", "Áreas recargadas exitosamente.")
        
def insertar_propuesta_reclutamiento(cursor, nombre, apellido, rol, area_nombre):
    """Inserta una nueva propuesta de trabajo en la tabla 'reclutamiento'."""
    try:
        descripcion = f"Propuesta de Autoregistro - Puesto: {rol} en Área: {area_nombre}. Usuario: {nombre} {apellido}"
        fecha_solicitud = datetime.now().strftime('%Y-%m-%d')
        
        sql_insert = """
        INSERT INTO reclutamiento 
        (Fecha_Solicitud, Descripcion_Puesto, Salario_Ofrecido, Estado_Proceso) 
        VALUES (%s, %s, %s, %s)
        """
        # Salario_Ofrecido se deja como NULL y Estado_Proceso como 'Pendiente RRHH'
        cursor.execute(sql_insert, (fecha_solicitud, descripcion, None, 'Pendiente RRHH'))
        
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Error de BD", f"Error al crear propuesta de reclutamiento: {err}")
        return False

# --- Cargar las áreas al inicio ---
areas_disponibles = get_areas_from_db()

def registro():
    correo = user.get().strip()
    nombre_usuario = nombre.get().strip()
    apellido_usuario = apellido.get().strip()
    fecha_nac = fecha_var.get()
    contrasena = code.get()
    rol = rol_var.get()
    area_nombre = area_var.get()

    # 1. Validación de campos inicial
    if correo in ('', 'Correo Electronico') or nombre_usuario in ('', 'Nombre') or \
       apellido_usuario in ('', 'Apellido') or fecha_nac in ('', 'Fecha de Nacimiento') or \
       contrasena in ('', 'Contraseña') or rol == "Seleccionar Rol" or area_nombre == "Seleccionar Área" or "Error al cargar" in area_nombre:
        messagebox.showerror('Error', 'Por favor, complete todos los campos y seleccione un Área válida.')
        return

    if not validar_correo(correo):
        messagebox.showerror('Error', 'Formato de correo inválido.')
        return

    try:
        fecha_obj = datetime.strptime(fecha_nac, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showerror('Error', 'Formato de fecha incorrecto. Use AAAA-MM-DD.')
        return

    # OBTENER EL ID DEL DEPARTAMENTO
    id_departamento_seleccionado = DEPARTAMENTOS_MAP.get(area_nombre)
    if id_departamento_seleccionado is None:
          messagebox.showerror('Error', 'ID de Departamento no encontrado. Intente recargar.')
          return
          
    db = conectar_bd()
    if not db: 
        messagebox.showerror('Error', 'No se pudo conectar a la base de datos.')
        return
    
    cursor = db.cursor()
    id_empleado = None

    try:
        # --- 2. VALIDACIÓN CRÍTICA CONTRA RR.HH. (Empleados_RRHH) ---
        # Se verifica si el usuario existe como empleado de alta en RR.HH.
        sql_rrhh = "SELECT ID_Empleado FROM Empleados_RRHH WHERE Nombre = %s AND Apellido = %s AND Puesto = %s AND Departamento = %s"
        cursor.execute(sql_rrhh, (nombre_usuario, apellido_usuario, rol, area_nombre))
        empleado_data = cursor.fetchone()

        if not empleado_data:
            # --- MODIFICACIÓN CLAVE: NO ENCONTRADO EN RRHH, CREAR PROPUESTA ---
            if insertar_propuesta_reclutamiento(cursor, nombre_usuario, apellido_usuario, rol, area_nombre):
                db.commit() # Confirmar la inserción en reclutamiento
                messagebox.showwarning('Propuesta Enviada 📧', 
                                         f'El usuario {nombre_usuario} {apellido_usuario} no está en RR.HH.!\n'
                                         'Se ha generado una **Propuesta de Trabajo** para que RR.HH. la revise. No se creó la cuenta.')
            return # Termina la función aquí, no hay cuenta de usuario
            # --- FIN MODIFICACIÓN ---

        id_empleado = empleado_data[0] # Si existe, tomamos el ID

        # --- 3. VALIDACIÓN DE DUPLICADOS EN USUARIO ---
        # Validación por Correo
        cursor.execute("SELECT Mail FROM usuario WHERE Mail = %s", (correo,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'El correo ya existe.')
            return

        # Validación por ID de Empleado (idUsuario)
        cursor.execute("SELECT idUsuario FROM usuario WHERE idUsuario = %s", (id_empleado,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'Ya existe una cuenta para este ID de empleado. Inicie sesión.')
            return

        # --- 4. INSERCIÓN EN LA TABLA DE USUARIO ---
        hashed_pass = hash_password(contrasena)
        
        sql_insert = """INSERT INTO usuario 
                             (idUsuario, Nombre, Apellido, Mail, Contrasenia, Fecha_de_nacimiento, Rol, id_departamento, logueado)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                             
        cursor.execute(sql_insert,
                        (id_empleado, nombre_usuario, apellido_usuario, correo, hashed_pass, fecha_obj, rol, id_departamento_seleccionado, 0))
        db.commit()
        messagebox.showinfo('Éxito', f'¡Registro exitoso!\nID de Usuario: {id_empleado}.')

        # Limpiar campos y navegar
        for e, placeholder in zip([user, nombre, apellido, fecha_entry, code],
                                 ['Correo Electronico','Nombre','Apellido','Fecha de Nacimiento','Contraseña']):
            e.delete(0, 'end')
            e.insert(0, placeholder)
            if placeholder == 'Contraseña':
                e.config(show='')

        rol_var.set("Seleccionar Rol")
        area_var.set("Seleccionar Área")
        abrir_login()
    except Exception as e:
        messagebox.showerror('Error Inesperado', f'Ocurrió un error: {e}')
        if db and db.is_connected():
            db.rollback()
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

def on_enter(e, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, 'end')
        if placeholder == 'Contraseña':
            entry.config(show='*')

def on_leave(e, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        if placeholder == 'Contraseña':
            entry.config(show='')

def abrir_login():
    try:
        # Intenta abrir el script login.py en un nuevo proceso
        subprocess.Popen(["python", "login.py"])
        # Cierra la ventana actual de registro
        root.destroy()
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró login.py. Asegúrate de que está en el mismo directorio.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar login.py: {e}")

# Fecha de Nacimiento
fecha_var = StringVar()
fecha_var.set("Fecha de Nacimiento")

def abrir_calendario(e):
    # Asegura que el placeholder se quite al abrir el calendario
    if fecha_var.get() == "Fecha de Nacimiento":
        fecha_var.set("") 
        
    x = fecha_entry.winfo_rootx()
    y = fecha_entry.winfo_rooty() + fecha_entry.winfo_height()
    top = Toplevel(root)
    top.geometry(f"+{x}+{y}")
    top.grab_set()
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(padx=10, pady=10)
    def seleccionar():
        fecha_var.set(cal.get_date())
        top.destroy()
    Button(top, text="Seleccionar", command=seleccionar).pack(pady=5)

# -----------------------------------------------------------------------
# --- CÓDIGO DE INTERFAZ ---
# -----------------------------------------------------------------------

frame = Frame(root, width=500, height=550, bg="#1dc1dd")
frame.place(x=480, y=40)

heading = Label(frame, text='Registrarse', fg='white', bg='#1dc1dd', font=('Billie DEMO Light', 23, 'bold'))
heading.place(x=150, y=5)

y_start = 70
y_gap = 60

# Correo
user = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
user.place(x=30, y=y_start)
user.insert(0, 'Correo Electronico')
user.bind('<FocusIn>', lambda e: on_enter(e, user, 'Correo Electronico'))
user.bind('<FocusOut>', lambda e: on_leave(e, user, 'Correo Electronico'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+25)

# Nombre
nombre = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
nombre.place(x=30, y=y_start+y_gap)
nombre.insert(0, 'Nombre')
nombre.bind('<FocusIn>', lambda e: on_enter(e, nombre, 'Nombre'))
nombre.bind('<FocusOut>', lambda e: on_leave(e, nombre, 'Nombre'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+y_gap+25)

# Apellido
apellido = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
apellido.place(x=30, y=y_start+2*y_gap)
apellido.insert(0, 'Apellido')
apellido.bind('<FocusIn>', lambda e: on_enter(e, apellido, 'Apellido'))
apellido.bind('<FocusOut>', lambda e: on_leave(e, apellido, 'Apellido'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+2*y_gap+25)

# Fecha de Nacimiento
fecha_entry = Entry(frame, textvariable=fecha_var, width=35, fg='black', font=('Billie DEMO Light', 11))
fecha_entry.place(x=30, y=y_start+3*y_gap)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+3*y_gap+25)
fecha_entry.bind('<Button-1>', abrir_calendario)

# Contraseña
code = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
code.place(x=30, y=y_start+4*y_gap)
code.insert(0, 'Contraseña')
code.bind('<FocusIn>', lambda e: on_enter(e, code, 'Contraseña'))
code.bind('<FocusOut>', lambda e: on_leave(e, code, 'Contraseña'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+4*y_gap+25)


# Menú Rol
rol_var = StringVar()
rol_var.set("Seleccionar Rol")
rol_menu = OptionMenu(frame, rol_var, "Gerente", "Empleado")
rol_menu.config(width=14, font=('Billie DEMO Light', 11), bg="white", fg="black")
rol_menu.place(x=30, y=y_start+5*y_gap) 

# Menú Área (Cargado dinámicamente)
area_var = StringVar()
area_var.set("Seleccionar Área")

# Inicialización del OptionMenu (puede contener "Error al cargar" al inicio)
area_menu = OptionMenu(frame, area_var, *areas_disponibles)
area_menu.config(width=14, font=('Billie DEMO Light', 11), bg="white", fg="black")
area_menu.place(x=200, y=y_start+5*y_gap) 

# Botón para Recargar Áreas 🔄
reload_button = Button(frame, text='🔄', command=recargar_areas, 
                       font=('Billie DEMO Light', 10, 'bold'), width=2, height=1,
                       bg="#0089a1", fg="#ffffff", cursor='hand2', border=0)
reload_button.place(x=370, y=y_start+5*y_gap) 

# --- Botones ---
label = Label(frame, text="¿Tienes cuenta?", fg='white', bg="#1dc1dd", font=('Billie DEMO Light', 11, 'bold'))
label.place(x=75, y=y_start+6*y_gap)

sign_up = Button(frame, width=12, text='Iniciar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
sign_up.place(x=220, y=y_start+6*y_gap)

enter = Button(frame, width=15, text='Registrarse', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=registro)
enter.place(x=150, y=y_start+7*y_gap)

root.mainloop()