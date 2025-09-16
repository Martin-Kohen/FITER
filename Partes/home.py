from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import sys

root = Tk()
root.title("Home")
root.state("zoomed")   
root.configure(bg="#1dc1dd")

# --- Conexión a la BD ---
def conectar_db():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="", 
        database="fiter"  
    )

# --- Cerrar sesión ---
def cerrar_sesion():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET logueado=0 WHERE logueado=1")
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cerrar sesión: {e}")
        return
    root.destroy()
    subprocess.Popen(["python", "login.py"])

# --- Obtener nombre de usuario desde argumento ---
if len(sys.argv) > 1:
    nombre_usuario = sys.argv[1]
else:
    nombre_usuario = "Usuario"

# --- Interfaz ---
frame = Frame(root, bg="#1dc1dd")
frame.pack(fill="both", expand=True)

# Botón de sesión
if nombre_usuario != "Usuario":
    btn_sesion = Button(frame, width=15, text='Cerrar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=cerrar_sesion)
else:
    btn_sesion = Button(frame, width=15, text='Iniciar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: subprocess.Popen(["python", "login.py"]))
btn_sesion.place(x=215, y=335)

# Mensaje de bienvenida
heading = Label(frame, text=f"Bienvenido {nombre_usuario}", fg="white", bg="#1dc1dd", font=("Billie DEMO Light", 23, "bold"))
heading.place(relx=0.5, rely=0.06, anchor="center")

root.mainloop()
