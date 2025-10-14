from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date

# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "", # Asegúrate de que esta sea tu contraseña, si tienes una.
    "database": "fiter"
}

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
    # 1. Solicitar Datos (YA NO SE PIDE ID_Empleado)
    
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

    # 2. Guardar en BD (Empleados_RRHH)
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # SQL CORREGIDO: OMITE ID_Empleado de la lista de columnas
            sql = """INSERT INTO Empleados_RRHH (Nombre, Apellido, Puesto, Fecha_Contratacion) 
                     VALUES (%s, %s, %s, %s)"""
            
            # VALORES CORREGIDOS: OMITE el valor de ID_Empleado
            cursor.execute(sql, (nombre, apellido, puesto, fecha_contratacion))
            conn.commit()
            
            # Opcional: Obtener y mostrar el ID generado
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

    # Se podría modificar más campos, aquí solo se pide el puesto como ejemplo.
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
    """Flujo: ¿Desea ver los empleados? -> Consultar BD -> Ver lista de empleados"""
    top = Toplevel()
    top.title("Lista de Empleados")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")

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
                    # Formatear la fecha para que se vea bien
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
    """Flujo: ¿Desea ver posibles candidatos? -> Ver lista de postulantes"""
    # Esta función requiere una tabla 'Reclutamiento' en tu BD
    top = Toplevel()
    top.title("Procesos de Reclutamiento (Candidatos)")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # Nota: Esta consulta ASUME que tienes la tabla 'Reclutamiento'
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
    """
    Simulación del botón de Finanzas que actualiza los maestros de RR.HH.
    """
    messagebox.showinfo("Actualizar Maestros",
                         "RR.HH. es el origen de los datos. La lista de Empleados está actualizada.\n"
                         "Si el módulo de Finanzas necesita la lista, debe consultarla aquí.")


# --- Función Principal de la Ventana de RR.HH. ---

def abrir_rrhh(parent_window, nombre_usuario):
    # Oculta el home temporalmente
    parent_window.withdraw()

    root = Toplevel()
    root.title(f"Recursos Humanos - Usuario: {nombre_usuario}")
    root.state("zoomed")
    root.configure(bg="#1dc1dd") # Fondo Turquesa

    # --- Función para volver al home ---
    def volver_home():
        root.destroy()
        parent_window.deiconify() 
        parent_window.state("zoomed") 

    # --- Contenedores ---
    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)
    
    Button(frame_top, text="← Volver al Home", bg="#ff4d4d", fg="white",
           font=("Arial", 12, "bold"), command=volver_home).pack(pady=5, padx=20, fill=X)
    
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

    # Alta de Empleado (USA LA FUNCIÓN CORREGIDA)
    Button(frame_botones_emp, text="Dar de Alta", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: alta_empleado(root)).pack(side=LEFT, padx=5)

    # Baja de Empleado
    Button(frame_botones_emp, text="Dar de Baja", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: baja_empleado(root)).pack(side=LEFT, padx=5)

    # Modificar Empleado
    Button(frame_botones_emp, text="Modificar Datos", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: modificar_empleado(root)).pack(side=LEFT, padx=5)

    # Consultar/Ver Empleados
    Button(frame_botones_emp, text="Ver Empleados", bg="#0089a1", fg="white", font=("Arial", 12, "bold"),
           width=18, command=ver_lista_empleados).pack(side=LEFT, padx=5)
    
    # --- Fila 2: Reclutamiento y Conexión ---
    frame_reclutamiento = Frame(frame_acciones, bg="#1dc1dd")
    frame_reclutamiento.pack(pady=5)
    Label(frame_reclutamiento, text="Reclutamiento y Conexión de Datos", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_rec = Frame(frame_reclutamiento, bg="#1dc1dd")
    frame_botones_rec.pack()

    # Ver Posibles Candidatos
    Button(frame_botones_rec, text="Ver Candidatos", bg="#006779", fg="white", font=("Arial", 12, "bold"),
           width=25, command=ver_posibles_candidatos).pack(side=LEFT, padx=10)
    
    # Simulación de la actualización de maestros de Finanzas (Conexión)
    Button(frame_botones_rec, text="Actualizar Maestros (Finanzas)", bg="#006779", fg="white", font=("Arial", 12, "bold"),
           width=25, command=actualizar_maestros).pack(side=LEFT, padx=10)


    root.mainloop()

# --- Ejemplo de uso (simulando la ventana principal) ---
if __name__ == '__main__':
    main_root = Tk()
    main_root.title("Home (Simulación)")
    main_root.geometry("400x200")
    
    def ejecutar_rrhh():
        abrir_rrhh(main_root, "Gerente RRHH")

    Label(main_root, text="Ventana Principal", font=("Arial", 16, "bold")).pack(pady=20)
    Button(main_root, text="Abrir Módulo de RR.HH.", bg="#1dc1dd", fg="white",
           font=("Arial", 12, "bold"), command=ejecutar_rrhh).pack(pady=10)

    main_root.mainloop()