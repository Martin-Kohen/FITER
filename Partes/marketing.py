from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date
import subprocess
import sys

# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "fiter"
}

# --- Funciones Generales ---

def conectar_bd():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {err}")
        return None

def mostrar_ventana_detalle_campanas(lista_campanas):
    ventana = Toplevel()
    ventana.title("Detalle de Campañas")
    ventana.state("zoomed")
    ventana.configure(bg="#1dc1dd")

    Label(ventana, text="Detalle Completo de Campañas",
          bg="#1dc1dd", fg="white",
          font=("Arial", 20, "bold")).pack(pady=20)

    frame_detalle = Frame(ventana, bg="#1dc1dd")
    frame_detalle.pack(pady=10, fill=BOTH, expand=True)

    # Encabezado
    Label(frame_detalle, text="ID    |    Nombre    |    Objetivo    |    Inicio    |    Fin",
          bg="#ffffff", fg="black",
          font=("Arial", 14, "bold"),
          justify="left").pack(fill=X, padx=20, pady=10)

    # Cada campaña en la nueva ventana
    for c in lista_campanas:
        id_camp = c[0]
        nombre = c[1]
        objetivo = c[2]
        f_inicio = c[3]
        f_fin = c[4]

        texto = (
            f"ID: {id_camp}   |   {nombre}\n"
            f"Objetivo: {objetivo}\n"
            f"Desde: {f_inicio}   Hasta: {f_fin}"
        )

        Label(frame_detalle, text=texto,
              bg="#ffffff", fg="black",
              font=("Arial", 12), anchor="w",
              justify="left").pack(fill=X, padx=20, pady=10)

def volver_home_gerente(root, parent_window, nombre_usuario, rol):
    root.destroy()
    subprocess.Popen([sys.executable, "Partes/home_gerente.py", nombre_usuario, rol])


def cerrar_sesion_marketing(root):
    root.destroy()
    subprocess.Popen([sys.executable, "Partes/home_deslog.py"])


def alta_campana(parent_window, frame_resultados):
    nombre = simpledialog.askstring("Nueva Campaña", "Nombre:", parent=parent_window)
    if not nombre: return

    objetivo = simpledialog.askstring("Nueva Campaña", "Objetivo:", parent=parent_window)
    if not objetivo: return

    fecha_inicio_str = simpledialog.askstring("Nueva Campaña", "Fecha Inicio (YYYY-MM-DD):", parent=parent_window)
    fecha_fin_str = simpledialog.askstring("Nueva Campaña", "Fecha Fin (YYYY-MM-DD):", parent=parent_window)

    try:
        fecha_inicio = date.fromisoformat(fecha_inicio_str)
        fecha_fin = date.fromisoformat(fecha_fin_str)
    except:
        messagebox.showerror("Error de Fecha", "Formato incorrecto. Usa YYYY-MM-DD.")
        return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO campañas (nombre_campaña, objetivo, fecha_inicio, fecha_fin) VALUES (%s,%s,%s,%s)",
                (nombre, objetivo, fecha_inicio, fecha_fin)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Campaña '{nombre}' registrada.")
            consultar_campanas(frame_resultados)
        except mysql.connector.Error as err:
            messagebox.showerror("Error BD", str(err))
        finally:
            cursor.close()
            conn.close()


def baja_campana(parent_window, frame_resultados):
    campana_id = simpledialog.askinteger("Eliminar Campaña", "ID a eliminar:", parent=parent_window)
    if campana_id is None: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            confirm = messagebox.askyesno("Confirmar", f"¿Eliminar campaña ID {campana_id}?")
            if confirm:
                cursor.execute("DELETE FROM campañas WHERE id_campaña = %s", (campana_id,))
                if cursor.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Éxito", "Campaña eliminada.")
                    consultar_campanas(frame_resultados)
                else:
                    messagebox.showwarning("No encontrada", "No existe ese ID.")
        except:
            messagebox.showerror("Error BD", "No se pudo eliminar.")
        finally:
            cursor.close()
            conn.close()


