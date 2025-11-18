from tkinter import *
from tkinter import messagebox
import mysql.connector

# Función para abrir la ventana de Servicio al Cliente
def abrir_servicio_cliente(parent_window, nombre_usuario):
    # Oculta el home temporalmente
    parent_window.withdraw()

    root = Toplevel()  # Nueva ventana encima del home
    root.title("Servicio al Cliente")
    root.state("zoomed")
    root.configure(bg="#1dc1dd")

    # --- Contenedores ---
    frame_clientes = Frame(root, bg="#1dc1dd")
    frame_clientes.pack(pady=10, fill=X)

    frame_tickets = Frame(root, bg="#1dc1dd")
    frame_tickets.pack(pady=10, fill=BOTH, expand=True)

    # --- Función para volver al home ---
    def volver_home():
        root.destroy()
        parent_window.deiconify()       
        parent_window.state("zoomed")   

    Button(frame_clientes, text="← Volver al Home", bg="#ff4d4d", fg="white",
           font=("Arial", 12, "bold"), command=volver_home).pack(pady=5, padx=20, fill=X)

    # --- Conectar y mostrar clientes ---
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre FROM clientes")
        clientes = cursor.fetchall()
        conn.close()

        if clientes:
            Label(frame_clientes, text="Clientes registrados:", bg="#1dc1dd", fg="white",
                  font=("Arial", 16, "bold")).pack(pady=5)

            for cli in clientes:
                Button(frame_clientes, text=f"{cli[1]}", bg="#ffffff", fg="black", font=("Arial", 12),
                       command=lambda id_c=cli[0], nombre_c=cli[1]: mostrar_tickets(id_c, nombre_c, frame_tickets)).pack(fill=X, padx=20, pady=2)
        else:
            Label(frame_clientes, text="No hay clientes registrados", bg="#1dc1dd", fg="black", font=("Arial", 12)).pack(pady=20)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")

    root.mainloop()


# --- Función para mostrar tickets de un cliente ---
def mostrar_tickets(id_cliente, nombre_cliente, frame_tickets):
    # Limpiar widgets anteriores
    for widget in frame_tickets.winfo_children():
        widget.destroy()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id_ticket, asunto, estado, fecha_apertura FROM tickets WHERE id_cliente = %s", (id_cliente,))
        tickets = cursor.fetchall()
        conn.close()

        if tickets:
            Label(frame_tickets, text=f"Tickets de {nombre_cliente}:", bg="#1dc1dd",
                  fg="white", font=("Arial", 14, "bold")).pack(pady=5)

            for t in tickets:
                frame_ticket = Frame(frame_tickets, bg="#1dc1dd")
                frame_ticket.pack(fill=X, pady=2, padx=20)

                Label(frame_ticket, text=f"Asunto: {t[1]} | Estado: {t[2]} | Fecha: {t[3]}", bg="#1dc1dd",
                      fg="white", font=("Arial", 12, "bold")).pack(side=LEFT)

                # Botón para ver interacciones
                Button(frame_ticket, text="Ver Interacciones", bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                       command=lambda id_t=t[0]: mostrar_interacciones(id_t)).pack(side=LEFT, padx=10)

                # Botón para ver encuesta
                Button(frame_ticket, text="Ver Encuesta", bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                       command=lambda id_t=t[0]: mostrar_encuesta(id_t)).pack(side=LEFT, padx=10)

        else:
            Label(frame_tickets, text="No hay tickets para este cliente", bg="#1dc1dd", fg="black", font=("Arial", 12)).pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")


# --- Función para mostrar interacciones de un ticket ---
def mostrar_interacciones(id_ticket):
    top = Toplevel()
    top.title(f"Interacciones del ticket {id_ticket}")
    top.geometry("600x400")
    top.configure(bg="#1dc1dd")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT fecha_hora, tipo_interaccion, detalles FROM interacciones WHERE id_ticket = %s", (id_ticket,))
        interacciones = cursor.fetchall()
        conn.close()

        if interacciones:
            for inter in interacciones:
                Label(top, text=f"{inter[0]} | {inter[1]}: {inter[2]}", bg="#ffffff", fg="black",
                      font=("Arial", 11), anchor="w", justify=LEFT, wraplength=550).pack(fill=X, padx=10, pady=2)
        else:
            Label(top, text="No hay interacciones para este ticket", bg="#ffffff", fg="black",
                  font=("Arial", 12)).pack(fill=X, padx=10, pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")


# --- Función para mostrar encuesta de un ticket ---
def mostrar_encuesta(id_ticket):
    top = Toplevel()
    top.title(f"Encuesta del ticket {id_ticket}")
    top.geometry("500x300")
    top.configure(bg="#1dc1dd")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fiter"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT calificacion, comentarios, fecha_realizacion FROM encuestas WHERE id_ticket = %s", (id_ticket,))
        encuesta = cursor.fetchone()
        conn.close()

        if encuesta:
            Label(top, text=f"Calificación: {encuesta[0]}/5", bg="#ffffff", fg="black",
                  font=("Arial", 12)).pack(fill=X, padx=10, pady=5)
            Label(top, text=f"Comentarios: {encuesta[1]}", bg="#ffffff", fg="black",
                  font=("Arial", 12), wraplength=480, justify=LEFT).pack(fill=X, padx=10, pady=5)
            Label(top, text=f"Fecha: {encuesta[2]}", bg="#ffffff", fg="black",
                  font=("Arial", 12)).pack(fill=X, padx=10, pady=5)
        else:
            Label(top, text="No hay encuesta para este ticket", bg="#ffffff", fg="black",
                  font=("Arial", 12)).pack(fill=X, padx=10, pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la BD: {err}")