from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import re
from tkcalendar import Calendar
from datetime import datetime
import hashlib
import sys

root = Tk()
root.title("Home")
root.state("zoomed")   
root.configure(bg="#1dc1dd")

def abrir_login():
    root.destroy()
    subprocess.Popen(["python", "login.py"])

def abrir_home():
    root.destroy()
    subprocess.Popen(["python", "home_deslog.py"])

# --- Verifica si hay argumentos (usuario logueado o no) ---
if len(sys.argv) > 1:
    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)
    nombre_usuario = sys.argv[1] 
    sign_up = Button(frame, width=15, text='Cerrar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_home)
    sign_up.place(x=215, y=250)
    logistica = Button(frame, width=30, text='Ver información de Logística', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
    logistica.place(x=215, y=300)

    servicio_cliente = Button(frame, width=30, text='Ver información de Servicio al Cliente', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
    servicio_cliente.place(x=215, y=350)

    marketing = Button(frame, width=30, text='Ver información de Marketing', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
    marketing.place(x=215, y=400)

    finanzas = Button(frame, width=30, text='Ver información de Finanzas', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
    finanzas.place(x=215, y=450)

    rrhh = Button(frame, width=30, text='Ver información de RRHH', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
    rrhh.place(x=215, y=500)

    # --- Mensaje de bienvenida ---
    heading = Label(frame, text=f"Bienvenido {nombre_usuario}", fg="white", bg="#1dc1dd", font=("Billie DEMO Light", 23, "bold"))
    heading.place(relx=0.5, rely=0.06, anchor="center")
else:
    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)
    nombre_usuario = "Usuario"
    sign_up = Button(frame, width=15, text='Iniciar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
    sign_up.place(x=215, y=250)

# --- Botones de módulos ---
logistica = Button(frame, width=30, text='Ver información de Logística', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
logistica.place(x=215, y=300)

servicio_cliente = Button(frame, width=30, text='Ver información de Servicio al Cliente', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
servicio_cliente.place(x=215, y=350)

marketing = Button(frame, width=30, text='Ver información de Marketing', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
marketing.place(x=215, y=400)

finanzas = Button(frame, width=30, text='Ver información de Finanzas', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
finanzas.place(x=215, y=450)

rrhh = Button(frame, width=30, text='Ver información de RRHH', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
rrhh.place(x=215, y=500)

# --- Mensaje de bienvenida ---
heading = Label(frame, text=f"Bienvenido {nombre_usuario}", fg="white", bg="#1dc1dd", font=("Billie DEMO Light", 23, "bold"))
heading.place(relx=0.5, rely=0.06, anchor="center")

root.mainloop()
