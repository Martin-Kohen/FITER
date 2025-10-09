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

# --- Funciones de Lógica de Finanzas (Creación y Simulación) ---

def actualizar_ingreso(parent_window):
    """Inserta un nuevo registro de ingreso."""
    # (Código sin cambios)
    monto = simpledialog.askfloat("Nuevo Ingreso", "Monto del Ingreso:", parent=parent_window)
    if monto is None or monto <= 0: return
    descripcion = simpledialog.askstring("Nuevo Ingreso", "Descripción:", parent=parent_window)
    if not descripcion: return
    fecha_str = simpledialog.askstring("Nuevo Ingreso", "Fecha (YYYY-MM-DD):", parent=parent_window, initialvalue=str(date.today()))
    try:
        fecha = date.fromisoformat(fecha_str)
    except (ValueError, TypeError):
        messagebox.showerror("Error de Fecha", "Formato de fecha incorrecto.")
        return
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Registro_Contable (Fecha, Monto, Descripcion, Tipo_Transaccion) VALUES (%s, %s, %s, 'Ingreso')"
            cursor.execute(sql, (fecha, monto, descripcion))
            conn.commit()
            messagebox.showinfo("Éxito", f"Ingreso de ${monto:.2f} registrado con éxito.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al registrar ingreso: {err}")
        finally:
            cursor.close()
            conn.close()

def generar_presupuesto(parent_window):
    """Registra un nuevo presupuesto."""
    # (Código sin cambios)
    año = simpledialog.askinteger("Generar Presupuesto", "Año del Presupuesto (ej. 2026):", parent=parent_window)
    if not año: return
    monto = simpledialog.askfloat("Generar Presupuesto", "Monto Total Estimado:", parent=parent_window)
    if monto is None or monto <= 0: return
    estado = simpledialog.askstring("Generar Presupuesto", "Estado (ej. Borrador/Aprobado):", parent=parent_window, initialvalue="Borrador")
    if not estado: return
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Presupuestos (Año, Monto_Total, Estado_Presupuesto) VALUES (%s, %s, %s)"
            cursor.execute(sql, (año, monto, estado))
            conn.commit()
            messagebox.showinfo("Éxito", f"Presupuesto para {año} (Monto: ${monto:.2f}) registrado.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al generar presupuesto: {err}")
        finally:
            cursor.close()
            conn.close()

def generar_plan_financiero(parent_window):
    """Registra una nueva Planificación."""
    # (Código sin cambios)
    periodo = simpledialog.askstring("Plan Financiero", "Periodo (ej. Trimestre 3):", parent=parent_window)
    if not periodo: return
    objetivo = simpledialog.askstring("Plan Financiero", "Objetivo Principal:", parent=parent_window)
    if not objetivo: return
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Planificacion (Fecha, Periodo, Objetivo, Alcance) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (date.today(), periodo, objetivo, "Definido por Finanzas"))
            conn.commit()
            messagebox.showinfo("Éxito", f"Plan Financiero para {periodo} registrado.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al generar plan: {err}")
        finally:
            cursor.close()
            conn.close()

def ver_lista_bajas():
    """Simula la consulta a las tablas de bajas de otras áreas."""
    # (Código sin cambios)
    messagebox.showinfo("Lista de Bajas", "Simulación:\nMostrando registros de bajas de Clientes/Máquinas...")

def actualizar_empleados_maquinas():
    """Simula la acción de mantener actualizados los maestros."""
    # (Código sin cambios)
    messagebox.showinfo("Actualizar Maestros", "Simulación:\nSe ha iniciado la actualización de la lista maestra de Empleados y Maquinaria.")


# --- Funciones de Historial (Consultas) ---

