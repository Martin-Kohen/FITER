from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import hashlib

# --- Ventana --- 
root = Tk()
root.title('Login')
root.geometry('1200x500+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False, False)

# --- Función para hashear contraseña ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Función de Login ---
def signin():
    correo_electronico = user.get()
    contraseña = code.get()

    if correo_electronico in ("", "Correo Electronico") or contraseña in ("", "Contraseña"):
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="fiter"
        )
        cursor = db.cursor()
        cursor.execute("SELECT Contrasenia FROM usuario WHERE Mail = %s", (correo_electronico,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "El usuario no existe.")
        else:
            contraseña_bd = result[0]
            if hash_password(contraseña) == contraseña_bd:
                messagebox.showinfo("Éxito", "¡Inicio de sesión correcto!")
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# --- GUI ---
try:
    img = PhotoImage(file='../imagenes/fiterLogo.png')
    Label(root, image=img, bg="#1dc1dd").place(x=50, y=50)
except:
    pass

frame = Frame(root, width=500, height=500, bg="#1dc1dd")
frame.place(x=480, y=70)

heading = Label(frame, text='Iniciar sesión', fg='white', bg='#1dc1dd', font=('Billie DEMO Light', 23, 'bold'))
heading.place(x=87, y=5)

def crear_entry(frame, placeholder, y, show=None):
    entry = Entry(frame, width=35, fg='black', border=0, bg='white', font=('Billie DEMO Light', 11), show=show)
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

user = crear_entry(frame, "Correo Electronico", 60)
code = crear_entry(frame, "Contraseña", 120, show="")

label = Label(frame, text="¿No tenés cuenta?", fg='white', bg="#1dc1dd", font=('Billie DEMO Light', 11, 'bold'))
label.place(x=75, y=180)

def abrir_registro():
    root.destroy()
    subprocess.Popen(["python", "registro.py"])

sign_up = Button(frame, width=10, text='Registrarse', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_registro)
sign_up.place(x=215, y=180)

enter = Button(frame, width=10, text='Entrar', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=signin)
enter.place(x=130, y=220)

root.mainloop()
