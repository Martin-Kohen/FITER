from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date
import subprocess
import sys 
# Configuración de la conexión a la base de datos
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

def actualizar_ingreso(parent_window):
    """Inserta un nuevo registro de ingreso."""
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
    messagebox.showinfo("Lista de Bajas", "Simulación:\nMostrando registros de bajas de Clientes/Máquinas...")


def mostrar_historial(tabla, titulo, columnas, consulta_sql):
    """Función genérica para mostrar cualquier historial en una nueva ventana."""
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

def abrir_finanzas(parent_window, nombre_usuario, rol):
    # La ventana principal (parent_window) se oculta para que no aparezca
    # si la aplicación se inicia directamente.
    parent_window.withdraw() 
    root = Toplevel()
    root.title(f"Finanzas - Usuario: {nombre_usuario}")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)

    if rol == "Gerente":
        Button(frame_top, text="⬅ Volver al Home", bg="#0089a1", fg="white",
                font=("Arial", 12, "bold"),
                command=lambda: volver_home_gerente(root, parent_window, nombre_usuario, rol)
        ).pack(pady=5, padx=20, fill=X)
    else:
        Button(frame_top, text="❌ Cerrar Sesión", bg="#ff4d4d", fg="white",
                font=("Arial", 12, "bold"),
                command=lambda: cerrar_sesion_finanzas(root, parent_window)
        ).pack(pady=5, padx=20, fill=X)

    Label(frame_top, text="Módulo de Finanzas", bg="#1dc1dd", fg="white",
            font=("Arial", 18, "bold")).pack(pady=10)

    frame_acc = Frame(root, bg="#1dc1dd")
    frame_acc.pack(pady=20)

    Button(frame_acc, text="Registrar Ingreso", bg="#0089a1", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=lambda: actualizar_ingreso(root)).pack(pady=10)

    Button(frame_acc, text="Generar Presupuesto", bg="#0089a1", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=lambda: generar_presupuesto(root)).pack(pady=10)

    Button(frame_acc, text="Generar Plan Financiero", bg="#0089a1", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=lambda: generar_plan_financiero(root)).pack(pady=10)

    Button(frame_acc, text="Historial Ingresos", bg="#006779", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=ver_historial_ingresos).pack(pady=10)

    Button(frame_acc, text="Historial Presupuestos", bg="#006779", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=ver_historial_presupuestos).pack(pady=10)

    Button(frame_acc, text="Historial Planes", bg="#006779", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=ver_historial_planes).pack(pady=10)

    Button(frame_acc, text="Baja de Ingreso", bg="#dc3545", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=lambda: baja_ingreso(root)).pack(pady=10)

    Button(frame_acc, text="Baja de Presupuesto", bg="#dc3545", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=lambda: baja_presupuesto(root)).pack(pady=10)

    Button(frame_acc, text="Baja de Plan Financiero", bg="#dc3545", fg="white",
            font=("Arial", 14, "bold"), width=25,
            command=lambda: baja_plan(root)).pack(pady=10)

    root.mainloop()
def volver_home_gerente(root, parent_window, nombre_usuario, rol):
    """Vuelve al home del gerente sin cerrar sesión."""
    root.destroy()
    subprocess.Popen([sys.executable, "Partes/home_gerente.py", nombre_usuario, rol])


def cerrar_sesion_finanzas(root, parent_window):
    """Cierra sesión y vuelve al login."""
    root.destroy()
    subprocess.Popen([sys.executable, "Partes/home_deslog.py"])


# --- Inicio directo de la aplicación ---
if __name__ == '__main__':
    # Creamos la ventana principal (root) pero la ocultamos inmediatamente
    # para que la aplicación inicie directamente en el módulo de Finanzas.
    main_root = Tk()
    main_root.withdraw() # Oculta la ventana principal

    # Datos de usuario de prueba
    nombre_usuario = "Test Finanzas"
    rol = "Empleado"

    # Llamada directa para abrir el módulo de Finanzas usando el root oculto como padre
    abrir_finanzas(main_root, nombre_usuario, rol)
    
    # Iniciar el bucle de eventos
    main_root.mainloop()