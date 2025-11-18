from tkinter import *
from tkinter import messagebox
import mysql.connector
import sys
import subprocess


def volver_home_gerente(root, parent_window, nombre_usuario, rol):
    """Regresa al home del gerente sin cerrar sesión."""
    root.destroy()
    subprocess.Popen([sys.executable, "Partes/home_gerente.py", nombre_usuario, rol])



def cerrar_sesion_sedes(root):
    """Cierra sesión y vuelve al login."""
    root.destroy()
    subprocess.Popen([sys.executable, "Partes/home_deslog.py"])

def abrir_sedes(parent_window, nombre_usuario, rol):
    parent_window.withdraw()

    root = Toplevel()
    root.title("Sedes y Máquinas")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame_sedes = Frame(root, bg="#1dc1dd")
    frame_sedes.pack(pady=10, fill=X)

    frame_maquinas = Frame(root, bg="#1dc1dd")
    frame_maquinas.pack(pady=10, fill=BOTH, expand=True)

    if rol == "Gerente":
        Button(
            frame_sedes,
            text="← Volver al Home",
            bg="#0089a1",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: volver_home_gerente(root, parent_window, nombre_usuario, rol)
        ).pack(pady=5, padx=20, fill=X)
    else:
        Button(
            frame_sedes,
            text="❌ Cerrar Sesión",
            bg="#ff4d4d",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: cerrar_sesion_sedes(root)
        ).pack(pady=5, padx=20, fill=X)


    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT idSedes, Nombre FROM sedes")
        sedes = cursor.fetchall()
        conn.close()

        if sedes:
            Label(frame_sedes, text="Sedes disponibles:",
                  bg="#1dc1dd", fg="white", font=("Arial", 16, "bold")).pack(pady=5)

            for sede in sedes:
                Button(
                    frame_sedes,
                    text=f"{sede[1]}",
                    bg="#ffffff",
                    fg="black",
                    font=("Arial", 12),
                    command=lambda id_s=sede[0], nombre_s=sede[1]: mostrar_maquinas(id_s, nombre_s, frame_maquinas)
                ).pack(fill=X, padx=20, pady=2)
        else:
            Label(frame_sedes, text="No hay sedes registradas",
                  bg="#1dc1dd", fg="black", font=("Arial", 12)).pack(pady=20)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")

    root.mainloop()

def mostrar_maquinas(id_sede, nombre_sede, frame_maquinas):
    for widget in frame_maquinas.winfo_children():
        widget.destroy()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT idMaquinas, Nombre, Estado FROM maquinas WHERE idSede = %s", (id_sede,))
        maquinas = cursor.fetchall()
        conn.close()

        if maquinas:
            Label(
                frame_maquinas,
                text=f"Máquinas de la sede {nombre_sede}:",
                bg="#1dc1dd",
                fg="white",
                font=("Arial", 14, "bold")
            ).pack(pady=5)

            for maq in maquinas:
                frame_maquina = Frame(frame_maquinas, bg="#1dc1dd")
                frame_maquina.pack(fill=X, pady=2, padx=20)

                Label(
                    frame_maquina,
                    text=f"{maq[1]} (Estado: {maq[2]})",
                    bg="#1dc1dd",
                    fg="black",
                    font=("Arial", 12)
                ).pack(side=LEFT)

                if maq[2].lower() == "activo":
                    btn_text = "Dar de baja"
                    nuevo_estado = "Inactivo"
                else:
                    btn_text = "Dar de alta"
                    nuevo_estado = "Activo"

                Button(
                    frame_maquina,
                    text=btn_text,
                    bg="#28a745",
                    fg="white",
                    font=("Arial", 10, "bold"),
                    command=lambda id_m=maq[0], nuevo=nuevo_estado: cambiar_estado(id_m, nuevo, id_sede, nombre_sede, frame_maquinas)
                ).pack(side=LEFT, padx=10)

        else:
            Label(frame_maquinas, text="No hay máquinas en esta sede",
                  bg="#1dc1dd", fg="black", font=("Arial", 12)).pack(pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")

def cambiar_estado(id_maquina, nuevo_estado, id_sede, nombre_sede, frame_maquinas):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE maquinas SET Estado = %s WHERE idMaquinas = %s", (nuevo_estado, id_maquina))
        conn.commit()
        conn.close()

        mostrar_maquinas(id_sede, nombre_sede, frame_maquinas)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo actualizar el estado: {err}")

if __name__ == "__main__":
    main_root = Tk()
    main_root.title("Simulación de Home Oculto")

    if len(sys.argv) > 2:
        nombre_usuario = sys.argv[1]
        rol = sys.argv[2]
    else:
        nombre_usuario = "Test"
        rol = "Empleado" 

    main_root.withdraw()
    abrir_sedes(main_root, nombre_usuario, rol)
    main_root.mainloop()