def modificar_campana(parent_window, frame_resultados):
    campana_id = simpledialog.askinteger("Modificar Campaña", "ID a modificar:", parent=parent_window)
    if campana_id is None: return

    nuevo_nombre = simpledialog.askstring("Modificar Campaña", "Nuevo nombre:", parent=parent_window)
    if not nuevo_nombre: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE campañas SET nombre_campaña=%s WHERE id_campaña=%s", (nuevo_nombre, campana_id))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", "Campaña modificada.")
                consultar_campanas(frame_resultados)
            else:
                messagebox.showwarning("No encontrada", "No existe ese ID.")
        except:
            messagebox.showerror("Error BD", "No se pudo modificar.")
        finally:
            cursor.close()
            conn.close()



def consultar_campanas(frame_resultados):
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    conn = conectar_bd()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id_campaña, nombre_campaña, objetivo, fecha_inicio, fecha_fin FROM campañas")
    campanas = cursor.fetchall()
    conn.close()

    Label(frame_resultados, text="Campañas Registradas",
          bg="#1dc1dd", fg="white",
          font=("Arial", 16, "bold")).pack(pady=5)

    if not campanas:
        Label(frame_resultados, text="No hay campañas.",
              bg="#1dc1dd", fg="black", font=("Arial", 12)).pack(pady=20)
        return

    Button(frame_resultados, text="🔍 Ver Detalles Completos",
           bg="#0089a1", fg="white",
           font=("Arial", 14, "bold"),
           command=lambda: mostrar_ventana_detalle_campanas(campanas)
           ).pack(pady=10)

    for c in campanas:
        Button(frame_resultados,
               text=f"ID {c[0]} | {c[1]} | {c[3]} → {c[4]}",
               bg="#ffffff", fg="black",
               font=("Arial", 12),
               command=lambda lista=campanas: mostrar_ventana_detalle_campanas(lista)
               ).pack(fill=X, padx=20, pady=2)

def abrir_marketing(parent_window, nombre_usuario, rol):
    parent_window.withdraw()

    root = Toplevel()
    root.title("Marketing y Ventas")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)

    if rol == "Gerente":
        Button(
            frame_top,
            text="← Volver al Home",
            bg="#0089a1", fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: volver_home_gerente(root, parent_window, nombre_usuario, rol)
        ).pack(pady=5, padx=20, fill=X)
    else:
        Button(
            frame_top,
            text="❌ Cerrar Sesión",
            bg="#ff4d4d", fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: cerrar_sesion_marketing(root)
        ).pack(pady=5, padx=20, fill=X)

    Label(frame_top, text="Gestión de Campañas de Marketing",
          bg="#1dc1dd", fg="white", font=("Arial", 18, "bold")).pack(pady=10)

    frame_acciones = Frame(root, bg="#1dc1dd")
    frame_acciones.pack(pady=10, fill=X)

    frame_resultados = Frame(root, bg="#1dc1dd")
    frame_resultados.pack(pady=10, fill=BOTH, expand=True)

    Button(frame_acciones, text="Alta Campaña", bg="#0089a1", fg="white",
           font=("Arial", 12, "bold"),
           command=lambda: alta_campana(root, frame_resultados)).pack(side=LEFT, padx=10)

    Button(frame_acciones, text="Baja Campaña", bg="#0089a1", fg="white",
           font=("Arial", 12, "bold"),
           command=lambda: baja_campana(root, frame_resultados)).pack(side=LEFT, padx=10)

    Button(frame_acciones, text="Modificar Campaña", bg="#0089a1", fg="white",
           font=("Arial", 12, "bold"),
           command=lambda: modificar_campana(root, frame_resultados)).pack(side=LEFT, padx=10)


    consultar_campanas(frame_resultados)
    root.mainloop()



if __name__ == '__main__':
    main_root = Tk()
    nombre_usuario = "Test"
    rol = "Empleado"

    main_root.withdraw()
    abrir_marketing(main_root, nombre_usuario, rol)
    main_root.mainloop()
