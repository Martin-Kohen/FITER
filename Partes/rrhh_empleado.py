from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date
import re 
try:
    import login 
except ImportError:
    messagebox.showerror("Error de Importación", "No se encontró el archivo 'login.py'. Asegúrate de que esté en la misma carpeta.")


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

# ----------------- FUNCIONES AUXILIARES -----------------

def parse_descripcion(descripcion):
    """Extrae Nombre, Apellido, Puesto y Área de la cadena de descripción."""
    # Ejemplo de cadena: "Propuesta de Autoregistro - Puesto: Empleado en Área: Finanzas. Usuario: Juan Perez"
    
    # 1. Extraer Puesto y Área (que se mapea a Departamento)
    puesto_match = re.search(r"Puesto: (.*?) en Área: (.*?)\.", descripcion)
    puesto = puesto_match.group(1).strip() if puesto_match else "N/A"
    # El nombre del área debe coincidir con los nombres en la tabla Departamentos/Empleados_RRHH (Ej: Finanzas)
    area = puesto_match.group(2).strip() if puesto_match else "N/A" 
    
    # 2. Extraer Nombre y Apellido
    usuario_match = re.search(r"Usuario: (.*?) (.*?)$", descripcion)
    nombre = usuario_match.group(1).strip() if usuario_match else "N/A"
    apellido = usuario_match.group(2).strip() if usuario_match else "N/A"
    
    return nombre, apellido, puesto, area 


# ----------------- RECLUTAMIENTO Y APROBACIÓN -----------------