def mostrar_historial(tabla, titulo, columnas, consulta_sql):
    """Función genérica para mostrar cualquier historial en una nueva ventana."""
    # (Código sin cambios)
    top = Toplevel()
    top.title(f"Historial de {titulo}")
    top.geometry("800x400")
    top.configure(bg="#1dc1dd")
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(consulta_sql)
            datos = cursor.fetchall()
            header = " | ".join(columnas)
            Label(top, text=header, bg="#ffffff", fg="#000000", font=("Arial", 12, "bold")).pack(fill=X, padx=10, pady=5)
            if datos:
                for fila in datos:
                    fila_str = " | ".join([str(item) for item in fila])
                    Label(top, text=fila_str, bg="#f0f0ff", fg="black", font=("Arial", 10), anchor="w", justify=LEFT, wraplength=750).pack(fill=X, padx=10, pady=1)
            else:
                Label(top, text=f"No hay registros en el historial de {titulo}.", bg="#ffffff", fg="black", font=("Arial", 12)).pack(padx=10, pady=10)
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar {titulo}: {err}")
        finally:
            cursor.close()
            conn.close()

def ver_historial_ingresos():
    mostrar_historial("Registro_Contable", "Ingresos", ["ID", "Fecha", "Monto", "Descripción"], "SELECT ID_Registro_Contable, Fecha, Monto, Descripcion FROM Registro_Contable WHERE Tipo_Transaccion = 'Ingreso' ORDER BY Fecha DESC")

def ver_historial_presupuestos():
    mostrar_historial("Presupuestos", "Presupuestos", ["ID", "Año", "Monto Total", "Estado"], "SELECT ID_Presupuesto, Año, Monto_Total, Estado_Presupuesto FROM Presupuestos ORDER BY Año DESC")

def ver_historial_planes():
    mostrar_historial("Planificacion", "Planes Financieros", ["ID", "Fecha", "Período", "Objetivo"], "SELECT ID_Planificacion, Fecha, Periodo, Objetivo FROM Planificacion ORDER BY Fecha DESC")


# --- NUEVAS Funciones para Bajas (Eliminar) ---

def baja_generica(parent_window, nombre_entidad, tabla, id_columna):
    """Función genérica para eliminar un registro por ID."""
    id_a_borrar = simpledialog.askinteger(f"Baja de {nombre_entidad}", f"Ingresa el ID del {nombre_entidad} a eliminar:", parent=parent_window)
    if id_a_borrar is None:
        return

    confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar el {nombre_entidad} con ID {id_a_borrar}?\nEsta acción no se puede deshacer.", icon='warning')
    if not confirm:
        return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            sql = f"DELETE FROM {tabla} WHERE {id_columna} = %s"
            cursor.execute(sql, (id_a_borrar,))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"{nombre_entidad} con ID {id_a_borrar} eliminado correctamente.")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró ningún {nombre_entidad} con el ID {id_a_borrar}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al eliminar el {nombre_entidad}: {err}")
        finally:
            cursor.close()
            conn.close()

def baja_ingreso(parent_window):
    """Da de baja un registro de ingreso."""
    baja_generica(parent_window, "Ingreso", "Registro_Contable", "ID_Registro_Contable")

def baja_presupuesto(parent_window):
    """Da de baja un presupuesto."""
    baja_generica(parent_window, "Presupuesto", "Presupuestos", "ID_Presupuesto")

def baja_plan(parent_window):
    """Da de baja un plan financiero."""
    baja_generica(parent_window, "Plan Financiero", "Planificacion", "ID_Planificacion")


# --- Función Principal de la Ventana de Finanzas (Diseño Actualizado) ---

