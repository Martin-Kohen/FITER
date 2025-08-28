from tkinter import *
import subprocess
from tkinter import messagebox

root=Tk()
root.title('Login')
root.geometry('1200x500+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False,False)

def signin():
    correo_electronico = user.get()
    fecha_de_nacimiento = date.get()
    contraseña = code.get()
    nombre_data = nombre.get()
    apellido_data = apellido.get()

img = PhotoImage(file='../imagenes/fiterLogo.png')
Label(root, image= img, bg= "#1dc1dd").place (x=50, y=50)

frame = Frame(root, width=500, height= 500, bg ="#1dc1dd")
frame.place(x=480, y=70)

heading = Label(frame,text='Inciar sesion',fg='white', bg= "#1dc1dd",font=('Billie DEMO Light',23,'bold'))
heading.place(x=87,y=5)

def on_enter(e):
    user.delete(0, 'end')
    
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'CorreoElectronico')
user = Entry(frame, width=35 ,fg='black', border=0,bg='white',font=('Billie DEMO Light',11))
user.place(x=30, y=60)
user.insert(0,'Correo Electronico')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=87)


def on_enter(e):
    code.delete(0, 'end')
    
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Contraseña')
code = Entry(frame,width=35,fg='black',border=0,bg='white',font=('Billie DEMO Light',11))
code.place(x=30,y=120)
code.insert(0,'Contraseña')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=150)

def crear_entry(frame, placeholder, y, show=None):
    """Crea un Entry con placeholder y devuelve la referencia"""
    entry = Entry(frame, width=35, fg='black', border=0, bg='white',
                  font=('Billie DEMO Light', 11), show=show)
    entry.place(x=30, y=y)
    entry.insert(0, placeholder)

user = crear_entry(frame, "Correo Electronico", 60)
nombre = crear_entry(frame, "Nombre", 120)
apellido = crear_entry(frame, "Apellido", 180)
date = crear_entry(frame, "Fecha de Nacimiento", 240)
code = crear_entry(frame, "Contraseña", 300, show="*")


def abrir_registro():
    root.destroy() 
    subprocess.Popen(["python", "registro.py"])

label = Label(frame,text="¿No tenes cuenta?",fg='white',bg="#1dc1dd",font=('Billie DEMO Light',11,'bold'))
label.place(x=75,y=180)
sign_up= Button(frame,width=10,text='Registrarse', border=0,bg="#0089a1",cursor='hand2',fg="#ffffff",command=abrir_registro)
sign_up.place(x=215,y=180)
enter= Button(frame,width=10,text='Entrar', border=0,bg="#0089a1",cursor='hand2',fg="#ffffff")
enter.place(x=130,y=220)

root.mainloop()