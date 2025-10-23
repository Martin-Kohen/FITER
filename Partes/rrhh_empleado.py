from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date
import subprocess # Importación necesaria para ejecutar otro script

# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "", # Asegúrate de que esta sea tu contraseña, si tienes una.
    "database": "fiter"
}

# --- Variables Globales para Control de Ventanas Toplevel Únicas ---
lista_empleados_window = None 
lista_candidatos_window = None

def conectar_bd():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {err}")
        return None

# ----------------- GESTIÓN DE EMPLEADOS -----------------

def alta_empleado(parent_window):
    """
    Flujo: Da de alta un empleado sin solicitar el ID, 
    permitiendo que la BD lo auto-incremente.
    """
    nombre = simpledialog.askstring("Alta Empleado", "Nombre:", parent=parent_window)
    if not nombre: return

    apellido = simpledialog.askstring("Alta Empleado", "Apellido:", parent=parent_window)
    if not apellido: return
    
    puesto = simpledialog.askstring("Alta Empleado", "Puesto:", parent=parent_window)
    if not puesto: return
    
    fecha_contratacion_str = simpledialog.askstring("Alta Empleado", "Fecha Contratación (YYYY-MM-DD):", parent=parent_window)
    try:
        fecha_contratacion = date.fromisoformat(fecha_contratacion_str)
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Formato de fecha incorrecto (debe ser YYYY-MM-DD).")
        return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Empleados_RRHH (Nombre, Apellido, Puesto, Fecha_Contratacion) 
                     VALUES (%s, %s, %s, %s)"""
            
            cursor.execute(sql, (nombre, apellido, puesto, fecha_contratacion))
            conn.commit()
            
            nuevo_id = cursor.lastrowid
            messagebox.showinfo("Éxito", f"Empleado {nombre} {apellido} registrado con éxito.\nID Generado: {nuevo_id}")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al insertar el empleado: {err}")
        finally:
            cursor.close()
            conn.close()


def baja_empleado(parent_window):
    """Flujo: ¿Desea dar de baja un empleado? -> Seleccionar empleado -> Actualizar BD"""
    id_a_borrar = simpledialog.askinteger("Baja Empleado", "Ingresa el ID del empleado a dar de baja:", parent=parent_window)
    if id_a_borrar is None: return

    confirm = messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de dar de BAJA al empleado con ID {id_a_borrar}?", icon='warning')
    if not confirm: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM Empleados_RRHH WHERE ID_Empleado = %s"
            cursor.execute(sql, (id_a_borrar,))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Empleado con ID {id_a_borrar} dado de baja (eliminado).")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró empleado con ID {id_a_borrar}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al dar de baja: {err}")
        finally:
            cursor.close()
            conn.close()

def modificar_empleado(parent_window):
    """Flujo: ¿Desea modificar datos? -> Seleccionar -> Modificar información"""
    id_modificar = simpledialog.askinteger("Modificar Empleado", "Ingresa el ID del empleado a modificar:", parent=parent_window)
    if id_modificar is None: return

    nuevo_puesto = simpledialog.askstring("Modificar Empleado", f"Nuevo Puesto para ID {id_modificar}:", parent=parent_window)
    if not nuevo_puesto: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "UPDATE Empleados_RRHH SET Puesto = %s WHERE ID_Empleado = %s"
            cursor.execute(sql, (nuevo_puesto, id_modificar))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Puesto del empleado ID {id_modificar} actualizado a '{nuevo_puesto}'.")
            else:
                messagebox.showwarning("Advertencia", f"No se encontró empleado con ID {id_modificar}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al modificar: {err}")
        finally:
            cursor.close()
            conn.close()

def ver_lista_empleados():
    """Flujo: Consulta BD y Muestra la lista de empleados en una ventana Toplevel ÚNICA."""
    global lista_empleados_window
    
    if lista_empleados_window and lista_empleados_window.winfo_exists():
        lista_empleados_window.lift()
        return

    top = Toplevel()
    lista_empleados_window = top
    top.title("Lista de Empleados")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")
    
    def on_close():
        global lista_empleados_window
        lista_empleados_window = None
        top.destroy()
        
    top.protocol("WM_DELETE_WINDOW", on_close)

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_Empleado, Nombre, Apellido, Puesto, Fecha_Contratacion FROM Empleados_RRHH")
            empleados = cursor.fetchall()
            
            header = "ID | Nombre | Apellido | Puesto | Contratación"
            Label(top, text=header, bg="#ffffff", fg="#000000", font=("Arial", 12, "bold")).pack(fill=X, padx=10, pady=5)

            if empleados:
                for emp in empleados:
                    fecha_contratacion = emp[4].strftime("%Y-%m-%d") if isinstance(emp[4], date) else str(emp[4])
                    emp_str = f"{emp[0]} | {emp[1]} | {emp[2]} | {emp[3]} | {fecha_contratacion}"
                    Label(top, text=emp_str, bg="#f0f0ff", fg="black",
                          font=("Arial", 10), anchor="w").pack(fill=X, padx=10, pady=1)
            else:
                Label(top, text="No hay empleados registrados.", bg="#ffffff", fg="black", font=("Arial", 12)).pack(padx=10, pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar empleados: {err}")
        finally:
            cursor.close()
            conn.close()

# ----------------- RECLUTAMIENTO -----------------

def ver_posibles_candidatos():
    """Flujo: Muestra la lista de procesos de reclutamiento en una ventana Toplevel ÚNICA."""
    global lista_candidatos_window
    
    if lista_candidatos_window and lista_candidatos_window.winfo_exists():
        lista_candidatos_window.lift()
        return
        
    top = Toplevel()
    lista_candidatos_window = top
    top.title("Procesos de Reclutamiento (Candidatos)")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")

    def on_close():
        global lista_candidatos_window
        lista_candidatos_window = None
        top.destroy()
        
    top.protocol("WM_DELETE_WINDOW", on_close)

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql_reclutamiento = "SELECT ID_Reclutamiento, Descripcion_Puesto, Salario_Ofrecido, Estado_Proceso FROM Reclutamiento WHERE Estado_Proceso != 'Cerrado'"
            cursor.execute(sql_reclutamiento)
            procesos = cursor.fetchall()

            header = "ID | Puesto | Salario Ofrecido | Estado"
            Label(top, text=header, bg="#ffffff", fg="#000000", font=("Arial", 12, "bold")).pack(fill=X, padx=10, pady=5)

            if procesos:
                for proc in procesos:
                    salario_formateado = f"${proc[2]:,.2f}" if proc[2] is not None else "N/A"
                    proc_str = f"{proc[0]} | {proc[1][:30]}... | {salario_formateado} | {proc[3]}"
                    Label(top, text=proc_str, bg="#f0f0ff", fg="black",
                          font=("Arial", 10), anchor="w").pack(fill=X, padx=10, pady=1)
            else:
                Label(top, text="No hay procesos de reclutamiento abiertos.", bg="#ffffff", fg="black", font=("Arial", 12)).pack(padx=10, pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar reclutamiento: {err}")
        finally:
            cursor.close()
            conn.close()

# ----------------- CONEXIÓN FINANZAS (SIMULACIÓN) -----------------

def actualizar_maestros():
    """Simulación del botón de Finanzas que actualiza los maestros de RR.HH."""
    messagebox.showinfo("Actualizar Maestros",
                          "RR.HH. es el origen de los datos. La lista de Empleados está actualizada.\n"
                          "Si el módulo de Finanzas necesita la lista, debe consultarla aquí.")


# --- Función Principal de la Ventana de RR.HH. ---

def abrir_rrhh(parent_window, nombre_usuario):
    
    root = Toplevel()
    root.title(f"Recursos Humanos - Usuario: {nombre_usuario}")
    root.state("zoomed")
    root.configure(bg="#1dc1dd") # Fondo Turquesa
    
    # Ocultamos la ventana principal para que no sea visible si se estaba mostrando.
    parent_window.withdraw()

    # --- Función para Cerrar Sesión y ABRIR home_empleado.py ---
    def cerrar_sesion():
        # Limpiar ventanas flotantes
        global lista_empleados_window, lista_candidatos_window
        if lista_empleados_window and lista_empleados_window.winfo_exists():
            lista_empleados_window.destroy()
        if lista_candidatos_window and lista_candidatos_window.winfo_exists():
            lista_candidatos_window.destroy()
            
        root.destroy()
        # 1. Cierra la aplicación actual de Tkinter (este script).
        parent_window.quit() 
        
        # 2. Lanza el Home (home_empleado.py) como un nuevo proceso.
        try:
            # Usamos subprocess.Popen para que el nuevo script se ejecute de forma independiente
            subprocess.Popen(["python", "home_deslog.py"]) 
        except FileNotFoundError:
            # Manejo de error si python no está en el PATH o el archivo no se encuentra
            messagebox.showerror("Error de Inicio", "Asegúrate de que 'home_deslog.py' exista y Python esté en el PATH.")
        
    # Asignamos la función de cerrar sesión al botón 'X' de la ventana de RR.HH. también
    root.protocol("WM_DELETE_WINDOW", cerrar_sesion)


    # --- Contenedores ---
    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)
    
    # Botón 'Cerrar Sesión'
    Button(frame_top, text="❌ Cerrar Sesión", bg="#ff4d4d", fg="white",
           font=("Arial", 12, "bold"), command=cerrar_sesion).pack(pady=5, padx=20, fill=X)
    
    # ... (Resto de la interfaz de RR.HH. se mantiene igual) ...
    
    Label(frame_top, text="Módulo de Recursos Humanos (RR.HH.)", bg="#1dc1dd", fg="white",
          font=("Arial", 18, "bold")).pack(pady=10)

    # Frame para AGRUPAR TODAS las acciones
    frame_acciones = Frame(root, bg="#1dc1dd")
    frame_acciones.pack(pady=20, fill=X)
    
    # --- Fila 1: Gestión de Empleados ---
    frame_empleados = Frame(frame_acciones, bg="#1dc1dd")
    frame_empleados.pack(pady=5)
    Label(frame_empleados, text="Gestión de Empleados", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_emp = Frame(frame_empleados, bg="#1dc1dd")
    frame_botones_emp.pack()

    Button(frame_botones_emp, text="Dar de Alta", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: alta_empleado(root)).pack(side=LEFT, padx=5)

    Button(frame_botones_emp, text="Dar de Baja", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: baja_empleado(root)).pack(side=LEFT, padx=5)

    Button(frame_botones_emp, text="Modificar Datos", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: modificar_empleado(root)).pack(side=LEFT, padx=5)

    Button(frame_botones_emp, text="Ver Empleados", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=ver_lista_empleados).pack(side=LEFT, padx=5)
    
    # --- Fila 2: Reclutamiento y Conexión ---
    frame_reclutamiento = Frame(frame_acciones, bg="#1dc1dd")
    frame_reclutamiento.pack(pady=5)
    Label(frame_reclutamiento, text="Reclutamiento y Conexión de Datos", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_rec = Frame(frame_reclutamiento, bg="#1dc1dd")
    frame_botones_rec.pack()

    Button(frame_botones_rec, text="Ver Candidatos", bg="#006779", fg="white", font=("Arial", 12, "bold"),
           width=25, command=ver_posibles_candidatos).pack(side=LEFT, padx=10)
    
    Button(frame_botones_rec, text="Actualizar Maestros (Finanzas)", bg="#006779", fg="white", font=("Arial", 12, "bold"),
           width=25, command=actualizar_maestros).pack(side=LEFT, padx=10)


    root.mainloop()

# ----------------- INICIO DEL PROGRAMA (ELIMINA LA VENTANA INICIAL) -----------------
if __name__ == '__main__':
    # Creamos la ventana principal (Root) de Tkinter. Es esencial para el mainloop.
    main_root = Tk()
    main_root.withdraw() # La ocultamos
    main_root.title("Ventana Raíz Oculta")
    
    # Iniciamos el módulo de RR.HH.
    abrir_rrhh(main_root, "Gerente RRHH")
    
    # El mainloop se mantiene hasta que cerrar_sesion lo termine.
    main_root.mainloop()