from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date

# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
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

# --- Funciones de Lógica de RR.HH. (Mapeo del Diagrama de Flujo) ---

# ----------------- GESTIÓN DE EMPLEADOS -----------------

def alta_empleado(parent_window):
    """Flujo: ¿Desea dar de alta un empleado? -> Ingresar datos -> Guardar en BD"""
    # 1. Solicitar Datos
    id_empleado = simpledialog.askinteger("Alta Empleado", "ID Empleado:", parent=parent_window)
    if not id_empleado: return

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
        messagebox.showerror("Error", "Formato de fecha incorrecto.")
        return

    # 2. Guardar en BD (Empleados_RRHH)
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Empleados_RRHH (ID_Empleado, Nombre, Apellido, Puesto, Fecha_Contratacion) 
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_empleado, nombre, apellido, puesto, fecha_contratacion))
            conn.commit()
            messagebox.showinfo("Éxito", f"Empleado {nombre} {apellido} registrado con éxito.")
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
            # Nota: En sistemas reales se usaría un campo 'Estado' (Activo/Inactivo)
            # Aquí, para simplicidad, usamos DELETE.
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
                    emp_str = f"{emp[0]} | {emp[1]} | {emp[2]} | {emp[3]} | {emp[4]}"
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
    # Consulta a la tabla Reclutamiento para ver los procesos abiertos
    top = Toplevel()
    top.title("Procesos de Reclutamiento (Candidatos)")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_Reclutamiento, Descripcion_Puesto, Salario_Ofrecido, Estado_Proceso FROM Reclutamiento WHERE Estado_Proceso != 'Cerrado'")
            procesos = cursor.fetchall()

            header = "ID | Puesto | Salario Ofrecido | Estado"
            Label(top, text=header, bg="#ffffff", fg="#000000", font=("Arial", 12, "bold")).pack(fill=X, padx=10, pady=5)

            if procesos:
                for proc in procesos:
                    proc_str = f"{proc[0]} | {proc[1][:40]}... | ${proc[2]:.2f} | {proc[3]}"
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
    Esta función simula que RR.HH. es el origen de los datos maestros.
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
    
    # --- Fila 1: Gestión de Empleados (Mapeo de las decisiones del diagrama) ---
    frame_empleados = Frame(frame_acciones, bg="#1dc1dd")
    frame_empleados.pack(pady=5)
    Label(frame_empleados, text="Gestión de Empleados", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_emp = Frame(frame_empleados, bg="#1dc1dd")
    frame_botones_emp.pack()

    # Alta de Empleado
    Button(frame_botones_emp, text="➕ Dar de Alta", bg="#28a745", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: alta_empleado(root)).pack(side=LEFT, padx=5)

    # Baja de Empleado
    Button(frame_botones_emp, text="➖ Dar de Baja", bg="#dc3545", fg="white", font=("Arial", 12, "bold"),
           width=18, command=lambda: baja_empleado(root)).pack(side=LEFT, padx=5)

    # Modificar Empleado
    Button(frame_botones_emp, text="✏️ Modificar Datos", bg="#ffc107", fg="black", font=("Arial", 12, "bold"),
           width=18, command=lambda: modificar_empleado(root)).pack(side=LEFT, padx=5)

    # Consultar/Ver Empleados
    Button(frame_botones_emp, text="📄 Ver Empleados", bg="#007bff", fg="white", font=("Arial", 12, "bold"),
           width=18, command=ver_lista_empleados).pack(side=LEFT, padx=5)
           
    # --- Fila 2: Reclutamiento y Conexión (Mapeo de Candidatos y Maestros) ---
    frame_reclutamiento = Frame(frame_acciones, bg="#1dc1dd")
    frame_reclutamiento.pack(pady=5)
    Label(frame_reclutamiento, text="Reclutamiento y Conexión de Datos", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_rec = Frame(frame_reclutamiento, bg="#1dc1dd")
    frame_botones_rec.pack()

    # Ver Posibles Candidatos
    Button(frame_botones_rec, text="🔍 Ver Candidatos", bg="#a44c9d", fg="white", font=("Arial", 12, "bold"),
           width=25, command=ver_posibles_candidatos).pack(side=LEFT, padx=10)
           
    # Simulación de la actualización de maestros de Finanzas (Conexión)
    Button(frame_botones_rec, text="📢 Actualizar Maestros (Finanzas)", bg="#00bcd4", fg="white", font=("Arial", 12, "bold"),
           width=25, command=actualizar_maestros).pack(side=LEFT, padx=10)


    root.mainloop()

# --- Ejemplo de uso (simulando la ventana principal) ---
if __name__ == '__main__':
    main_root = Tk()
    main_root.title("Home")
    main_root.geometry("400x200")
    
    def ejecutar_rrhh():
        abrir_rrhh(main_root, "Gerente RRHH")

    Label(main_root, text="Ventana Principal", font=("Arial", 16, "bold")).pack(pady=20)
    Button(main_root, text="Abrir Módulo de RR.HH.", bg="#1dc1dd", fg="white",
           font=("Arial", 12, "bold"), command=ejecutar_rrhh).pack(pady=10)

    main_root.mainloop()