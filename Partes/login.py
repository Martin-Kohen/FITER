from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import hashlib
import sys

# --- Constantes de Departamento ---
ID_DEPARTAMENTO_Direccion = 1 
ID_DEPARTAMENTO_RRHH = 2 
ID_DEPARTAMENTO_Finanzas = 3 
ID_DEPARTAMENTO_Marketing = 4 
ID_DEPARTAMENTO_Servicio_al_cliente = 5
ID_DEPARTAMENTO_Logistica = 6 

# --- Variables Globales para las Entradas ---
user = None 
code = None


# --- Función para hashear la contraseña (CRÍTICA) ---
def hash_password(password):
    """Retorna el hash SHA256 de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- Función Auxiliar para la Conexión ---
def conectar_bd():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {err}")
        return None

# --- Función para crear entradas con placeholder ---
def crear_entry(frame, placeholder, y, show=None):
    """Crea un campo de entrada (Entry) con lógica de placeholder."""
    # Reducimos un poco el ancho del Entry para el frame más pequeño
    entry = Entry(frame, width=30, fg='black', border=0, bg='white',
                  font=('Billie DEMO Light', 11), show=show)
    entry.place(x=30, y=y)
    entry.insert(0, placeholder)

    def on_enter(e):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            if placeholder == "Contraseña":
                entry.config(show="*")

    def on_leave(e):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Contraseña":
                entry.config(show="")

    entry.bind("<FocusIn>", on_enter)
    entry.bind("<FocusOut>", on_leave)
    return entry


# ---------------------------------------------------
# --- Lógica de Inicio de Sesión y Redirección ---
# ---------------------------------------------------

def _handle_signin(root_window):
    """Maneja el inicio de sesión, autenticación y redirección."""
    global user, code
    
    correo = user.get().strip()
    contrasena = code.get()

    if correo in ("", "Correo Electronico") or contrasena in ("", "Contraseña"):
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    db = conectar_bd()
    if not db: 
        return
    
    cursor = db.cursor()

    try:
        sql_query = "SELECT idUsuario, Nombre, Contrasenia, Rol, ID_Departamento FROM usuario WHERE Mail = %s"
        cursor.execute(sql_query, (correo,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "El usuario no existe.")
            return

        user_id, nombre_usuario, contrasenia_bd, rol, id_departamento = result

        # ✅ VERIFICACIÓN DEL HASH: Compara el hash de la contraseña ingresada con el hash de la BD
        if hash_password(contrasena) == contrasenia_bd:
            
            # 1. Marcar como logueado
            cursor.execute("UPDATE usuario SET logueado = 1 WHERE idUsuario = %s", (user_id,))
            db.commit()

            messagebox.showinfo("Éxito", f"Bienvenido {nombre_usuario}! Rol: {rol} (Depto ID: {id_departamento})")
            root_window.destroy() # Cierra la ventana de login
            
            # 2. LÓGICA DE REDIRECCIÓN BASADA EN ROL Y ID_DEPARTAMENTO
            target_script = None
            
            if rol == "Gerente":
                target_script = "Partes/home_gerente.py"
            elif id_departamento == ID_DEPARTAMENTO_RRHH:
                target_script = "Partes/rrhh_empleado.py"
            elif id_departamento == ID_DEPARTAMENTO_Finanzas:
                target_script = "Partes/finanzas.py"
            elif id_departamento == ID_DEPARTAMENTO_Marketing:
                target_script = "Partes/marketing.py"
            elif id_departamento == ID_DEPARTAMENTO_Servicio_al_cliente:
                target_script = "Partes/servicio_cliente.py"
            elif id_departamento == ID_DEPARTAMENTO_Logistica:
                target_script = "Partes/sedes.py"
            elif id_departamento == ID_DEPARTAMENTO_Direccion:
                target_script = "Partes/home_direccion.py" 
            else:
                if id_departamento is not None:
                    target_script = "home.py"

            if target_script:
                # 🚨 CORRECCIÓN CLAVE: Pasamos el nombre de usuario Y el rol
                subprocess.Popen([sys.executable, target_script, nombre_usuario, rol])
            else:
                messagebox.showerror("Error de Asignación", 
                                     f"El usuario tiene un rol ({rol}) o departamento ({id_departamento}) sin ventana de inicio asignada.")

        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error de BD", f"Error durante el inicio de sesión: {err}")
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()


# ---------------------------------------------------
# --- Ventana Principal de Login ---
# ---------------------------------------------------

def abrir_login(root_window):
    """
    Función que configura e inicia la interfaz de login. 
    """
    global user, code
    
    if not root_window.winfo_ismapped():
        root_window.deiconify() 
    
    for widget in root_window.winfo_children():
        widget.destroy()

    root_window.title('Login')
    # 📏 CAMBIO CLAVE: Reducir el tamaño de la ventana a 400x300
    root_window.geometry('400x300+400+250') 
    root_window.configure(bg="#1dc1dd")
    root_window.resizable(False, False)

    # --- Interfaz ---
    # Reducir el frame para que quepa en la ventana pequeña y centrarlo
    frame = Frame(root_window, width=350, height=250, bg="#1dc1dd")
    # Colocar el frame en el centro de la nueva ventana (400-350)/2 = 25
    frame.place(x=25, y=25)

    heading = Label(frame, text='Iniciar sesión', fg='white', bg='#1dc1dd',
                    font=('Billie DEMO Light', 20, 'bold')) # Reducir un poco el tamaño de fuente
    # Ajustar posición del título para centrarlo en el frame de 350px de ancho
    heading.place(x=85, y=5)

    # Asignación de variables globales de Entrada
    # La y=60 y y=120 es relativa al nuevo frame
    user = crear_entry(frame, "Correo Electronico", 60) 
    code = crear_entry(frame, "Contraseña", 110, show="") # Subimos un poco la contraseña

    # El botón llama a la función de manejo de inicio de sesión
    # Se ajusta la posición y para estar cerca de los campos de entrada
    enter = Button(frame, width=10, text='Entrar', border=0, bg="#0089a1",
                      cursor='hand2', fg="#ffffff", command=lambda: _handle_signin(root_window))
    # Centrar el botón en el frame (350/2 - 70/2 = 175 - 35 = 140)
    enter.place(x=140, y=170) 


# =======================================================
# 🚀 EJECUCIÓN DEL MÓDULO
# =======================================================
if __name__ == '__main__':
    main_root = Tk()
    abrir_login(main_root)
    main_root.mainloop()