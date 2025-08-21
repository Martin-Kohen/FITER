from tkinter import *
import subprocess
from tkinter import messagebox

root=Tk()
root.title('Registro')
root.geometry('1200x500+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False,False)

def signin():
    CorreoElectronico=user.get()
    FechadeNacimiento=date.get()
    Contraseña=code.get()
    Nombre=nombre.get()
    Apellido=apellido.get()


img = PhotoImage(file='../imagenes/fiterLogo.png')
Label(root, image= img, bg= "#1dc1dd").place (x=50, y=50)

frame = Frame(root, width=500, height= 500, bg ="#1dc1dd")
frame.place(x=480, y=70)

heading = Label(frame,text='Registrarse',fg='white', bg= "#1dc1dd",font=('Billie DEMO Light',23,'bold'))
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
    nombre.delete(0, 'end')
    
def on_leave(e):
    name=nombre.get()
    if name=='':
        nombre.insert(0,'Nombre')
nombre = Entry(frame,width=35,fg='black',border=0,bg='white',font=('Billie DEMO Light',11))
nombre.place(x=30,y=120)
nombre.insert(0,'Nombre')
nombre.bind('<FocusIn>', on_enter)
nombre.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=147)

def on_enter(e):
    apellido.delete(0, 'end')
    
def on_leave(e):
    name=apellido.get()
    if name=='':
        apellido.insert(0,'Apellido')
apellido = Entry(frame,width=35,fg='black',border=0,bg='white',font=('Billie DEMO Light',11))
apellido.place(x=30,y=180)
apellido.insert(0,'Apellido')
apellido.bind('<FocusIn>', on_enter)
apellido.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=207)

def on_enter(e):
    date.delete(0, 'end')
    
def on_leave(e):
    name=date.get()
    if name=='':
        date.insert(0,'Fecha de Nacimiento')
date = Entry(frame,width=35,fg='black',border=0,bg='white',font=('Billie DEMO Light',11))
date.place(x=30,y=240)
date.insert(0,'Fecha de Nacimiento')
date.bind('<FocusIn>', on_enter)
date.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=267)


def on_enter(e):
    code.delete(0, 'end')
    
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Contraseña')
code = Entry(frame,width=35,fg='black',border=0,bg='white',font=('Billie DEMO Light',11))
code.place(x=30,y=300)
code.insert(0,'Contraseña')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=327)

def abrir_login():
    root.destroy() 
    subprocess.Popen(["python", "login.py"])

label = Label(frame,text="¿Tenes cuenta?",fg='white',bg="#1dc1dd",font=('Billie DEMO Light',11,'bold'))
label.place(x=75,y=335)
sign_up= Button(frame,width=10,text='Iniciar Sesion', border=0,bg="#0089a1",cursor='hand2',fg="#ffffff", command=abrir_login)
sign_up.place(x=215,y=335)
enter= Button(frame,width=10,text='Entrar', border=0,bg="#0089a1",cursor='hand2',fg="#ffffff")
enter.place(x=130,y=370)
root.mainloop()