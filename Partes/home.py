import sys
from tkinter import *

root = Tk()
root.title("Home")
root.state("zoomed")   
root.configure(bg="#1dc1dd")

if len(sys.argv) > 1:
    nombre_usuario = sys.argv[1]
else:
    nombre_usuario = "Usuario"

frame = Frame(root, bg="#1dc1dd")
frame.pack(fill="both", expand=True)


heading = Label(frame, text=f"Bienvenido {nombre_usuario}", fg="white", bg="#1dc1dd", font=("Billie DEMO Light", 23, "bold"))
heading.place(relx=0.5, rely=0.06, anchor="center")



root.mainloop()


