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
    entry = Entry(frame, width=35, fg='black', border=0, bg='white',
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
                target_script = "home_gerente.py"
            elif id_departamento == ID_DEPARTAMENTO_RRHH:
                target_script = "rrhh_empleado.py"
            elif id_departamento == ID_DEPARTAMENTO_Finanzas:
                target_script = "finanzas.py"
            elif id_departamento == ID_DEPARTAMENTO_Marketing:
                target_script = "marketing.py"
            elif id_departamento == ID_DEPARTAMENTO_Servicio_al_cliente:
                target_script = "servicio_cliente.py"
            elif id_departamento == ID_DEPARTAMENTO_Logistica:
                target_script = "logistica.py"
            elif id_departamento == ID_DEPARTAMENTO_Direccion:
                target_script = "home_direccion.py" 
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
    root_window.geometry('1200x500+300+200')
    root_window.configure(bg="#1dc1dd")
    root_window.resizable(False, False)

    # --- Interfaz ---
    frame = Frame(root_window, width=500, height=500, bg="#1dc1dd")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Iniciar sesión', fg='white', bg='#1dc1dd',
                    font=('Billie DEMO Light', 23, 'bold'))
    heading.place(x=87, y=5)

    # Asignación de variables globales de Entrada
    user = crear_entry(frame, "Correo Electronico", 60)
    code = crear_entry(frame, "Contraseña", 120, show="")

    def abrir_registro():
        root_window.destroy()
        subprocess.Popen([sys.executable, "registro.py"])

    label = Label(frame, text="¿No tenés cuenta?", fg='white', bg="#1dc1dd",
                  font=('Billie DEMO Light', 11, 'bold'))
    label.place(x=75, y=180)

    sign_up = Button(frame, width=10, text='Registrarse', border=0, bg="#0089a1",
                     cursor='hand2', fg="#ffffff", command=abrir_registro)
    sign_up.place(x=215, y=180)

    # El botón llama a la función de manejo de inicio de sesión
    enter = Button(frame, width=10, text='Entrar', border=0, bg="#0089a1",
                     cursor='hand2', fg="#ffffff", command=lambda: _handle_signin(root_window))
    enter.place(x=130, y=220)


# =======================================================
# 🚀 EJECUCIÓN DEL MÓDULO
# =======================================================
if __name__ == '__main__':
    main_root = Tk()
    abrir_login(main_root)
    main_root.mainloop()