def abrir_finanzas(parent_window, nombre_usuario):
    parent_window.withdraw()
    root = Toplevel()
    root.title(f"Finanzas - Usuario: {nombre_usuario}")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    def volver_home():
        root.destroy()
        parent_window.deiconify()
        parent_window.state("zoomed")

    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)
    Button(frame_top, text="← Volver al Home", bg="#ff4d4d", fg="white", font=("Arial", 12, "bold"), command=volver_home).pack(pady=5, padx=20, fill=X)
    Label(frame_top, text="Módulo de Finanzas", bg="#1dc1dd", fg="white", font=("Arial", 18, "bold")).pack(pady=10)

    # --- Contenedor Principal de Acciones ---
    frame_acciones = Frame(root, bg="#1dc1dd")
    frame_acciones.pack(pady=10)

    # --- Fila 1: Operaciones Principales ---
    frame_operaciones = Frame(frame_acciones, bg="#1dc1dd")
    frame_operaciones.pack(pady=5)
    Label(frame_operaciones, text="Operaciones y Planeación", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_op = Frame(frame_operaciones, bg="#1dc1dd")
    frame_botones_op.pack()

    Button(frame_botones_op, text="💰 Registrar Ingreso", bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=22, command=lambda: actualizar_ingreso(root)).pack(side=LEFT, padx=5)
    Button(frame_botones_op, text="📝 Generar Presupuesto", bg="#e37222", fg="white", font=("Arial", 12, "bold"), width=22, command=lambda: generar_presupuesto(root)).pack(side=LEFT, padx=5)
    Button(frame_botones_op, text="📈 Generar Plan Financiero", bg="#a44c9d", fg="white", font=("Arial", 12, "bold"), width=22, command=lambda: generar_plan_financiero(root)).pack(side=LEFT, padx=5)
    Button(frame_botones_op, text="🔄 Actualizar Maestros", bg="#ffc107", fg="black", font=("Arial", 12, "bold"), width=22, command=actualizar_empleados_maquinas).pack(side=LEFT, padx=5)

    # --- Fila 2: Consultas e Historiales ---
    frame_consultas = Frame(frame_acciones, bg="#1dc1dd")
    frame_consultas.pack(pady=5)
    Label(frame_consultas, text="Historiales y Consultas", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_hist = Frame(frame_consultas, bg="#1dc1dd")
    frame_botones_hist.pack()

    Button(frame_botones_hist, text="🔎 Historial Ingresos", bg="#007bff", fg="white", font=("Arial", 12, "bold"), width=22, command=ver_historial_ingresos).pack(side=LEFT, padx=5)
    Button(frame_botones_hist, text="🔎 Historial Presupuestos", bg="#007bff", fg="white", font=("Arial", 12, "bold"), width=22, command=ver_historial_presupuestos).pack(side=LEFT, padx=5)
    Button(frame_botones_hist, text="🔎 Historial Planes", bg="#007bff", fg="white", font=("Arial", 12, "bold"), width=22, command=ver_historial_planes).pack(side=LEFT, padx=5)
    Button(frame_botones_hist, text="👁️ Ver Bajas (Clientes/Maq)", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), width=22, command=ver_lista_bajas).pack(side=LEFT, padx=5)

    # --- Fila 3: Bajas (Acciones de Eliminación) ---
    frame_bajas = Frame(frame_acciones, bg="#1dc1dd")
    frame_bajas.pack(pady=5)
    Label(frame_bajas, text="Eliminación de Registros", bg="#1dc1dd", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
    frame_botones_bajas = Frame(frame_bajas, bg="#1dc1dd")
    frame_botones_bajas.pack()

    Button(frame_botones_bajas, text="➖ Baja de Ingreso", bg="#dc3545", fg="white", font=("Arial", 12, "bold"), width=22, command=lambda: baja_ingreso(root)).pack(side=LEFT, padx=5)
    Button(frame_botones_bajas, text="➖ Baja de Presupuesto", bg="#dc3545", fg="white", font=("Arial", 12, "bold"), width=22, command=lambda: baja_presupuesto(root)).pack(side=LEFT, padx=5)
    Button(frame_botones_bajas, text="➖ Baja de Plan Financiero", bg="#dc3545", fg="white", font=("Arial", 12, "bold"), width=22, command=lambda: baja_plan(root)).pack(side=LEFT, padx=5)

    root.mainloop()

# --- Ejemplo de uso ---
if __name__ == '__main__':
    main_root = Tk()
    main_root.title("Home")
    main_root.geometry("400x200")
    
    def ejecutar_finanzas():
        abrir_finanzas(main_root, "CFO")

    Label(main_root, text="Ventana Principal", font=("Arial", 16, "bold")).pack(pady=20)
    Button(main_root, text="Abrir Módulo de Finanzas", bg="#1dc1dd", fg="white", font=("Arial", 12, "bold"), command=ejecutar_finanzas).pack(pady=10)

    main_root.mainloop()