import tkinter as tk
from tkinter import messagebox as mb

# ventana principal

principal = tk.Tk()
principal.title("AHORCADO")
principal.geometry("1200x1000")
principal.configure(bg="#d9beff")
principal.resizable(False, False)



Titulo = tk.Label(principal, text="AHORCADO", font=("Courier New", 28), bg="#d9beff")
Titulo.place(x=510, y=100)


"""
imagen = tk.PhotoImage(file="../Resources/Vida7.png")
imagenLabel = tk.Label(principal, image=imagen, bg=principal.cget("bg"))
imagenLabel.place(x=400, y=200)
"""

BotonSalir = tk.Button(principal, text="Salir", font=("Courier New", 24), bg="white", command=principal.quit)
BotonSalir.place(x=550, y=600)

principal.mainloop()
