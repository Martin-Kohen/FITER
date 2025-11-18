from tkinter import *
import subprocess
import sys
from PIL import Image, ImageTk  # Pillow para manejo de imágenes
import webbrowser

root = Tk()
root.title("Home")
root.state("zoomed")
root.configure(bg="#1dc1dd")

def abrir_login():
    root.destroy()
    subprocess.Popen(["python", "Partes/login.py"])

def abrir_home():
    root.destroy()
    subprocess.Popen(["python", "Partes/home.py"])


def abrir_instagram():
    webbrowser.open("https://www.instagram.com/somosfiter")

def abrir_facebook():
    webbrowser.open("https://www.facebook.com/SomosFiter")

def abrir_Web():
    webbrowser.open("https://fiter.com/AR")

frame = Frame(root, bg="#1dc1dd")
frame.pack(fill="both", expand=True)

if len(sys.argv) > 1:
    nombre_usuario = sys.argv[1]
    sign_up = Button(frame, width=10, text='Cerrar Sesión', border=0, bg="#0089a1", cursor='hand2', fg="#ffffff", command=abrir_home)
    sign_up.place(x=215, y=335)
else:
    sign_up = Button(frame, width=15, height=1 , text='Iniciar Sesión', border=0, bg="#03abc9", cursor='hand2', fg="#ffffff", font=("Billie DEMO Light", 15, "bold"), command=abrir_login)
    sign_up.place(relx=0.812, rely=0.06, anchor="center")

try:
    imagen_original = Image.open("imagenes/Mision.png")
    imagen_redimensionada = imagen_original.resize((450, 350), Image.Resampling.LANCZOS)  
    imagen = ImageTk.PhotoImage(imagen_redimensionada)
    label_imagen = Label(frame, image=imagen, bg="#1dc1dd")
    label_imagen.place(relx=0.5, rely=0.3, anchor="center")
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

try:
    imagen_original1 = Image.open("../imagenes/fiterLogo.png")
    imagen_redimensionada1 = imagen_original1.resize((150, 150), Image.Resampling.LANCZOS)  
    imagen1 = ImageTk.PhotoImage(imagen_redimensionada1)
    label_imagen1 = Label(frame, image=imagen1, bg="#1dc1dd")
    label_imagen1.place(relx=0.5, rely=0.05, anchor="center")
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

try:
    imagen_original2 = Image.open("../imagenes/Mision2.png")
    imagen_redimensionada2 = imagen_original2.resize((450, 350), Image.Resampling.LANCZOS)  
    imagen2 = ImageTk.PhotoImage(imagen_redimensionada2)
    label_imagen2 = Label(frame, image=imagen2, bg="#1dc1dd")
    label_imagen2.place(relx=0.5, rely=0.75, anchor="center")
except Exception as e:
    print(f"Error al cargar la imagen: {e}")


mision = Text(frame, border=0, fg="#ffffff", font=("Billie DEMO Light", 20, "bold"), bg="#1dc1dd", wrap=WORD)
mision.place(relx=0.19, rely=0.2, anchor="center", width=200, height=40)
mision.insert(END, "Misión")
mision.config(state=DISABLED)

Texto_mision = Text(frame, border=0, fg="#ffffff", font=("Billie DEMO Light", 15, "bold"), bg="#1dc1dd", wrap=WORD)
Texto_mision.place(relx=0.18, rely=0.3, anchor="center", width=500, height=150)
Texto_mision.insert(END, "En Fiter, nuestra misión es ofrecer soluciones innovadoras y eficientes que mejoren la calidad de vida de nuestros clientes, mediante productos y servicios de alta calidad, tecnología avanzada y un compromiso constante con la satisfacción y confianza de quienes confían en nosotros.")
Texto_mision.config(state=DISABLED)

software = Text(frame, border=0, fg="#ffffff", font=("Billie DEMO Light", 20, "bold"), bg="#1dc1dd", wrap=WORD)
software.place(relx=0.19, rely=0.6, anchor="center", width=300, height=40)
software.insert(END, "Nuestro Software")
software.config(state=DISABLED)

Texto_software = Text(frame, border=0, fg="#ffffff", font=("Billie DEMO Light", 15, "bold"), bg="#1dc1dd", wrap=WORD)
Texto_software.place(relx=0.18, rely=0.7, anchor="center", width=500, height=150)
Texto_software.insert(END, "El software que nosotros queremos proponer a la empresa, va a poder contar con una base de datos con la cual almacenar y manejar con mayor estabilidad toda la información con la que cuenta la empresa, desde sus sedes, el personal de cada una de las mismas, sus respectivos ingresos, el estado de las máquinas, etc.")
Texto_software.config(state=DISABLED)

# Botones redes sociales
btn_instagram = Button(frame, text="Instagram", bg="#fe0f73", fg="white", cursor="hand2", border=0, font=("Billie DEMO Light", 15, "bold"), command=abrir_instagram)
btn_instagram.place(relx=0.74, rely=0.2, anchor="n")

btn_facebook = Button(frame, text="Facebook", bg="#3b5998", fg="white", cursor="hand2", border=0, font=("Billie DEMO Light", 15, "bold"), command=abrir_facebook)
btn_facebook.place(relx=0.812, rely=0.2, anchor="n")

btn_twitter = Button(frame, text="Nuestra Web", bg="#1DA1F2", fg="white", cursor="hand2", border=0, font=("Billie DEMO Light", 15, "bold"), command=abrir_Web)
btn_twitter.place(relx=0.89, rely=0.2, anchor="n")

# Mini FAQ
faq_title = Label(frame, text="Preguntas Frecuentes", fg="white", bg="#1dc1dd", font=("Billie DEMO Light", 16, "bold"))
faq_title.place(relx=0.81, rely=0.497, anchor="n")

# Datos FAQ: pregunta y respuesta
faq_data = [
    ("¿Cómo puedo registrarme?", "Puedes registrarte haciendo clic en el botón 'Registrarse' en la parte superior derecha."),
    ("¿Cuáles son los métodos de pago?", "Aceptamos tarjetas de crédito, débito y pagos a través de plataformas digitales."),
    ("¿Puedo cancelar mi suscripción?", "Sí, puedes cancelar tu suscripción en cualquier momento desde tu perfil."),
]

# Para guardar las etiquetas de respuestas y el estado visible/no visible
faq_labels = []
faq_visible = [False]*len(faq_data)

def toggle_faq(index):
    if faq_visible[index]:
        faq_labels[index].place_forget()
        faq_visible[index] = False
    else:
        faq_labels[index].place(relx=0.77, rely=0.56 + index*0.09, anchor="nw")
        faq_visible[index] = True

# Crear preguntas y respuestas (ocultas inicialmente)
for i, (pregunta, respuesta) in enumerate(faq_data):
    btn = Button(frame, text=pregunta, bg="#03abc9", fg="white", cursor="hand2", border=0,
                 font=("Billie DEMO Light", 12, "bold"), command=lambda i=i: toggle_faq(i))
    btn.place(relx=0.75, rely=0.53 + i*0.09, anchor="nw", width=300)

    lbl = Label(frame, text=respuesta, bg="#1dc1dd", fg="white", font=("Billie DEMO Light", 11, "bold"), wraplength=300, justify="left")  # <- aquí está el bold aplicado
    faq_labels.append(lbl)

root.mainloop()
