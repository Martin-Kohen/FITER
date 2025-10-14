from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date # Necesario para manejar las fechas de la BD

# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "fiter"
}

# --- Funciones de Lógica (Simplificadas para la Interfaz) ---

def conectar_bd():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        # En la interfaz simple, mostramos el error de inmediato
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {err}")
        return None

def alta_campana(parent_window, frame_resultados):
    """Implementa el flujo: Ingresar datos de campaña -> Guardar en BD."""
    nombre = simpledialog.askstring("Nueva Campaña", "Nombre:", parent=parent_window)
    if not nombre: return
    objetivo = simpledialog.askstring("Nueva Campaña", "Objetivo:", parent=parent_window)
    if not objetivo: return
    fecha_inicio_str = simpledialog.askstring("Nueva Campaña", "Fecha Inicio (YYYY-MM-DD):", parent=parent_window)
    fecha_fin_str = simpledialog.askstring("Nueva Campaña", "Fecha Fin (YYYY-MM-DD):", parent=parent_window)
    
    try:
        fecha_inicio = date.fromisoformat(fecha_inicio_str)
        fecha_fin = date.fromisoformat(fecha_fin_str)
    except (ValueError, TypeError):
        messagebox.showerror("Error de Fecha", "Formato de fecha incorrecto. Usa YYYY-MM-DD.")
        return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO campañas (nombre_campaña, objetivo, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, objetivo, fecha_inicio, fecha_fin))
            conn.commit()
            messagebox.showinfo("Éxito", f"Campaña '{nombre}' registrada.")
            consultar_campanas(frame_resultados) # Actualizar la lista
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al insertar: {err}")
        finally:
            cursor.close()
            conn.close()

def baja_campana(parent_window, frame_resultados):
    """Implementa el flujo: Seleccionar campaña a eliminar -> Eliminar de BD."""
    campana_id = simpledialog.askinteger("Eliminar Campaña", "Ingresa el ID de la campaña a eliminar:", parent=parent_window)
    if campana_id is None: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            confirm = messagebox.askyesno("Confirmar", f"¿Eliminar campaña ID {campana_id}?")
            if confirm:
                sql = "DELETE FROM campañas WHERE id_campaña = %s"
                cursor.execute(sql, (campana_id,))
                if cursor.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Éxito", f"Campaña ID {campana_id} eliminada.")
                    consultar_campanas(frame_resultados) # Actualizar la lista
                else:
                    messagebox.showwarning("Advertencia", f"No se encontró campaña con ID {campana_id}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al eliminar: {err}")
        finally:
            cursor.close()
            conn.close()

def modificar_campana(parent_window, frame_resultados):
    """Implementa el flujo: Seleccionar -> Modificar datos -> Actualizar BD."""
    campana_id = simpledialog.askinteger("Modificar Campaña", "Ingresa el ID de la campaña a modificar:", parent=parent_window)
    if campana_id is None: return

    # Nota: Aquí se podría agregar la lógica para obtener los datos actuales
    # y mostrarlos como initialvalue, como en el código anterior, pero lo
    # simplificamos para la interfaz.
    nuevo_nombre = simpledialog.askstring("Modificar Campaña", f"Nuevo nombre para ID {campana_id}:", parent=parent_window)
    if nuevo_nombre is None: return
    
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "UPDATE campañas SET nombre_campaña = %s WHERE id_campaña = %s"
            cursor.execute(sql, (nuevo_nombre, campana_id))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Campaña ID {campana_id} modificada.")
                consultar_campanas(frame_resultados) # Actualizar la lista
            else:
                messagebox.showwarning("Advertencia", f"No se encontró campaña con ID {campana_id}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al modificar: {err}")
        finally:
            cursor.close()
            conn.close()

