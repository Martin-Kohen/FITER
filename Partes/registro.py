from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import re
from tkcalendar import DateEntry
from datetime import datetime
import hashlib

# --- Ventana ---
root = Tk()
root.title('Registro')
root.geometry('1200x500+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False, False)

# --- Función para hashear contraseña ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validar_correo(correo):
    return "@" in correo and "." in correo.split("@")[-1]

# --- Función de Registro ---
def registro():
    CorreoElectronico = user.get()
    Nombre = nombre.get()
    Apellido = apellido.get()
    Fecha_de_nacimiento = date.get()
    Contrasena = code.get()

    # --- Verificar campos vacíos ---
    if (CorreoElectronico in ('', 'Correo Electronico') or 
        Nombre in ('', 'Nombre') or 
        Apellido in ('', 'Apellido') or 
        Fecha_de_nacimiento in ('', 'Fecha de Nacimiento') or 
        Contrasena in ('', 'Contraseña')):
        messagebox.showerror('Error', 'Por favor, complete todos los campos.')
        return

    # --- Validar formato del correo ---
    if not validar_correo(CorreoElectronico):
        messagebox.showerror('Error de Correo', 'Formato de correo inválido.')
        return

    # --- Validar fecha ---
    try:
        fecha_obj = datetime.strptime(Fecha_de_nacimiento, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showerror('Error de Fecha', 'Formato de fecha incorrecto. Use AAAA-MM-DD.')
        return

    db = None
    try:
        db = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="root", 
            database="fiter"
        )
        cursor = db.cursor()
        cursor.execute("SELECT Mail FROM usuario WHERE Mail = %s", (CorreoElectronico,))
        result = cursor.fetchone()
        if result:
            messagebox.showerror('Error', 'El correo ya existe.')
            return

        hashed_password = hash_password(Contrasena)

        sql = "INSERT INTO usuario (Nombre, Apellido, Mail, Contrasenia, Fecha_de_nacimiento) VALUES (%s, %s, %s, %s, %s)"
        val = (Nombre, Apellido, CorreoElectronico, hashed_password, fecha_obj)
        cursor.execute(sql, val)
        db.commit()
        messagebox.showinfo('Éxito', '¡Registro exitoso!')

        # Limpiar entradas
        for e, placeholder in zip([user, nombre, apellido, date, code], 
                                  ['Correo Electronico', 'Nombre', 'Apellido', 'Fecha de Nacimiento', 'Contraseña']):
            e.delete(0, 'end')
            e.insert(0, placeholder)
            if placeholder == 'Contraseña':
                e.config(show='')
                abrir_login()

    except Exception as e:
        messagebox.showerror('Error Inesperado', f'Ocurrió un error: {e}')
        if db and db.is_connected():
            db.rollback()
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

# --- Entradas ---
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
    root.destroy()
    subprocess.Popen(["python", "login.py"])

try:
    img = PhotoImage(file='../imagenes/fiterLogo.png')
    Label(root, image=img, bg="#1dc1dd").place(x=50, y=50)
except:
    pass

frame = Frame(root, width=500, height=500, bg="#1dc1dd")
frame.place(x=480, y=70)

heading = Label(frame, text='Registrarse', fg='white', bg="#1dc1dd", font=('Billie DEMO Light', 23, 'bold'))
heading.place(x=87, y=5)

user = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
user.place(x=30, y=60)
user.insert(0, 'Correo Electronico')
user.bind('<FocusIn>', lambda e: on_enter(e, user, 'Correo Electronico'))
user.bind('<FocusOut>', lambda e: on_leave(e, user, 'Correo Electronico'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=87)

nombre = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
nombre.place(x=30, y=120)
nombre.insert(0, 'Nombre')
nombre.bind('<FocusIn>', lambda e: on_enter(e, nombre, 'Nombre'))
nombre.bind('<FocusOut>', lambda e: on_leave(e, nombre, 'Nombre'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=147)

apellido = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
apellido.place(x=30, y=180)
apellido.insert(0, 'Apellido')
apellido.bind('<FocusIn>', lambda e: on_enter(e, apellido, 'Apellido'))
apellido.bind('<FocusOut>', lambda e: on_leave(e, apellido, 'Apellido'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=207)

date = DateEntry(frame, width=43, foreground='black', borderwidth=2, background='white', date_pattern="yyyy-mm-dd")
date.place(x=30, y=240)
date.insert(0, 'Fecha de Nacimiento')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=267)

code = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
code.place(x=30, y=300)
code.insert(0, 'Contraseña')
code.bind('<FocusIn>', lambda e: on_enter(e, code, 'Contraseña'))
code.bind('<FocusOut>', lambda e: on_leave(e, code, 'Contraseña'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=327)

label = Label(frame, text="¿Tienes cuenta?", fg='white', bg="#1dc1dd", font=('Billie DEMO Light', 11, 'bold'))
label.place(x=75, y=335)

sign_up = Button(frame, width=10, text='Iniciar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
sign_up.place(x=215, y=335)

enter = Button(frame, width=10, text='Entrar', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=registro)
enter.place(x=130, y=370)

root.mainloop()