def aprobar_propuesta_reclutamiento(id_reclutamiento, parent_window):
    """
    Función que maneja el flujo de APROBACIÓN para un ID específico:
    1. Pide Salario.
    2. Mueve datos a Empleados_RRHH (Alta).
    3. Cierra el proceso de Reclutamiento.
    """
    if id_reclutamiento is None: return

    conn = conectar_bd()
    if not conn: return
    # No usamos dictionary=True si vamos a usar .lastrowid
    cursor = conn.cursor() 

    try:
        # 1. Obtener la información de la propuesta
        sql_select = "SELECT Descripcion_Puesto, Estado_Proceso FROM Reclutamiento WHERE ID_Reclutamiento = %s"
        cursor.execute(sql_select, (id_reclutamiento,))
        # Usamos fetchone() sin dictionary=True, el resultado es una tupla
        propuesta_tuple = cursor.fetchone() 

        if not propuesta_tuple:
            messagebox.showwarning("Error", f"No se encontró la propuesta con ID {id_reclutamiento}.")
            return
            
        descripcion_puesto, estado_proceso = propuesta_tuple
            
        if estado_proceso != 'Pendiente RRHH':
            messagebox.showwarning("Advertencia", "Esta propuesta ya fue procesada o no está pendiente de aprobación.")
            return

        # 2. Parsear los datos del empleado
        nombre, apellido, puesto, area = parse_descripcion(descripcion_puesto)
        
        # 3. Pedir el Salario
        salario_str = simpledialog.askstring("Salario", f"Ingrese el Salario (€/$) para {nombre} {apellido}:", parent=parent_window)
        if not salario_str: return

        try:
            salario = float(salario_str)
            if salario <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Salario inválido. Debe ser un número positivo.")
            return

        # A) Insertar en Empleados_RRHH (Alta del Empleado)
        fecha_contratacion = date.today().strftime("%Y-%m-%d")
        
        # CORRECCIÓN CLAVE: Usamos 'Departamento' (la columna que existe en tu tabla)
        sql_insert_rrhh = """INSERT INTO Empleados_RRHH (Nombre, Apellido, Puesto, Departamento, Fecha_Contratacion) 
                             VALUES (%s, %s, %s, %s, %s)"""
                             
        cursor.execute(sql_insert_rrhh, (nombre, apellido, puesto, area, fecha_contratacion))
        nuevo_id_empleado = cursor.lastrowid # Obtiene el ID generado por AUTO_INCREMENT

        # B) Actualizar el proceso de Reclutamiento (Cerrar Propuesta)
        sql_update_reclutamiento = """UPDATE Reclutamiento 
                                      SET Estado_Proceso = %s, Salario_Ofrecido = %s, Fecha_Cierre = %s 
                                      WHERE ID_Reclutamiento = %s"""
        cursor.execute(sql_update_reclutamiento, ('Aprobado - Contratado', salario, fecha_contratacion, id_reclutamiento))
        
        # FINALIZAR TRANSACCIÓN (guardar cambios)
        conn.commit() 
        messagebox.showinfo("Éxito de Aprobación", 
                            f"¡Propuesta APROBADA! ✅\n"
                            f"**{nombre} {apellido}** registrado en RR.HH. (ID: {nuevo_id_empleado}).")
        
        # Refrescar la lista 
        if lista_candidatos_window and lista_candidatos_window.winfo_exists():
            lista_candidatos_window.destroy()
            ver_posibles_candidatos()

    except mysql.connector.Error as err:
        conn.rollback() 
        # CORRECCIÓN DE ERROR: Eliminamos la llamada a conn.rollback() dentro del try
        # Usamos el error específico de la BD.
        messagebox.showerror("Error de BD", f"Error durante la aprobación/inserción: {err}")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def denegar_propuesta_reclutamiento(id_reclutamiento):
    """Función para Denegar una propuesta, cerrando el proceso sin contratar."""
    if id_reclutamiento is None: return

    confirm = messagebox.askyesno("Confirmar Denegación", f"¿Estás seguro de DENERGAR la propuesta con ID {id_reclutamiento}? El proceso se cerrará.", icon='error')
    if not confirm: return

    conn = conectar_bd()
    if not conn: return
    cursor = conn.cursor()

    try:
        fecha_cierre = date.today().strftime("%Y-%m-%d")

        sql_update_reclutamiento = """UPDATE Reclutamiento 
                                      SET Estado_Proceso = %s, Fecha_Cierre = %s 
                                      WHERE ID_Reclutamiento = %s AND Estado_Proceso = 'Pendiente RRHH'"""
        cursor.execute(sql_update_reclutamiento, ('Denegado', fecha_cierre, id_reclutamiento))
        
        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Éxito", f"Propuesta ID {id_reclutamiento} **DENERGADA** y proceso cerrado.")
            
            # Refrescar la lista
            if lista_candidatos_window and lista_candidatos_window.winfo_exists():
                lista_candidatos_window.destroy()
                ver_posibles_candidatos()
        else:
            messagebox.showwarning("Advertencia", f"No se encontró la propuesta PENDIENTE con ID {id_reclutamiento}.")
            
    except mysql.connector.Error as err:
        conn.rollback()
        messagebox.showerror("Error de BD", f"Error durante la denegación: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ----------------- GESTIÓN DE EMPLEADOS -----------------

def alta_empleado(parent_window):
    """Da de alta un empleado (manual)."""
    nombre = simpledialog.askstring("Alta Empleado", "Nombre:", parent=parent_window)
    if not nombre: return

    apellido = simpledialog.askstring("Alta Empleado", "Apellido:", parent=parent_window)
    if not apellido: return
    
    puesto = simpledialog.askstring("Alta Empleado", "Puesto:", parent=parent_window)
    if not puesto: return
    
    # Aquí pedimos el nombre del departamento, que es lo que acepta la tabla Empleados_RRHH
    departamento_nombre = simpledialog.askstring("Alta Empleado", "Departamento (Ej: Finanzas):", parent=parent_window)
    if not departamento_nombre: return
    
    fecha_contratacion_str = simpledialog.askstring("Alta Empleado", "Fecha Contratación (YYYY-MM-DD):", parent=parent_window)
    try:
        fecha_contratacion = date.fromisoformat(fecha_contratacion_str)
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Formato de fecha incorrecto (debe ser YYYY-MM-DD).")
        return

    conn = conectar_bd()
    if not conn: return
    
    cursor = conn.cursor()
    try:
        # CORRECCIÓN CLAVE: Usamos la columna 'Departamento'
        sql = """INSERT INTO Empleados_RRHH (Nombre, Apellido, Puesto, Departamento, Fecha_Contratacion) 
                 VALUES (%s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (nombre, apellido, puesto, departamento_nombre, fecha_contratacion))
        conn.commit()
        
        nuevo_id = cursor.lastrowid
        messagebox.showinfo("Éxito", f"Empleado {nombre} {apellido} registrado con éxito.\nID Generado: {nuevo_id}")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error de BD", f"Error al insertar el empleado: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def baja_empleado(parent_window):
    """Flujo: Dar de baja un empleado y su usuario asociado."""
    id_a_borrar = simpledialog.askinteger("Baja Empleado", "Ingresa el ID del empleado a dar de baja:", parent=parent_window)
    if id_a_borrar is None: return

    confirm = messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de dar de BAJA al empleado con ID {id_a_borrar}?", icon='warning')
    if not confirm: return

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # 1. Eliminar de Empleados_RRHH
            sql = "DELETE FROM Empleados_RRHH WHERE ID_Empleado = %s"
            cursor.execute(sql, (id_a_borrar,))
            
            # 2. Eliminar de Usuario 
            sql_user = "DELETE FROM usuario WHERE idUsuario = %s"
            cursor.execute(sql_user, (id_a_borrar,))

            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Empleado y Usuario con ID {id_a_borrar} dados de baja (eliminados).")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró empleado con ID {id_a_borrar}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al dar de baja: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

def modificar_empleado(parent_window):
    """Flujo: Modificar Puesto de Empleado"""
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
            if conn and conn.is_connected():
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
    top.geometry("900x500") 
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
            sql_select = """
            SELECT 
                ID_Empleado, Nombre, Apellido, Puesto, Departamento, Fecha_Contratacion 
            FROM Empleados_RRHH
            ORDER BY ID_Empleado
            """
            cursor.execute(sql_select)
            empleados = cursor.fetchall()
            
            # --- TÍTULO Y CABECERA (Header) ---
            Label(top, text="Lista de Empleados Actuales", bg="#1dc1dd", fg="white", 
                  font=("Arial", 16, "bold")).pack(fill=X, padx=10, pady=10)

            header = Frame(top, bg="#ffffff")
            header.pack(fill=X, padx=10, pady=(0, 5))
            
            Label(header, text="ID", bg="#ffffff", font=("Arial", 10, "bold"), width=5).pack(side=LEFT, padx=5)
            Label(header, text="Nombre", bg="#ffffff", font=("Arial", 10, "bold"), width=15).pack(side=LEFT, padx=5)
            Label(header, text="Apellido", bg="#ffffff", font=("Arial", 10, "bold"), width=15).pack(side=LEFT, padx=5)
            Label(header, text="Puesto", bg="#ffffff", font=("Arial", 10, "bold"), width=20).pack(side=LEFT, padx=5)
            Label(header, text="Departamento", bg="#ffffff", font=("Arial", 10, "bold"), width=20).pack(side=LEFT, padx=5)
            Label(header, text="Contratación", bg="#ffffff", font=("Arial", 10, "bold"), width=15).pack(side=LEFT, padx=5)

            if empleados:
                canvas = Canvas(top, bg="#1dc1dd")
                scrollbar = Scrollbar(top, orient="vertical", command=canvas.yview)
                scrollable_frame = Frame(canvas, bg="#1dc1dd")

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
                scrollbar.pack(side="right", fill="y")
                
                for emp in empleados:
                    id_emp, nombre, apellido, puesto, depto_nombre, fecha_contratacion = emp
                    
                    fecha_contratacion_str = fecha_contratacion.strftime("%Y-%m-%d") if isinstance(fecha_contratacion, date) else str(fecha_contratacion)
                    
                    row_frame = Frame(scrollable_frame, bg="#f0f0ff")
                    row_frame.pack(fill=X, pady=1)

                    Label(row_frame, text=id_emp, bg="#f0f0ff", font=("Arial", 10), width=5).pack(side=LEFT, padx=5)
                    Label(row_frame, text=nombre, bg="#f0f0ff", font=("Arial", 10), width=15).pack(side=LEFT, padx=5)
                    Label(row_frame, text=apellido, bg="#f0f0ff", font=("Arial", 10), width=15).pack(side=LEFT, padx=5)
                    Label(row_frame, text=puesto, bg="#f0f0ff", font=("Arial", 10), width=20).pack(side=LEFT, padx=5)
                    Label(row_frame, text=depto_nombre or "N/A", bg="#f0f0ff", font=("Arial", 10), width=20).pack(side=LEFT, padx=5)
                    Label(row_frame, text=fecha_contratacion_str, bg="#f0f0ff", font=("Arial", 10), width=15).pack(side=LEFT, padx=5)
            else:
                Label(top, text="No hay empleados registrados.", bg="#ffffff", fg="black", font=("Arial", 12)).pack(padx=10, pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar empleados: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

def ver_posibles_candidatos():
    """Muestra la lista de procesos de reclutamiento con botones de acción por fila."""
    global lista_candidatos_window
    
    if lista_candidatos_window and lista_candidatos_window.winfo_exists():
        lista_candidatos_window.lift()
        return
        
    top = Toplevel()
    lista_candidatos_window = top
    top.title("Procesos de Reclutamiento (Candidatos)")
    top.geometry("1300x600") 
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
            sql_reclutamiento = "SELECT ID_Reclutamiento, Descripcion_Puesto, Salario_Ofrecido, Estado_Proceso, Fecha_Solicitud FROM Reclutamiento WHERE Estado_Proceso != 'Cerrado' ORDER BY Fecha_Solicitud DESC"
            cursor.execute(sql_reclutamiento)
            procesos = cursor.fetchall()
            
            # --- TÍTULO Y CABECERA (Header) ---
            Label(top, text="Lista de Propuestas y Vacantes Activas", bg="#1dc1dd", fg="white", 
                  font=("Arial", 16, "bold")).pack(fill=X, padx=10, pady=10)

            header = Frame(top, bg="#ffffff")
            header.pack(fill=X, padx=10, pady=(0, 5))
            
            Label(header, text="ID", bg="#ffffff", font=("Arial", 10, "bold"), width=5).pack(side=LEFT, padx=5)
            Label(header, text="Fecha", bg="#ffffff", font=("Arial", 10, "bold"), width=10).pack(side=LEFT, padx=5)
            Label(header, text="Descripción del Puesto", bg="#ffffff", font=("Arial", 10, "bold"), width=60).pack(side=LEFT, padx=5)
            Label(header, text="Salario", bg="#ffffff", font=("Arial", 10, "bold"), width=15).pack(side=LEFT, padx=5)
            Label(header, text="Estado", bg="#ffffff", font=("Arial", 10, "bold"), width=15).pack(side=LEFT, padx=5)
            Label(header, text="Acciones", bg="#ffffff", font=("Arial", 10, "bold"), width=25).pack(side=LEFT, padx=5)


            if procesos:
                canvas = Canvas(top, bg="#1dc1dd")
                scrollbar = Scrollbar(top, orient="vertical", command=canvas.yview)
                scrollable_frame = Frame(canvas, bg="#1dc1dd")

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                canvas.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))
                scrollbar.pack(side="right", fill="y")
                
                for proc in procesos:
                    id_reclutamiento, descripcion, salario, estado, fecha_solicitud = proc
                    
                    salario_formateado = f"${salario:,.2f}" if salario is not None else "N/A"
                    fecha_formateada = fecha_solicitud.strftime("%Y-%m-%d")

                    row_frame = Frame(scrollable_frame, bg="#f0f0ff")
                    row_frame.pack(fill=X, pady=1)

                    # Datos de la propuesta
                    Label(row_frame, text=id_reclutamiento, bg="#f0f0ff", font=("Arial", 10), width=5).pack(side=LEFT, padx=5)
                    Label(row_frame, text=fecha_formateada, bg="#f0f0ff", font=("Arial", 10), width=10).pack(side=LEFT, padx=5)
                    Label(row_frame, text=descripcion, bg="#f0f0ff", fg="black",
                          font=("Arial", 10), anchor="w", width=60, wraplength=450, justify=LEFT).pack(side=LEFT, padx=5)
                    Label(row_frame, text=salario_formateado, bg="#f0f0ff", font=("Arial", 10), width=15).pack(side=LEFT, padx=5)
                    Label(row_frame, text=estado, bg="#f0f0ff", font=("Arial", 10), width=15).pack(side=LEFT, padx=5)
                    
                    # --- FRAME DE ACCIONES POR FILA ---
                    frame_acciones_fila = Frame(row_frame, bg="#f0f0ff")
                    frame_acciones_fila.pack(side=LEFT, padx=5)
                    
                    # Los botones solo se muestran si el estado es 'Pendiente RRHH'
                    if estado == 'Pendiente RRHH':
                        # Botón Aprobar
                        Button(frame_acciones_fila, text="Aprobar", bg="#00aa00", fg="white", 
                               font=("Arial", 8, "bold"), width=8, height=1,
                               command=lambda id=id_reclutamiento: aprobar_propuesta_reclutamiento(id, top)).pack(side=LEFT, padx=2, pady=1)

                        # Botón Denegar
                        Button(frame_acciones_fila, text="Denegar", bg="#cc0000", fg="white", 
                               font=("Arial", 8, "bold"), width=8, height=1,
                               command=lambda id=id_reclutamiento: denegar_propuesta_reclutamiento(id)).pack(side=LEFT, padx=2, pady=1)
                    else:
                        Label(frame_acciones_fila, text=f"Proceso {estado}", bg="#f0f0ff", fg="gray", font=("Arial", 8)).pack(padx=5)


            else:
                Label(top, text="No hay procesos de reclutamiento abiertos.", bg="#ffffff", fg="black", font=("Arial", 12)).pack(padx=10, pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al consultar reclutamiento: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

# ----------------- CONEXIÓN FINANZAS (SIMULACIÓN) -----------------

def actualizar_maestros():
    """Simulación de actualización de maestros (RR.HH. es la fuente)."""
    messagebox.showinfo("Actualizar Maestros",
                         "RR.HH. es el origen de los datos. La lista de Empleados está actualizada.\n"
                         "Si el módulo de Finanzas necesita la lista, debe consultarla aquí.")

# --- Función para cerrar la sesión de RR.HH. ---
def cerrar_sesion_rrhh(root, parent_window):
    """
    Cierra la ventana de RR.HH., destruye las ventanas secundarias abiertas, 
    y llama a la función de la ventana de Login.
    """
    global lista_empleados_window, lista_candidatos_window
    
    # Destruir ventanas secundarias si están abiertas
    if lista_empleados_window and lista_empleados_window.winfo_exists():
        lista_empleados_window.destroy()
        lista_empleados_window = None
    if lista_candidatos_window and lista_candidatos_window.winfo_exists():
        lista_candidatos_window.destroy()
        lista_candidatos_window = None
        
    # Destruir la ventana de RR.HH.
    root.destroy()
    
    # LLAMADA AL LOGIN: Reutilizamos la ventana principal (parent_window)
    try:
        login.abrir_login(parent_window) 
    except AttributeError:
        messagebox.showerror("Error de Módulo", 
                             "No se pudo llamar a la función 'abrir_login' en login.py.\n"
                             "Asegúrate de que 'login.py' tiene la función 'def abrir_login(root):'.")
    except Exception as e:
         messagebox.showerror("Error", f"Ocurrió un error al llamar a login: {e}")

# --- Función Principal de la Ventana de RR.HH. ---

def abrir_rrhh(parent_window, nombre_usuario):
    if parent_window.winfo_exists():
        parent_window.withdraw() 

    root = Toplevel()
    root.title(f"Recursos Humanos - Usuario: {nombre_usuario}")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    # --- Contenedores y Botones ---
    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)
    
    # BOTÓN DE CERRAR SESIÓN 
    Button(frame_top, text="❌ Cerrar Sesión", bg="#ff4d4d", fg="white",
           font=("Arial", 12, "bold"), command=lambda: cerrar_sesion_rrhh(root, parent_window)).pack(pady=5, padx=20, fill=X)
    
    Label(frame_top, text="Módulo de Recursos Humanos (RR.HH.)", bg="#1dc1dd", fg="white",
          font=("Arial", 18, "bold")).pack(pady=10)

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

# ----------------- EJECUCIÓN -----------------
if __name__ == '__main__':
    # La ventana principal de Tkinter se crea aquí
    main_root = Tk()
    main_root.title("Simulación de Home Oculto")
    main_root.withdraw() # Oculta la ventana principal al inicio
    
    # Se simula la apertura del módulo RRHH, pasando la ventana principal oculta
    abrir_rrhh(main_root, "Gerente RRHH")
    
    main_root.mainloop()