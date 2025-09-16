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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validar_correo(correo):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo) is not None

def registro():
    correo = user.get().strip()
    nombre_usuario = nombre.get().strip()
    apellido_usuario = apellido.get().strip()
    fecha_nac = fecha_var.get()
    contrasena = code.get()
    rol = rol_var.get()

    # Validación de campos
    if correo in ('', 'Correo Electronico') or nombre_usuario in ('', 'Nombre') or \
       apellido_usuario in ('', 'Apellido') or fecha_nac in ('', 'Fecha de Nacimiento') or \
       contrasena in ('', 'Contraseña') or rol == "Seleccionar Rol":
        messagebox.showerror('Error', 'Por favor, complete todos los campos.')
        return

    if not validar_correo(correo):
        messagebox.showerror('Error', 'Formato de correo inválido.')
        return

    try:
        fecha_obj = datetime.strptime(fecha_nac, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showerror('Error', 'Formato de fecha incorrecto. Use AAAA-MM-DD.')
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
        cursor.execute("SELECT Mail FROM usuario WHERE Mail = %s", (correo,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'El correo ya existe.')
            return

        hashed_pass = hash_password(contrasena)
        cursor.execute("""INSERT INTO usuario 
                          (Nombre, Apellido, Mail, Contrasenia, Fecha_de_nacimiento, Rol, logueado)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                       (nombre_usuario, apellido_usuario, correo, hashed_pass, fecha_obj, rol, 0))
        db.commit()
        messagebox.showinfo('Éxito', '¡Registro exitoso!')

        # Limpiar campos
        for e, placeholder in zip([user, nombre, apellido, fecha_entry, code],
                                  ['Correo Electronico','Nombre','Apellido','Fecha de Nacimiento','Contraseña']):
            e.delete(0, 'end')
            e.insert(0, placeholder)
            if placeholder == 'Contraseña':
                e.config(show='')

        rol_var.set("Seleccionar Rol")
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
        subprocess.Popen(["python", "login.py"])
        root.destroy()
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró login.py")

# --- Entradas y menú ---
frame = Frame(root, width=500, height=550, bg="#1dc1dd")
frame.place(x=480, y=40)

heading = Label(frame, text='Registrarse', fg='white', bg='#1dc1dd', font=('Billie DEMO Light', 23, 'bold'))
heading.place(x=150, y=5)

y_start = 70
y_gap = 60

user = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
user.place(x=30, y=y_start)
user.insert(0, 'Correo Electronico')
user.bind('<FocusIn>', lambda e: on_enter(e, user, 'Correo Electronico'))
user.bind('<FocusOut>', lambda e: on_leave(e, user, 'Correo Electronico'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+25)

nombre = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
nombre.place(x=30, y=y_start+y_gap)
nombre.insert(0, 'Nombre')
nombre.bind('<FocusIn>', lambda e: on_enter(e, nombre, 'Nombre'))
nombre.bind('<FocusOut>', lambda e: on_leave(e, nombre, 'Nombre'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+y_gap+25)

apellido = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
apellido.place(x=30, y=y_start+2*y_gap)
apellido.insert(0, 'Apellido')
apellido.bind('<FocusIn>', lambda e: on_enter(e, apellido, 'Apellido'))
apellido.bind('<FocusOut>', lambda e: on_leave(e, apellido, 'Apellido'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+2*y_gap+25)

fecha_var = StringVar()
fecha_var.set("Fecha de Nacimiento")
fecha_entry = Entry(frame, textvariable=fecha_var, width=35, fg='black', font=('Billie DEMO Light', 11))
fecha_entry.place(x=30, y=y_start+3*y_gap)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+3*y_gap+25)

def abrir_calendario(e):
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

fecha_entry.bind('<Button-1>', abrir_calendario)

code = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11))
code.place(x=30, y=y_start+4*y_gap)
code.insert(0, 'Contraseña')
code.bind('<FocusIn>', lambda e: on_enter(e, code, 'Contraseña'))
code.bind('<FocusOut>', lambda e: on_leave(e, code, 'Contraseña'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=y_start+4*y_gap+25)

rol_var = StringVar()
rol_var.set("Seleccionar Rol")
rol_menu = OptionMenu(frame, rol_var, "Gerente", "Empleado")
rol_menu.config(width=32, font=('Billie DEMO Light', 11), bg="white", fg="black")
rol_menu.place(x=30, y=y_start+5*y_gap)

# --- Botones ---
label = Label(frame, text="¿Tienes cuenta?", fg='white', bg="#1dc1dd", font=('Billie DEMO Light', 11, 'bold'))
label.place(x=75, y=y_start+6*y_gap)

sign_up = Button(frame, width=12, text='Iniciar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
sign_up.place(x=220, y=y_start+6*y_gap)

enter = Button(frame, width=15, text='Registrarse', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=registro)
enter.place(x=150, y=y_start+7*y_gap)

root.mainloop()
