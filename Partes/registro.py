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

# --- NUEVA FUNCIÓN PARA MANEJAR EL CAMBIO DE ROL ---
def handle_rol_change(*args):
    """Muestra u oculta el menú de Área y el botón de recarga basándose en el Rol seleccionado."""
    
    global area_menu, reload_button
    
    if rol_var.get() == "Gerente":
        # Ocultar menú de Área y botón de recarga
        area_menu.place_forget()
        reload_button.place_forget()
        area_var.set("Gerente (Todos)") # Establecer un valor por defecto que no cause error.
    else:
        # Mostrar menú de Área y botón de recarga
        area_menu.place(x=200, y=y_start+5*y_gap)
        reload_button.place(x=370, y=y_start+5*y_gap)
        if area_var.get() == "Gerente (Todos)":
             area_var.set("Seleccionar Área") # Resetear a la selección original
# ----------------------------------------------------
        
# --- Cargar las áreas al inicio ---
areas_disponibles = get_areas_from_db()

def registro():
    correo = user.get().strip()
    nombre_usuario = nombre.get().strip()
    apellido_usuario = apellido.get().strip()
    fecha_nac = fecha_var.get()
    contrasena = code.get()
    rol = rol_var.get()
    area_nombre = area_var.get() # Puede ser "Gerente (Todos)" o un nombre de área real

    # 1. Validación de campos inicial
    # Validamos el área solo si el rol NO es Gerente, o si es Gerente y el placeholder sigue ahí
    if correo in ('', 'Correo Electronico') or nombre_usuario in ('', 'Nombre') or \
       apellido_usuario in ('', 'Apellido') or fecha_nac in ('', 'Fecha de Nacimiento') or \
       contrasena in ('', 'Contraseña') or rol == "Seleccionar Rol" or \
       (rol != "Gerente" and (area_nombre == "Seleccionar Área" or "Error al cargar" in area_nombre)):
        
        messagebox.showerror('Error', 'Por favor, complete todos los campos y seleccione un Área válida (o seleccione Gerente).')
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
    # Gerente: Usamos 0 o NULL para representar "todos" o "sin departamento específico"
    # IMPORTANTE: Debes asegurarte que tu columna ID_Departamento en 'usuario' acepte NULL o que 0 sea un ID válido para Gerente.
    if rol == "Gerente":
        id_departamento_seleccionado = 0 # Usamos 0 como un ID genérico para Gerentes
        area_nombre_busqueda = "Todos" # Usamos un nombre genérico para la búsqueda
        
        # VALIDACIÓN EXTRA: Si el rol es Gerente, deberías tener un registro en empleados_rrhh
        # que NO use ID_Departamento para la validación, o que use 0.
        # Para simplificar y mantener el flujo, buscaremos sin el ID de departamento.
        sql_rrhh = "SELECT ID_Empleado FROM empleados_rrhh WHERE Nombre = %s AND Apellido = %s AND Puesto = %s"
        empleado_params = (nombre_usuario, apellido_usuario, rol)

    else:
        # Empleado: Usamos el mapeo normal
        id_departamento_seleccionado = DEPARTAMENTOS_MAP.get(area_nombre)
        area_nombre_busqueda = area_nombre
        if id_departamento_seleccionado is None:
              messagebox.showerror('Error', 'ID de Departamento no encontrado. Intente recargar.')
              return
        
        # Consulta normal con ID_Departamento
        sql_rrhh = "SELECT ID_Empleado FROM empleados_rrhh WHERE Nombre = %s AND Apellido = %s AND Puesto = %s AND ID_Departamento = %s"
        empleado_params = (nombre_usuario, apellido_usuario, rol, id_departamento_seleccionado)


    db = conectar_bd()
    if not db: 
        messagebox.showerror('Error', 'No se pudo conectar a la base de datos.')
        return
    
    cursor = db.cursor()
    id_empleado = None

    try:
        # --- 2. VALIDACIÓN CRÍTICA CONTRA RR.HH. (empleados_rrhh) ---
        cursor.execute(sql_rrhh, empleado_params)
        empleado_data = cursor.fetchone()

        if not empleado_data:
            messagebox.showerror('Error de RR.HH.', 
                                 f'El usuario {nombre_usuario} {apellido_usuario} (Rol: {rol}) no está registrado en RR.HH.\n'
                                 'No se puede crear la cuenta de usuario.')
            return

        id_empleado = empleado_data[0] # Si existe, tomamos el ID

        # --- 3. VALIDACIÓN DE DUPLICADOS EN USUARIO ---
        # (código para verificar correo y idUsuario)
        cursor.execute("SELECT Mail FROM usuario WHERE Mail = %s", (correo,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'El correo ya existe.')
            return

        cursor.execute("SELECT idUsuario FROM usuario WHERE idUsuario = %s", (id_empleado,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'Ya existe una cuenta para este ID de empleado. Inicie sesión.')
            return

        # --- 4. INSERCIÓN EN LA TABLA DE USUARIO ---
        hashed_pass = hash_password(contrasena)
        
        sql_insert = """INSERT INTO usuario 
                             (idUsuario, Nombre, Apellido, Mail, Contrasenia, Fecha_de_nacimiento, Rol, id_departamento, logueado)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                             
        # Si es Gerente, insertamos 0 en id_departamento_seleccionado
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
# --- RASTREAR EL CAMBIO DE ROL ---
rol_var.trace("w", handle_rol_change)
# ---------------------------------

# Menú Área (Cargado dinámicamente)
area_var = StringVar()
area_var.set("Seleccionar Área")

# Inicialización del OptionMenu 
area_menu = OptionMenu(frame, area_var, *areas_disponibles)
area_menu.config(width=14, font=('Billie DEMO Light', 11), bg="white", fg="black")
area_menu.place(x=200, y=y_start+5*y_gap) 

# --- Botones ---
label = Label(frame, text="¿Tienes cuenta?", fg='white', bg="#1dc1dd", font=('Billie DEMO Light', 11, 'bold'))
label.place(x=75, y=y_start+6*y_gap)

sign_up = Button(frame, width=12, text='Iniciar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
sign_up.place(x=220, y=y_start+6*y_gap)

enter = Button(frame, width=15, text='Registrarse', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=registro)
enter.place(x=150, y=y_start+7*y_gap)

root.mainloop()