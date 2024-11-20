import tkinter as tk
from tkinter import messagebox as mb
from PIL import Image, ImageTk

def abrir_ventana_juego():

    # Ocultar ventana principal
    principal.withdraw()

    # Crear ventana del juego

    juego = tk.Toplevel();
    juego.title("Juego de Ahorcado")
    juego.geometry("1200x1000")
    juego.configure(bg="#d9beff")
    juego.resizable(False, False)

    # Mostrar ventana del juego

    Nombre = tk.Label(juego, text="Ingrese su nombre: ", font=("Courier New", 20), bg="#d9beff")
    Nombre.place(x=300, y=450)


    Entrada = tk.Entry(juego, font=("Courier New", 20), bg="white")
    Entrada.place(x=650, y=450)


    imagen = tk.PhotoImage(file="../Resources/Vida6.png")
    imagenLabel = tk.Label(juego, image=imagen, bg=juego.cget("bg"))
    imagenLabel.place(x=500, y=300)

    Volver = tk.Button(
        juego,
        text="Volver",
        font=("Courier New", 24),
        bg="#ffccbe",
        width=10,
        command=lambda : volver(juego)
    )

    Volver.place(
        relx = 0.05,
        rely = 0.05,
        anchor = "nw"
    )

# ventana principal


# Función para regresar a la ventana principal

def volver(juego):
    # Cierra la ventana secundaria
    juego.destroy()
    # Muestra la ventana principal
    principal.deiconify()

principal = tk.Tk()
principal.title("AHORCADO")
principal.geometry("1200x1000")
principal.configure(bg="#d9beff")
principal.resizable(False, False)



Titulo = tk.Label(principal, text="AHORCADO", font=("Courier New", 28), bg="#d9beff")
Titulo.place(x=510, y=150)


imagen = tk.PhotoImage(file="../Resources/Logo.png")
imagenLabel = tk.Label(principal, image=imagen, bg=principal.cget("bg"))
imagenLabel.place(x=500, y=300)


BotonJugar = tk.Button(
    principal,
    text="Jugar",
    font=("Courier New", 24),
    bg="#e4ffbe", width=10,
    command=abrir_ventana_juego
)

BotonJugar.place(
    x=500,
    y=650
)

BotonSalir = tk.Button(
    principal,
    text="Salir",
    font=("Courier New", 24),
    bg="#ffccbe", width=10,
    command=principal.quit
)

BotonSalir.place(
    x=500,
    y=800
)

principal.mainloop()
