from tkinter import *
from tkinter import messagebox
import mysql.connector

# Función para abrir la ventana de sedes
def abrir_sedes(parent_window, nombre_usuario):
    # Oculta el home temporalmente
    parent_window.withdraw()

    root = Toplevel()  # Nueva ventana encima del home
    root.title("Sedes y Máquinas")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    # --- Contenedores ---
    frame_sedes = Frame(root, bg="#1dc1dd")
    frame_sedes.pack(pady=10, fill=X)

    frame_maquinas = Frame(root, bg="#1dc1dd")
    frame_maquinas.pack(pady=10, fill=BOTH, expand=True)

    # --- Función para volver al home ---
    def volver_home():
        root.destroy()
        parent_window.deiconify()       # Muestra nuevamente el home
        parent_window.state("zoomed")   # Asegura que ocupe toda la pantalla
  # Muestra nuevamente el home

    Button(frame_sedes, text="← Volver al Home", bg="#ff4d4d", fg="white",
           font=("Arial", 12, "bold"), command=volver_home).pack(pady=5, padx=20, fill=X)

    # --- Conectar y mostrar sedes ---
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
            Label(frame_sedes, text="Sedes disponibles:", bg="#1dc1dd", fg="white",
                  font=("Arial", 16, "bold")).pack(pady=5)

            for sede in sedes:
                Button(frame_sedes, text=f"{sede[1]}", bg="#ffffff", fg="black", font=("Arial", 12),
                       command=lambda id_s=sede[0], nombre_s=sede[1]: mostrar_maquinas(id_s, nombre_s, frame_maquinas)).pack(fill=X, padx=20, pady=2)
        else:
            Label(frame_sedes, text="No hay sedes registradas", bg="#1dc1dd", fg="black", font=("Arial", 12)).pack(pady=20)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")

    root.mainloop()


# --- Función para mostrar máquinas de una sede ---
def mostrar_maquinas(id_sede, nombre_sede, frame_maquinas):
    # Limpiar widgets anteriores
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
            Label(frame_maquinas, text=f"Máquinas de la sede {nombre_sede}:", bg="#1dc1dd",
                  fg="white", font=("Arial", 14, "bold")).pack(pady=5)

            for maq in maquinas:
                frame_maquina = Frame(frame_maquinas, bg="#1dc1dd")
                frame_maquina.pack(fill=X, pady=2, padx=20)

                Label(frame_maquina, text=f"{maq[1]} (Estado: {maq[2]})", bg="#1dc1dd",
                      fg="black", font=("Arial", 12)).pack(side=LEFT)

                # Botón para cambiar estado
                if maq[2].lower() == "activo":
                    btn_text = "Dar de baja"
                    nuevo_estado = "Inactivo"
                else:
                    btn_text = "Dar de alta"
                    nuevo_estado = "Activo"

                Button(frame_maquina, text=btn_text, bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                       command=lambda id_m=maq[0], nuevo=nuevo_estado: cambiar_estado(id_m, nuevo, id_sede, nombre_sede, frame_maquinas)).pack(side=LEFT, padx=10)

        else:
            Label(frame_maquinas, text="No hay máquinas en esta sede", bg="#1dc1dd", fg="black", font=("Arial", 12)).pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")


# --- Función para cambiar estado de la máquina ---
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
        mostrar_maquinas(id_sede, nombre_sede, frame_maquinas)  # Recargar lista
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo actualizar el estado: {err}")
