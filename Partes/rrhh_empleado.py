from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from datetime import date
import re 
from tkcalendar import DateEntry 
try:
    import login 
except ImportError:
    messagebox.showerror("Error de Importación", "No se encontró el archivo 'login.py'. Asegúrate de que esté en la misma carpeta.")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "", 
    "database": "fiter"
}

lista_empleados_window = None 
lista_candidatos_window = None

def conectar_bd():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {err}")
        return None

def obtener_departamentos(excluir_direccion=False):
    conn = conectar_bd()
    if not conn: 
        return []
    cursor = conn.cursor()
    
    departamentos = []
    try:
        sql_select = "SELECT Nombre FROM Departamentos"
        
        if excluir_direccion:
            sql_select += " WHERE Nombre != 'Dirección'" 
            
        sql_select += " ORDER BY Nombre"
        
        cursor.execute(sql_select)
        departamentos = [row[0] for row in cursor.fetchall()] 
    except mysql.connector.Error as err:
        messagebox.showerror("Error de BD", f"Error al consultar departamentos: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
    return departamentos

def parse_descripcion(descripcion):
    puesto_match = re.search(r"Puesto: (.*?) en Área: (.*?)\.", descripcion)
    puesto = puesto_match.group(1).strip() if puesto_match else "N/A"
    area = puesto_match.group(2).strip() if puesto_match else "N/A" 
    
    usuario_match = re.search(r"Usuario: (.*?) (.*?)$", descripcion)
    nombre = usuario_match.group(1).strip() if usuario_match else "N/A"
    apellido = usuario_match.group(2).strip() if usuario_match else "N/A"
    
    return nombre, apellido, puesto, area 

def aprobar_propuesta_reclutamiento(id_reclutamiento, parent_window):
    if id_reclutamiento is None: return
    conn = conectar_bd()
    if not conn: return
    cursor = conn.cursor() 

    try:
        sql_select = "SELECT Descripcion_Puesto, Estado_Proceso FROM Reclutamiento WHERE ID_Reclutamiento = %s"
        cursor.execute(sql_select, (id_reclutamiento,))
        propuesta_tuple = cursor.fetchone() 
        if not propuesta_tuple:
            messagebox.showwarning("Error", f"No se encontró la propuesta con ID {id_reclutamiento}.")
            return
            
        descripcion_puesto, estado_proceso = propuesta_tuple
        if estado_proceso != 'Pendiente RRHH':
            messagebox.showwarning("Advertencia", "Esta propuesta ya fue procesada o no está pendiente de aprobación.")
            return

        nombre, apellido, puesto, area = parse_descripcion(descripcion_puesto)
        salario_str = simpledialog.askstring("Salario", f"Ingrese el Salario (€/$) para {nombre} {apellido}:", parent=parent_window)
        if not salario_str: return

        try:
            salario = float(salario_str)
            if salario <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Salario inválido. Debe ser un número positivo.")
            return

        fecha_contratacion = date.today().strftime("%Y-%m-%d")
        sql_insert_rrhh = """INSERT INTO Empleados_RRHH (Nombre, Apellido, Puesto, Departamento, Fecha_Contratacion) 
                              VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert_rrhh, (nombre, apellido, puesto, area, fecha_contratacion))
        nuevo_id_empleado = cursor.lastrowid 

        sql_update_reclutamiento = """UPDATE Reclutamiento 
                                      SET Estado_Proceso = %s, Salario_Ofrecido = %s, Fecha_Cierre = %s, ID_Empleado = %s
                                      WHERE ID_Reclutamiento = %s"""
        estado_cierre = "Aprobado y Contratado"
        cursor.execute(sql_update_reclutamiento, (estado_cierre, salario, fecha_contratacion, nuevo_id_empleado, id_reclutamiento))

        sql_insert_contratacion = """INSERT INTO Contratacion (ID_Empleado, Salario, Tipo_Contrato, Fecha_Contrato) 
                                      VALUES (%s, %s, %s, %s)"""
        tipo_contrato = "Fijo" 
        cursor.execute(sql_insert_contratacion, (nuevo_id_empleado, salario, tipo_contrato, fecha_contratacion))

        conn.commit()
        messagebox.showinfo("Éxito", f"¡Propuesta Aprobada! {nombre} {apellido} ha sido contratado.\nID Empleado: {nuevo_id_empleado}")
        
        if lista_candidatos_window and lista_candidatos_window.winfo_exists():
            lista_candidatos_window.destroy()
            ver_posibles_candidatos()

    except mysql.connector.Error as err:
        conn.rollback() 
        messagebox.showerror("Error de BD", f"Error durante la aprobación/inserción: {err}")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def denegar_propuesta_reclutamiento(id_reclutamiento):
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
            
def solicitar_datos_alta(parent_window, callback):
    opciones_departamento_empleado = obtener_departamentos(excluir_direccion=True) 
    if not opciones_departamento_empleado and 'Dirección' not in obtener_departamentos(excluir_direccion=False):
        messagebox.showwarning("Advertencia", "No se pudo cargar la lista de departamentos o falta 'Dirección'. Asegúrate de que la tabla exista y tenga datos.")

    top = Toplevel(parent_window)
    top.title("Alta Empleado Manual")
    top.geometry("400x650") 
    top.resizable(False, False)
    top.transient(parent_window)
    top.grab_set()

    nombre_var = StringVar()
    apellido_var = StringVar()
    puesto_var = StringVar(value='Empleado') 
    valor_inicial_depto = opciones_departamento_empleado[0] if opciones_departamento_empleado else "N/A"
    departamento_var = StringVar(value=valor_inicial_depto)
    direccion_var = StringVar()
    telefono_var = StringVar()
    email_var = StringVar()
    opciones_puesto = ['Empleado', 'Gerente']

    Label(top, text="Datos del Nuevo Empleado", font=("Arial", 12, "bold")).pack(pady=10)
    
    canvas = Canvas(top)
    vsb = Scrollbar(top, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=380)
    canvas.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    vsb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=vsb.set)
    
    Frame_nombre = Frame(scrollable_frame)
    Frame_nombre.pack(pady=5, padx=20, fill=X)
    Label(Frame_nombre, text="Nombre:").pack(side=LEFT, padx=5)
    Entry(Frame_nombre, textvariable=nombre_var, width=25).pack(side=RIGHT, padx=5, fill=X, expand=True)

    Frame_apellido = Frame(scrollable_frame)
    Frame_apellido.pack(pady=5, padx=20, fill=X)
    Label(Frame_apellido, text="Apellido:").pack(side=LEFT, padx=5)
    Entry(Frame_apellido, textvariable=apellido_var, width=25).pack(side=RIGHT, padx=5, fill=X, expand=True)
    
    Frame_fecha_nacimiento = Frame(scrollable_frame)
    Frame_fecha_nacimiento.pack(pady=5, padx=20, fill=X)
    Label(Frame_fecha_nacimiento, text="F. Nacimiento:").pack(side=LEFT, padx=5)
    fecha_nacimiento_entry = DateEntry(Frame_fecha_nacimiento, selectmode='day', date_pattern='yyyy-mm-dd', width=15, borderwidth=2)
    fecha_nacimiento_entry.delete(0, 'end') 
    fecha_nacimiento_entry.pack(side=RIGHT, padx=5, fill=X, expand=True)

    Frame_direccion = Frame(scrollable_frame)
    Frame_direccion.pack(pady=5, padx=20, fill=X)
    Label(Frame_direccion, text="Dirección:").pack(side=LEFT, padx=5)
    Entry(Frame_direccion, textvariable=direccion_var, width=25).pack(side=RIGHT, padx=5, fill=X, expand=True)
    
    Frame_telefono = Frame(scrollable_frame)
    Frame_telefono.pack(pady=5, padx=20, fill=X)
    Label(Frame_telefono, text="Teléfono:").pack(side=LEFT, padx=5)
    Entry(Frame_telefono, textvariable=telefono_var, width=25).pack(side=RIGHT, padx=5, fill=X, expand=True)
    
    Frame_email = Frame(scrollable_frame)
    Frame_email.pack(pady=5, padx=20, fill=X)
    Label(Frame_email, text="Email:").pack(side=LEFT, padx=5)
    Entry(Frame_email, textvariable=email_var, width=25).pack(side=RIGHT, padx=5, fill=X, expand=True)
    
    Frame_puesto = Frame(scrollable_frame)
    Frame_puesto.pack(pady=5, padx=20, fill=X)
    Label(Frame_puesto, text="Puesto/Rol:").pack(side=LEFT, padx=5)
    puesto_menu = OptionMenu(Frame_puesto, puesto_var, *opciones_puesto)
    puesto_menu.pack(side=RIGHT, padx=5, fill=X, expand=True)

    Frame_depto = Frame(scrollable_frame)
    
    if opciones_departamento_empleado:
        depto_menu = OptionMenu(Frame_depto, departamento_var, *opciones_departamento_empleado)
    else:
        depto_menu = Entry(Frame_depto, textvariable=departamento_var, width=25)
    
    Label(Frame_depto, text="Departamento:").pack(side=LEFT, padx=5)
    depto_menu.pack(side=RIGHT, padx=5, fill=X, expand=True)
        
    Frame_fecha = Frame(scrollable_frame)
    Frame_fecha.pack(pady=5, padx=20, fill=X)
    Label(Frame_fecha, text="F. Contratación:").pack(side=LEFT, padx=5)
    fecha_contratacion_entry = DateEntry(Frame_fecha, selectmode='day', date_pattern='yyyy-mm-dd', width=15, borderwidth=2, 
                                        setdate=date.today())
    fecha_contratacion_entry.pack(side=RIGHT, padx=5, fill=X, expand=True)

    def actualizar_ui_por_puesto(*args):
        puesto_actual = puesto_var.get()
        if puesto_actual == 'Gerente':
            Frame_depto.pack_forget() 
            departamento_var.set("Dirección") 
        else:
            Frame_depto.pack(pady=5, padx=20, fill=X) 
            if departamento_var.get() == "Dirección" or departamento_var.get() == "N/A":
                departamento_var.set(opciones_departamento_empleado[0] if opciones_departamento_empleado else "N/A") 

    puesto_var.trace_add("write", actualizar_ui_por_puesto)
    actualizar_ui_por_puesto()

    def aceptar():
        nombre = nombre_var.get().strip()
        apellido = apellido_var.get().strip()
        puesto = puesto_var.get().strip()
        depto = departamento_var.get().strip()
        
        try:
            fecha_contratacion = fecha_contratacion_entry.get_date() 
        except ValueError:
            messagebox.showerror("Error de Fecha", "El campo Fecha de Contratación es obligatorio y tiene un formato incorrecto.", parent=top)
            return

        fecha_nacimiento_input = fecha_nacimiento_entry.get()
        fecha_nacimiento = None
        if fecha_nacimiento_input:
            try:
                fecha_nacimiento = fecha_nacimiento_entry.get_date()
            except Exception:
                 messagebox.showerror("Error de Fecha", "El campo Fecha de Nacimiento no tiene un formato válido (YYYY-MM-DD).", parent=top)
                 return

        direccion = direccion_var.get().strip() or None
        telefono = telefono_var.get().strip() or None
        email = email_var.get().strip() or None
        
        if not all([nombre, apellido, puesto, fecha_contratacion]):
            messagebox.showerror("Error de Validación", "Los campos Nombre, Apellido, Puesto y F. Contratación son obligatorios.", parent=top)
            return

        if puesto == 'Empleado' and (not depto or depto == "Dirección"):
              messagebox.showerror("Error de Validación", "El campo Departamento es obligatorio para empleados regulares y no puede ser 'Dirección'.", parent=top)
              return
        
        if puesto == 'Gerente' and depto != 'Dirección':
              messagebox.showerror("Error de Validación", "El puesto 'Gerente' debe asignarse al departamento 'Dirección'.", parent=top)
              return
        
        callback(nombre, apellido, puesto, depto, fecha_contratacion, fecha_nacimiento, direccion, telefono, email)
        top.destroy()

    Button(top, text="Registrar", command=aceptar, bg="#00aa00", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
    
    top.wait_window()

def alta_empleado(parent_window):
    def procesar_alta(nombre, apellido, puesto, departamento_nombre, fecha_contratacion, fecha_nacimiento, direccion, telefono, email):
        conn = conectar_bd()
        if not conn: return
        
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Empleados_RRHH 
                        (Nombre, Apellido, Departamento, Fecha_Nacimiento, Direccion, Telefono, Email, Fecha_Contratacion, Puesto) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (
                nombre, 
                apellido, 
                departamento_nombre, 
                fecha_nacimiento,
                direccion,      
                telefono,       
                email,          
                fecha_contratacion, 
                puesto
            ))
            conn.commit()
            
            nuevo_id = cursor.lastrowid
            messagebox.showinfo("Éxito", f"Empleado {nombre} {apellido} registrado con éxito.\nID Generado: {nuevo_id}\nDepartamento: {departamento_nombre}", parent=parent_window)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al insertar el empleado: {err}", parent=parent_window)
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    solicitar_datos_alta(parent_window, procesar_alta)
    
def baja_empleado(parent_window):
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
            
            sql_user = "DELETE FROM usuario WHERE idUsuario = %s"
            cursor.execute(sql_user, (id_a_borrar,))

            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Empleado y Usuario con ID {id_a_borrar} dados de baja (eliminados).")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró empleado con ID {id_a_borrar}.")
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Error de BD", f"Error al dar de baja: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            
def modificar_empleado(parent_window):
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
            conn.rollback()
            messagebox.showerror("Error de BD", f"Error al modificar: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

def ver_lista_empleados():
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

                    Label(row_frame, text=id_reclutamiento, bg="#f0f0ff", font=("Arial", 10), width=5).pack(side=LEFT, padx=5)
                    Label(row_frame, text=fecha_formateada, bg="#f0f0ff", font=("Arial", 10), width=10).pack(side=LEFT, padx=5)
                    Label(row_frame, text=descripcion, bg="#f0f0ff", fg="black",
                          font=("Arial", 10), anchor="w", width=60, wraplength=450, justify=LEFT).pack(side=LEFT, padx=5)
                    Label(row_frame, text=salario_formateado, bg="#f0f0ff", font=("Arial", 10), width=15).pack(side=LEFT, padx=5)
                    Label(row_frame, text=estado, bg="#f0f0ff", font=("Arial", 10), width=15).pack(side=LEFT, padx=5)
                    
                    frame_acciones_fila = Frame(row_frame, bg="#f0f0ff")
                    frame_acciones_fila.pack(side=LEFT, padx=5)
                    
                    if estado == 'Pendiente RRHH':
                        Button(frame_acciones_fila, text="Aprobar", bg="#00aa00", fg="white", 
                               font=("Arial", 8, "bold"), width=8, height=1,
                               command=lambda id=id_reclutamiento: aprobar_propuesta_reclutamiento(id, top)).pack(side=LEFT, padx=2, pady=1)

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


def actualizar_maestros():
    messagebox.showinfo("Actualizar Maestros",
                         "RR.HH. es el origen de los datos. La lista de Empleados está actualizada.\n"
                         "Si el módulo de Finanzas necesita la lista, debe consultarla aquí.")

def cerrar_sesion_rrhh(root, parent_window):
    global lista_empleados_window, lista_candidatos_window
    
    if lista_empleados_window and lista_empleados_window.winfo_exists():
        lista_empleados_window.destroy()
        lista_empleados_window = None
    if lista_candidatos_window and lista_candidatos_window.winfo_exists():
        lista_candidatos_window.destroy()
        lista_candidatos_window = None
        
    root.destroy()
    
    try:
        login.abrir_login(parent_window) 
    except AttributeError:
        messagebox.showerror("Error de Módulo", 
                              "No se pudo llamar a la función 'abrir_login' en login.py.\n"
                              "Asegúrate de que 'login.py' tiene la función 'def abrir_login(root):'.")
    except Exception as e:
          messagebox.showerror("Error", f"Ocurrió un error al llamar a login: {e}")


def abrir_rrhh(parent_window, nombre_usuario):
    if parent_window.winfo_exists():
        parent_window.withdraw() 

    root = Toplevel()
    root.title(f"Recursos Humanos - Usuario: {nombre_usuario}")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    frame_top = Frame(root, bg="#1dc1dd")
    frame_top.pack(pady=10, fill=X)
    
    Button(frame_top, text="❌ Cerrar Sesión", bg="#ff4d4d", fg="white",
           font=("Arial", 12, "bold"), command=lambda: cerrar_sesion_rrhh(root, parent_window)).pack(pady=5, padx=20, fill=X)
    
    Label(frame_top, text="Módulo de Recursos Humanos (RR.HH.)", bg="#1dc1dd", fg="white",
          font=("Arial", 18, "bold")).pack(pady=10)

    frame_acciones = Frame(root, bg="#1dc1dd")
    frame_acciones.pack(pady=20, fill=X)

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

if __name__ == '__main__':
    main_root = Tk()
    main_root.title("Simulación de Home Oculto")
    main_root.withdraw() 
    abrir_rrhh(main_root, "Gerente RRHH")
    
    main_root.mainloop()