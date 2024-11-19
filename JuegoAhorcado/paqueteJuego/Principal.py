import tkinter as tk
from tkinter import messagebox as mb

def seleccionar_tematica():
    seleccion = tematica_seleccionada.get()
    mb.showinfo("Selección", f"Has seleccionado la temática: {seleccion}")

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


"""
imagen = tk.PhotoImage(file="../Resources/Vida7.png")
imagenLabel = tk.Label(principal, image=imagen, bg=principal.cget("bg"))
imagenLabel.place(x=400, y=200)
"""

# Variable para rastrear la selección

tematica_seleccionada = tk.StringVar(value="")

# Opciones de temáticas

tematicas = ["Personas", "Frutas", "Conceptos Informáticos"]
x_pos = 240
y_pos = 300

for i, tematica in enumerate(tematicas):
    boton = tk.Radiobutton(
        principal,
        text=tematica,
        variable=tematica_seleccionada,
        value=tematica,
        font=("Courier New", 20),
        bg="#d9beff",
        activebackground="#d9beff",
        command=seleccionar_tematica,
    )
    boton.place(x=x_pos + i * 200, y=y_pos)


Nombre = tk.Label(principal, text="Ingrese su nombre: ", font=("Courier New", 20), bg="#d9beff")
Nombre.place(x=300, y=450)


Entrada = tk.Entry(principal, font=("Courier New", 20), bg="white")
Entrada.place(x=650, y=450)

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
