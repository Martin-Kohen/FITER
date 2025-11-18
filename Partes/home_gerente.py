from tkinter import *
import sys
import subprocess
from functools import partial
from sedes import abrir_sedes
from marketing import abrir_marketing
from finanzas import abrir_finanzas
from rrhh_empleado import abrir_rrhh 

def abrir_home_deslog(root):
    if root is None:
        print("ERROR: abrir_home_deslog fue llamado sin pasar la ventana 'root'.")
        return
    try:
        root.destroy()
    except Exception as e:
        print("No se pudo destruir la ventana root:", e)
    subprocess.Popen([sys.executable, "Partes/home_deslog.py"])

def abrir_home(nombre_usuario, rol):
    # Crear ventana principal
    root = Tk()
    root.title("Home Gerente")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)

    heading = Label(frame, text=f"Bienvenido {nombre_usuario}", fg="white", bg="#1dc1dd",
                    font=("Billie DEMO Light", 23, "bold"))
    heading.place(relx=0.5, rely=0.06, anchor="center")
    
    sign_up = Button(frame, width=25, height=1, text='Cerrar Sesión', border=0, bg="#0089a1",
                     cursor='hand2', fg="#ffffff",
                     command=lambda r=root: abrir_home_deslog(r),
                     font=('Billie DEMO Light', 11, 'bold'))
    sign_up.place(relx=0.98, rely=0.05, anchor="ne") 


    frame_botones_modulos = Frame(frame, bg="#1dc1dd")
    frame_botones_modulos.pack(pady=250, anchor='center') 

    padx_btn = 10 
    width_btn = 30 
    height_btn = 2 
    btn_font = ('Billie DEMO Light', 11, 'bold')

    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de Logística', border=0, bg="#0089a1",
           cursor='hand2', fg="#ffffff", command=lambda: abrir_sedes(root, nombre_usuario, rol), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)
            
    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de Marketing', border=0,
           bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_marketing(root, nombre_usuario, rol), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)

    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de Finanzas', border=0,
           bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_finanzas(root, nombre_usuario, rol), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)

    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de RRHH', border=0,
           bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_rrhh(root, nombre_usuario, rol), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)
            
    root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        usuario = sys.argv[1] 
        rol = sys.argv[2]     
    else:
        usuario = "Gerente de Prueba"
        rol = "Gerente"
    
    abrir_home(usuario, rol) 