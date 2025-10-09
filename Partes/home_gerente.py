from tkinter import *
import sys
from sedes import abrir_sedes
from servicio_cliente import abrir_servicio_cliente  
from marketing import abrir_marketing
from finanzas import abrir_finanzas
from rrhh import abrir_rrhh

def abrir_home(nombre_usuario):
    # Crear ventana principal
    root = Tk()
    root.title("Home")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)

    # --- Botón de Cerrar Sesión ---
    sign_up = Button(frame, width=15, text='Cerrar Sesión', border=0, bg="#0089a1",
                     cursor='hand2', fg="#ffffff", command=root.destroy)
    sign_up.place(x=215, y=250)

    # --- Botones de módulos ---
    logistica = Button(frame, width=30, text='Ver información de Logística', border=0, bg="#0089a1",
                       cursor='hand2', fg="#ffffff", command=lambda: abrir_sedes(root, nombre_usuario))
    logistica.place(x=215, y=300)

    servicio_cliente = Button(frame, width=30, text='Ver información de Servicio al Cliente', border=0,
                              bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_servicio_cliente(root, nombre_usuario))
    servicio_cliente.place(x=215, y=350)

    marketing = Button(frame, width=30, text='Ver información de Marketing', border=0,
                       bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_marketing(root, nombre_usuario))
    marketing.place(x=215, y=400)

    finanzas = Button(frame, width=30, text='Ver información de Finanzas', border=0,
                      bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_finanzas(root, nombre_usuario))
    finanzas.place(x=215, y=450)

    rrhh = Button(frame, width=30, text='Ver información de RRHH', border=0,
                  bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_rrhh(root, nombre_usuario))
    rrhh.place(x=215, y=500)

    # --- Mensaje de bienvenida ---
    heading = Label(frame, text=f"Bienvenido {nombre_usuario}", fg="white", bg="#1dc1dd",
                    font=("Billie DEMO Light", 23, "bold"))
    heading.place(relx=0.5, rely=0.06, anchor="center")

    root.mainloop()

# --- Inicio del programa ---
if len(sys.argv) > 1:
    usuario = sys.argv[1]
else:
    usuario = "Usuario"

abrir_home(usuario)
