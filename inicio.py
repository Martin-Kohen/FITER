from tkinter import *
from tkinter import messagebox

root=Tk()
root.title('login')
root.geometry('925x500+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False,False)

def signin():
    Usuario=user.get()
    Contraseña=code.get()

    if Usuario=='admin' and Contraseña=='1234':
        screen=Toplevel(root)
        screen.title("Hola")
        screen.geometry('925x500+300+200')
        screen.config(bg="white")

        Label(screen,text="Hola", bg='#fff', font =('calibri(Body)', 50, 'bold')).pack(expand=True)

        screen.mainloop()

    elif Usuario!='admin' and Contraseña!='1234':
        messagebox.showerror("Invalido", "Usuario y contraseña invalidos")

    elif Usuario!='admin':
        messagebox.showerror("Invalido", "Usuario invalido")

    elif Contraseña!='1234':
        messagebox.showerror("Invalido", "Contraseña invalida")

img = PhotoImage(file='imagenes/fiterLogo.png')
Label(root, image= img, bg= "#1dc1dd").place (x=50, y=50)

frame = Frame(root, width=350, height= 350, bg ="#1dc1dd")
frame.place(x=480, y=70)

heading = Label(frame,text='Sign in',fg='white', bg= "#1dc1dd",font=('Billie DEMO Light',23,'bold'))
heading.place(x=120,y=5)

def on_enter(e):
    user.delete(0, 'end')
    
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Usuario')

user = Entry(frame, width=35 ,fg='black', border=0,bg='white',font=('Billie DEMO Light',11))
user.place(x=30, y=80)
user.insert(0,'Usuario')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)


Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

def on_enter(e):
    code.delete(0, 'end')
    
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Contraseña')

code = Entry(frame,width=35,fg='black',border=0,bg='white',font=('Billie DEMO Light',11))
code.place(x=30,y=150)
code.insert(0,'Contraseña')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

Button(frame,width=39,pady=7,text='Sign in',bg="#0089a1",fg='white',border=0, command=signin).place(x=35,y=204)
label = Label(frame,text="¿no tenes cuenta?",fg='white',bg="#1dc1dd",font=('Billie DEMO Light',11,'bold'))
label.place(x=75,y=270)

sign_up= Button(frame,width=10,text='Registrarse', border=0,bg="#0089a1",cursor='hand2',fg="#ffffff")
sign_up.place(x=215,y=270)

root.mainloop()