from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import hashlib

root = Tk()
root.title('Login')
root.geometry('1200x500+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False, False)

# --- Función para hashear la contraseña ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Función de inicio de sesión ---
def signin():
    correo = user.get().strip()
    contrasena = code.get()

    if correo in ("", "Correo Electronico") or contrasena in ("", "Contraseña"):
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    db = None
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = db.cursor()
        cursor.execute("SELECT idUsuario, Nombre, Contrasenia, Rol FROM usuario WHERE Mail = %s", (correo,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "El usuario no existe.")
            return

        user_id, nombre_usuario, contrasenia_bd, rol = result

        if hash_password(contrasena) == contrasenia_bd:
            # Marcar como logueado
            cursor.execute("UPDATE usuario SET logueado = 1 WHERE idUsuario = %s", (user_id,))
            db.commit()

            messagebox.showinfo("Éxito", f"Bienvenido {nombre_usuario}! Rol: {rol}")
            root.destroy()

            # Según el rol, abrir la página correspondiente
            if rol == "Gerente":
                subprocess.Popen(["python", "home_gerente.py", nombre_usuario])
            elif rol == "Empleado":
                subprocess.Popen(["python", "home.py", nombre_usuario])
           
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

# --- Función para crear entradas con placeholder ---
def crear_entry(frame, placeholder, y, show=None):
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

# --- Interfaz ---
frame = Frame(root, width=500, height=500, bg="#1dc1dd")
frame.place(x=480, y=70)

heading = Label(frame, text='Iniciar sesión', fg='white', bg='#1dc1dd',
                font=('Billie DEMO Light', 23, 'bold'))
heading.place(x=87, y=5)

user = crear_entry(frame, "Correo Electronico", 60)
code = crear_entry(frame, "Contraseña", 120, show="")

def abrir_registro():
    root.destroy()
    subprocess.Popen(["python", "registro.py"])

label = Label(frame, text="¿No tenés cuenta?", fg='white', bg="#1dc1dd",
              font=('Billie DEMO Light', 11, 'bold'))
label.place(x=75, y=180)

sign_up = Button(frame, width=10, text='Registrarse', border=0, bg="#0089a1",
                 cursor='hand2', fg="#ffffff", command=abrir_registro)
sign_up.place(x=215, y=180)

enter = Button(frame, width=10, text='Entrar', border=0, bg="#0089a1",
               cursor='hand2', fg="#ffffff", command=signin)
enter.place(x=130, y=220)

root.mainloop()