def consultar_campanas(frame_resultados):
    """Implementa el flujo: Consultar BD -> Ver lista de campañas."""
    # Limpiar widgets anteriores
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_campaña, nombre_campaña, objetivo, fecha_inicio, fecha_fin FROM campañas")
            campanas = cursor.fetchall()

            Label(frame_resultados, text="Campañas Registradas:", bg="#1dc1dd", fg="white",
                  font=("Arial", 16, "bold")).pack(pady=5)
            
            if campanas:
                for c in campanas:
                    # Mostrar la campaña como un botón simple
                    texto_campana = f"ID: {c[0]} | {c[1]} | {c[3]} a {c[4]}"
                    Button(frame_resultados, text=texto_campana, bg="#ffffff", fg="black", font=("Billie DEMO Light", 12),
                           # Al igual que en tu modelo, un comando simple al hacer clic
                           command=lambda id_c=c[0], nombre_c=c[1]: messagebox.showinfo("Detalles", f"Objetivo de {nombre_c}: {c[2]}")
                           ).pack(fill=X, padx=20, pady=2)
            else:
                Label(frame_resultados, text="No hay campañas registradas.", bg="#1dc1dd", fg="black", font=("Billie DEMO Light", 12)).pack(pady=20)

        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar la BD: {err}")
        finally:
            cursor.close()
            conn.close()

# --- Función Principal de la Ventana de Marketing ---

def abrir_marketing(parent_window, nombre_usuario):
    # Oculta el home temporalmente
    parent_window.withdraw()

    root = Toplevel()
    root.title("Marketing y Ventas")
    root.state("zoomed")
    root.configure(bg="#1dc1dd") # Mantenemos el color de fondo de tu modelo

    # --- Función para volver al home ---
    def volver_home():
        root.destroy()
        parent_window.deiconify()       
        parent_window.state("zoomed")   

    # --- Contenedores ---
    # Frame para el botón Volver y el título
    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)
    
    Button(frame_top, text="← Volver al Home", bg="#ff4d4d", fg="white",
           font=("Billie DEMO Light", 12, "bold"), command=volver_home).pack(pady=5, padx=20, fill=X)
    
    Label(frame_top, text="Gestión de Campañas de Marketing", bg="#1dc1dd", fg="white",
          font=("Billie DEMO Light", 18, "bold")).pack(pady=10)


    # Frame para los botones de acción (Alta, Baja, Modificar, Consultar)
    frame_acciones = Frame(root, bg="#1dc1dd")
    frame_acciones.pack(pady=10, fill=X)

    # Frame para mostrar la lista de campañas (similar a mostrar_tickets)
    frame_resultados = Frame(root, bg="#1dc1dd")
    frame_resultados.pack(pady=10, fill=BOTH, expand=True)

    # --- Botones de Acción de Campañas (Simulando el flujo del diagrama) ---
    
    # 1. Alta (¿Deseas dar de alta una campaña?)
    Button(frame_acciones, text="Dar de Alta Campaña", bg="#0089a1", fg="white",
           font=("Billie DEMO Light", 12, "bold"),
           command=lambda: alta_campana(root, frame_resultados)).pack(side=LEFT, padx=10, expand=True)

    # 2. Baja (¿Deseas dar de baja una campaña?)
    Button(frame_acciones, text="Dar de Baja Campaña", bg="#0089a1", fg="white",
           font=("Billie DEMO Light", 12, "bold"),
           command=lambda: baja_campana(root, frame_resultados)).pack(side=LEFT, padx=10, expand=True)

    # 3. Modificar (¿Deseas modificar una campaña?)
    Button(frame_acciones, text="Modificar Campaña", bg="#0089a1", fg="white",
           font=("Billie DEMO Light", 12, "bold"),
           command=lambda: modificar_campana(root, frame_resultados)).pack(side=LEFT, padx=10, expand=True)
           
    # 4. Consultar/Ver (¿Deseas ver las campañas?)
    Button(frame_acciones, text="Ver/Actualizar Campañas", bg="#0089a1", fg="white",
           font=("Billie DEMO Light", 12, "bold"),
           command=lambda: consultar_campanas(frame_resultados)).pack(side=LEFT, padx=10, expand=True)


    frame_enlaces = Frame(root, bg="#1dc1dd")
    frame_enlaces.pack(pady=10, fill=X)

    # Inicializar la lista de campañas al abrir la ventana
    consultar_campanas(frame_resultados)

    root.mainloop()


# --- Ejemplo de uso (simulando la ventana principal) ---
if __name__ == '__main__':
    main_root = Tk()
    main_root.title("Home")
    main_root.geometry("400x200")
    
    def ejecutar_marketing():
        abrir_marketing(main_root, "Admin")

    Label(main_root, text="Ventana Principal", font=("Arial", 16, "bold")).pack(pady=20)
    Button(main_root, text="Abrir Módulo de Marketing", bg="#1dc1dd", fg="white",
           font=("Arial", 12, "bold"), command=ejecutar_marketing).pack(pady=10)

    main_root.mainloop()