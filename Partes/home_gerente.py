from tkinter import *
import sys
import subprocess
from sedes import abrir_sedes
from servicio_cliente import abrir_servicio_cliente  
from marketing import abrir_marketing
from finanzas import abrir_finanzas
from rrhh import abrir_rrhh
from functools import partial

def abrir_home_deslog(root):
    """
    Cierra la ventana actual (root) y lanza home_deslog.py en un nuevo proceso.
    """
    if root is None:
        # Mensaje de debug si se llama mal la función
        print("ERROR: abrir_home_deslog fue llamado sin pasar la ventana 'root'.")
        return

    # Cierra la ventana actual
    try:
        root.destroy()
    except Exception as e:
        print("No se pudo destruir la ventana root:", e)

    # Abre el script de la pantalla no logueada
    subprocess.Popen(["python", "home_deslog.py"])


def abrir_home(nombre_usuario):
    # Crear ventana principal
    root = Tk()
    root.title("Home")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)

    # --- Botón de Cerrar Sesión ---
    # Opción A: usando lambda (muy común)
    sign_up = Button(frame, width=25, height=1, text='Cerrar Sesión', border=0, bg="#0089a1",
                     cursor='hand2', fg="#ffffff",
                     command=lambda r=root: abrir_home_deslog(r),
                     font=('Billie DEMO Light', 11, 'bold'))
    sign_up.place(x=1600, y=55)

    # Opción B: usando functools.partial (equivalente)
    # sign_up = Button(frame, width=25, height=1, text='Cerrar Sesión', border=0, bg="#0089a1",
    #                  cursor='hand2', fg="#ffffff",
    #                  command=partial(abrir_home_deslog, root),
    #                  font=('Billie DEMO Light', 11, 'bold'))
    # sign_up.place(x=1600, y=55)

    # --- Botones de módulos ---
    logistica = Button(frame, width=30, text='Ver información de Logística', border=0, bg="#0089a1",
                       cursor='hand2', fg="#ffffff", command=lambda: abrir_sedes(root, nombre_usuario), font=('Billie DEMO Light', 11, 'bold'))
    logistica.place(x=215, y=300)

    servicio_cliente = Button(frame, width=30, text='Ver información de Servicio al Cliente', border=0,
                              bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_servicio_cliente(root, nombre_usuario), font=('Billie DEMO Light', 11, 'bold'))
    servicio_cliente.place(x=515, y=300)

    marketing = Button(frame, width=30, text='Ver información de Marketing', border=0,
                       bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_marketing(root, nombre_usuario), font=('Billie DEMO Light', 11, 'bold'))
    marketing.place(x=815, y=300)

    finanzas = Button(frame, width=30, text='Ver información de Finanzas', border=0,
                      bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_finanzas(root, nombre_usuario), font=('Billie DEMO Light', 11, 'bold'))
    finanzas.place(x=1115, y=300)

    rrhh = Button(frame, width=30, text='Ver información de RRHH', border=0,
                  bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_rrhh(root, nombre_usuario), font=('Billie DEMO Light', 11, 'bold'))
    rrhh.place(x=1415, y=300)

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
