import tkinter as tk
from tkinter import messagebox, font
import random

# Clase para manejar el juego del Ahorcado
class Ahorcado:
    def __init__(self):
        self.palabra = ""
        self.palabra_guiones = []
        self.letras_incorrectas = set()
        self.intentos_restantes = 6
        self.ganadas = 0
        self.perdidas = 0

        # Crear ventana principal
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Ahorcado")
        self.ventana_principal.geometry("1200x1000")
        self.ventana_principal.configure(bg="#E2D8FE")

        # Título
        tk.Label(
            self.ventana_principal,
            text="Juego del Ahorcado",
            font=("Courier", 24),
            bg="#E2D8FE"
        ).place(x=500, y=150)

        # Botones para jugar y salir
        tk.Button(
            self.ventana_principal,
            text="Jugar",
            font=("Courier", 16),
            padx=20,
            pady=10,
            width= 10,
            bg="#90d5fe",
            command=self.abrir_juego
        ).place(x=500, y=700)

        tk.Button(
            self.ventana_principal,
            text="Salir",
            font=("Courier", 16),
            padx=20,
            pady=10,
            bg="#FFB6C1",
            command=self.ventana_principal.quit
        ).place(x=500, y=800)

        # Crear la ventana del juego (pero mantenerla oculta al inicio)
        self.ventana_juego = tk.Toplevel(self.ventana_principal)
        self.ventana_juego.title("Ahorcado - Juego")
        self.ventana_juego.geometry("800x600")
        self.ventana_juego.configure(bg="#90d5fe")
        self.ventana_juego.withdraw()  # Ocultar la ventana

        # Widgets de la ventana del juego
        self.label_palabra = tk.Label(self.ventana_juego, text="", font=("Courier", 24), bg="#90d5fe")
        self.label_palabra.pack(pady=20)

        self.nombre = tk.Label(self.ventana_juego, text="Introduce tu nombre:", font=("Courier", 16), bg="#90d5fe")
        self.nombre.pack(pady=10)

        self.entry_nombre = tk.Entry(self.ventana_juego, font=("Courier", 16), bg="#E2D8FE")
        self.entry_nombre.pack(pady=10)

        tk.Label(self.ventana_juego, text="Selecciona un tema:", font=("Courier", 16), bg="#90d5fe").pack()
        self.Tipos = tk.StringVar(value="Personas")
        fuente_personalizada = font.Font(family="Courier New", size=14, weight="bold")

        # Crear OptionMenu con fuente personalizada
        menu_temas = tk.OptionMenu(self.ventana_juego, self.Tipos, "Personas", "Frutas", "Informatico")
        menu_temas.pack(pady=10)

        # Aplicar la fuente personalizada al menú
        menu_temas.config(font=fuente_personalizada)



        self.label_intentos = tk.Label(self.ventana_juego, text="Intentos restantes: 6", font=("Courier", 16), bg="#90d5fe")
        self.label_intentos.pack(pady=10)

        self.label_incorrectas = tk.Label(self.ventana_juego, text="Letras incorrectas: ", font=("Courier", 16), bg="#90d5fe")
        self.label_incorrectas.pack(pady=10)

        self.entry_letra = tk.Entry(self.ventana_juego, font=("Courier", 16), state=tk.DISABLED)
        self.entry_letra.pack(pady=10)

        tk.Button(
            self.ventana_juego,
            text="Adivinar Letra",
            font=("Courier", 16),
            padx=10,
            pady=5,
            bg="#ffffcb",
            command=self.adivinar_letra
        ).pack(pady=10)

        tk.Button(
            self.ventana_juego,
            text="Volver al Menú Principal",
            font=("Courier", 16),
            padx=10,
            pady=5,
            bg="#FFB6C1",
            command=self.volver_menu
        ).pack(pady=10)

    def abrir_juego(self):
        """Inicia el juego mostrando la ventana del juego y ocultando la principal."""
        self.ventana_principal.withdraw()
        self.ventana_juego.deiconify()
        self.comenzar_juego()

    def volver_menu(self):
        """Vuelve al menú principal desde la ventana del juego."""
        self.ventana_juego.withdraw()
        self.ventana_principal.deiconify()

    def comenzar_juego(self):
        """Inicializa una nueva partida."""
        # Selección de palabra aleatoria (puedes conectarla a una base de datos o lista)
        palabras = ["python", "ahorcado", "programacion", "juego", "desarrollo"]
        self.palabra = random.choice(palabras)
        self.palabra_guiones = ["_"] * len(self.palabra)
        self.letras_incorrectas = set()
        self.intentos_restantes = 6

        # Actualizar interfaz
        self.label_palabra.config(text=" ".join(self.palabra_guiones))
        self.label_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")
        self.label_incorrectas.config(text="Letras incorrectas: ")
        self.entry_letra.config(state=tk.NORMAL)

    def adivinar_letra(self):
        """Maneja la lógica de adivinar letras."""
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)  # Limpia el campo de entrada

        if len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Advertencia", "Por favor, introduce solo una letra.")
            return

        if letra in self.letras_incorrectas or letra in self.palabra_guiones:
            messagebox.showwarning("Advertencia", "Ya has intentado esa letra. Intenta con otra.")
            return

        if letra in self.palabra:
            for i, l in enumerate(self.palabra):
                if l == letra:
                    self.palabra_guiones[i] = letra
            self.label_palabra.config(text=" ".join(self.palabra_guiones))
            if "_" not in self.palabra_guiones:
                messagebox.showinfo("¡Felicidades!", f"¡Ganaste! La palabra era: {self.palabra}")
                self.comenzar_juego()
        else:
            self.intentos_restantes -= 1
            self.letras_incorrectas.add(letra)
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")
            self.label_incorrectas.config(text=f"Letras incorrectas: {' '.join(self.letras_incorrectas)}")
            if self.intentos_restantes == 0:
                messagebox.showinfo("Fin del juego", f"Perdiste. La palabra era: {self.palabra}")
                self.comenzar_juego()

    def run(self):
        """Ejecuta la aplicación."""
        self.ventana_principal.mainloop()


# Iniciar el juego
game = Ahorcado()
game.run()
