from tkinter import *
import sys
import subprocess
from functools import partial
# Si estas importaciones dan error, coméntalas y usa subprocess.Popen en los botones.
from sedes import abrir_sedes
from marketing import abrir_marketing
from finanzas import abrir_finanzas
from rrhh_empleado import abrir_rrhh # Esta función ahora requiere 3 argumentos

def abrir_home_deslog(root):
    """
    Cierra la ventana actual (root) y lanza home_deslog.py en un nuevo proceso.
    """
    if root is None:
        print("ERROR: abrir_home_deslog fue llamado sin pasar la ventana 'root'.")
        return
    try:
        root.destroy()
    except Exception as e:
        print("No se pudo destruir la ventana root:", e)
    # Usar sys.executable en lugar de "python" es más seguro
    subprocess.Popen([sys.executable, "home_deslog.py"])


# ----------------------------------------------------------------------------------
# 1. CORRECCIÓN: Se agrega el argumento 'rol' a la función
# ----------------------------------------------------------------------------------
def abrir_home(nombre_usuario, rol):
    # Crear ventana principal
    root = Tk()
    root.title("Home Gerente")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame = Frame(root, bg="#1dc1dd")
    frame.pack(fill="both", expand=True)

    # --- Mensaje de bienvenida (centrado con relx/rely) ---
    heading = Label(frame, text=f"Bienvenido {nombre_usuario} (Rol: {rol})", fg="white", bg="#1dc1dd",
                    font=("Billie DEMO Light", 23, "bold"))
    heading.place(relx=0.5, rely=0.06, anchor="center")
    
    # --- Botón de Cerrar Sesión (Colocado en la esquina superior derecha) ---
    sign_up = Button(frame, width=25, height=1, text='Cerrar Sesión', border=0, bg="#0089a1",
                     cursor='hand2', fg="#ffffff",
                     command=lambda r=root: abrir_home_deslog(r),
                     font=('Billie DEMO Light', 11, 'bold'))
    sign_up.place(relx=0.98, rely=0.05, anchor="ne") 


    # --- Nuevo Frame para los Botones de Módulos (para centrado horizontal) ---
    frame_botones_modulos = Frame(frame, bg="#1dc1dd")
    # ✅ Centrado horizontal y movimiento hacia abajo
    frame_botones_modulos.pack(pady=250, anchor='center') 

    # --- Botones de módulos (usando pack con side=LEFT para ponerlos en fila) ---
    padx_btn = 10 # Espacio entre botones
    width_btn = 30 # Ancho de los botones
    height_btn = 2 # Altura de los botones
    btn_font = ('Billie DEMO Light', 11, 'bold')

    # 1. Logística (sedes.py)
    # NOTA: Los demás botones también pueden requerir el rol si abren scripts actualizados
    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de Logística', border=0, bg="#0089a1",
           cursor='hand2', fg="#ffffff", command=lambda: abrir_sedes(root, nombre_usuario), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)
            
    # 2. Marketing
    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de Marketing', border=0,
           bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_marketing(root, nombre_usuario), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)

    # 3. Finanzas
    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de Finanzas', border=0,
           bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_finanzas(root, nombre_usuario), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)

    # ----------------------------------------------------------------------------------
    # 2. CORRECCIÓN: Se pasa el rol 'rol' como tercer argumento
    # ----------------------------------------------------------------------------------
    # 4. RRHH
    Button(frame_botones_modulos, width=width_btn, height=height_btn, text='Ver información de RRHH', border=0,
           bg="#0089a1", cursor='hand2', fg="#ffffff", command=lambda: abrir_rrhh(root, nombre_usuario, rol), 
           font=btn_font).pack(side=LEFT, padx=padx_btn)
            
    # ❌ ELIMINADO: Botón de Servicio al Cliente

    root.mainloop()


# --- Inicio del programa ---
# ----------------------------------------------------------------------------------
# 3. CORRECCIÓN: Se captura el rol (sys.argv[2])
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) > 2:
        usuario = sys.argv[1] # Primer argumento: Nombre
        rol = sys.argv[2]     # Segundo argumento: Rol
    else:
        # Valores por defecto para ejecución manual
        usuario = "Gerente de Prueba"
        rol = "Gerente"
    
    abrir_home(usuario, rol) # Se llama con los dos argumentos