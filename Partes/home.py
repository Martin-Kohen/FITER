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

if len(sys.argv) > 1:
    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)
    nombre_usuario = sys.argv[1] 
    sign_up = Button(frame, width=10, text='Cerrar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_home)
    sign_up.place(x=215, y=335)
    
else:
    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)
    nombre_usuario = "Usuario"
    sign_up = Button(frame, width=10, text='Iniciar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_login)
    sign_up.place(x=215, y=335)



heading = Label(frame, text=f"Bienvenido {nombre_usuario}", fg="white", bg="#1dc1dd", font=("Billie DEMO Light", 23, "bold"))
heading.place(relx=0.5, rely=0.06, anchor="center")



root.mainloop()


