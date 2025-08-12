from tkinter import *
from tkinter import messagebox

root=Tk()
root.title('login')
root.geometry('925x500+300+200')
root.configure(bg="#1dc1dd")
root.resizable(False,False)

img = PhotoImage(file='imagenes/fiterLogo.png')
Label(root, image= img, bg= "#1dc1dd").place (x=50, y=50)

frame = Frame(root, width=350, height= 350, bg ="#1dc1dd")
frame.place(x=480, y=70)

heading = Label(frame,text='Sign in',fg='white', bg= "#1dc1dd",font=('Billie DEMO Light',23,'bold'))
heading.place(x=120,y=5)

user = Entry(frame, width=35 ,fg='black', border=0,bg='white',font=('Billie DEMO Light',11))
user.place(x=30, y=80)
user.insert(0,'username')

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

code = Entry(frame,width=35,fg='black',border=0,bg='white',font=('Billie DEMO Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

Button(frame,width=39,pady=7,text='Sign in',bg="#0089a1",fg='white',border=0).place(x=35,y=204)
label = Label(frame,text="¿no tenes cuenta?",fg='white',bg="#1dc1dd",font=('Billie DEMO Light',11,'bold'))
label.place(x=75,y=270)

sign_up= Button(frame,width=10,text='Registrarse', border=0,bg="#0089a1",cursor='hand2',fg="#ffffff")
sign_up.place(x=215,y=270)

root.mainloop()