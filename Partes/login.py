from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import hashlib

# --- Función para hashear la contraseña ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Función para crear entradas con placeholder ---
def crear_entry(frame, placeholder, y, show=None):
    entry = Entry(frame, width=35, fg='black', border=0, bg='white',
                  font=('Billie DEMO Light', 11), show=show)
    entry.place(x=30, y=y)
    entry.insert(0, placeholder)

    def on_enter(e):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            if placeholder == "Contraseña":
                entry.config(show="*")

    def on_leave(e):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Contraseña":
                entry.config(show="")

    entry.bind("<FocusIn>", on_enter)
    entry.bind("<FocusOut>", on_leave)
    return entry


# =======================================================
# 🔑 FUNCIÓN PRINCIPAL DE LOGIN (Expuesta para otros módulos)
# =======================================================
def abrir_login(root):
    """
    Función que inicia la interfaz de login. Es llamada por:
    1. El bloque __main__ de este archivo (al inicio).
    2. Otros módulos (como RR.HH.) al cerrar sesión.
    """
    
    # Si la ventana principal estaba oculta (por otro módulo), la volvemos a mostrar
    if not root.winfo_ismapped():
        root.deiconify() 
    
    # Limpiar cualquier widget anterior (útil al regresar de RR.HH.)
    for widget in root.winfo_children():
        widget.destroy()

    root.title('Login')
    root.geometry('1200x500+300+200')
    root.configure(bg="#1dc1dd")
    root.resizable(False, False)

    # --- Función interna de inicio de sesión (CORREGIDA) ---
    def signin():
        correo = user.get().strip()
        contrasena = code.get()

        if correo in ("", "Correo Electronico") or contrasena in ("", "Contraseña"):
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        db = None
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="fiter"
            )
            cursor = db.cursor()
            
            # CONSULTA MODIFICADA: Ahora se selecciona 'id_departamento'
            sql_query = "SELECT idUsuario, Nombre, Contrasenia, Rol, id_departamento FROM usuario WHERE Mail = %s"
            cursor.execute(sql_query, (correo,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "El usuario no existe.")
                return

            # DESEMPAQUETADO MODIFICADO: Se incluye la nueva columna
            user_id, nombre_usuario, contrasenia_bd, rol, id_departamento = result

            if hash_password(contrasena) == contrasenia_bd:
                # Marcar como logueado
                cursor.execute("UPDATE usuario SET logueado = 1 WHERE idUsuario = %s", (user_id,))
                db.commit()

                messagebox.showinfo("Éxito", f"Bienvenido {nombre_usuario}! Rol: {rol} (Depto ID: {id_departamento})")
                root.destroy() # Cierra la ventana principal

                # -----------------------------------------------------------------
                # LÓGICA DE REDIRECCIÓN BASADA EN ROL Y ID_DEPARTAMENTO
                # -----------------------------------------------------------------
                
                # 1. Gerente (Excepción por Rol)
                if rol == "Gerente":
                    subprocess.Popen(["python", "home_gerente.py", nombre_usuario])
                
                # 2. RRHH (id_departamento == 2)
                elif id_departamento == 2:
                    subprocess.Popen(["python", "rrhh_empleado.py", nombre_usuario])
                
                # 3. Otros Departamentos (id_departamento != 2 y no Gerente)
                elif id_departamento is not None:
                    subprocess.Popen(["python", "home.py", nombre_usuario])
                
                # 4. Fallback (si el usuario no tiene departamento o es un rol no manejado)
                else:
                    messagebox.showerror("Error de Asignación", 
                                         f"El usuario tiene un rol ({rol}) o departamento ({id_departamento}) sin ventana de inicio asignada.")
                
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    # --- Interfaz ---
    frame = Frame(root, width=500, height=500, bg="#1dc1dd")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Iniciar sesión', fg='white', bg='#1dc1dd',
                    font=('Billie DEMO Light', 23, 'bold'))
    heading.place(x=87, y=5)

    global user, code
    user = crear_entry(frame, "Correo Electronico", 60)
    code = crear_entry(frame, "Contraseña", 120, show="")

    def abrir_registro():
        root.destroy()
        subprocess.Popen(["python", "registro.py"])

    label = Label(frame, text="¿No tenés cuenta?", fg='white', bg="#1dc1dd",
                  font=('Billie DEMO Light', 11, 'bold'))
    label.place(x=75, y=180)

    sign_up = Button(frame, width=10, text='Registrarse', border=0, bg="#0089a1",
                     cursor='hand2', fg="#ffffff", command=abrir_registro)
    sign_up.place(x=215, y=180)

    enter = Button(frame, width=10, text='Entrar', border=0, bg="#0089a1",
                   cursor='hand2', fg="#ffffff", command=signin)
    enter.place(x=130, y=220)


# =======================================================
# 🚀 EJECUCIÓN DEL MÓDULO (Para abrir login cuando ejecutas login.py)
# =======================================================
if __name__ == '__main__':
    main_root = Tk()
    abrir_login(main_root)
    main_root.mainloop()