import tkinter as tk
from tkinter import messagebox as mb, font
import threading
import random
from paqueteJuego.Conexion import conexion

# Variables globales
palabra = ""
palabra_guiones = []
letras_incorrectas = set()
intentos_restantes = 6
usuario_id = None
ganadas = 0
perdidas = 0
nombre = ""
conexion_bd = conexion()


def jugar():
    """Inicia el juego verificando al usuario y seleccionando la palabra."""
    global nombre
    nombre = entradaNombre.get().strip()

    if not nombre:
        mb.showwarning("Advertencia", "Por favor, introduce tu nombre antes de comenzar.")
        return

    entradaLetra.config(state=tk.DISABLED)
    mb.showinfo("Cargando", "Por favor, espera mientras preparamos tu juego...")
    threading.Thread(target=procesar_jugador, args=(nombre,), daemon=True).start()


def procesar_jugador(nombre):
    """Consulta al usuario en la base de datos y configura la palabra."""
    global usuario_id, ganadas, perdidas, palabra, palabra_guiones, letras_incorrectas, intentos_restantes

    try:
        # Verificar si el usuario ya existe
        usuario = conexion_bd.obtenerUsuario(nombre)
        if not usuario:
            conexion_bd.crearUsuario(nombre)
            usuario = conexion_bd.obtenerUsuario(nombre)

        usuario_id, ganadas, perdidas = usuario

        # Elegir una palabra de la base de datos
        cargar_palabra()

        # Actualizar la interfaz gráfica en el hilo principal
        juego.after(0, actualizar_pantalla)

    except Exception as e:
        juego.after(0, lambda: mb.showerror("Error", f"Error al procesar el usuario: {e}"))


def cargar_palabra():
    """Carga una palabra según la temática seleccionada."""
    global palabra, palabra_guiones
    tipo = menu_temas.get()
    palabras = conexion_bd.cargarPalabras(tipo)
    palabra = random.choice(palabras)
    palabra_guiones = ["_"] * len(palabra)


def actualizar_pantalla():
    """Actualiza la interfaz gráfica después de cargar datos."""
    global palabra_guiones, letras_incorrectas, intentos_restantes
    palabraSecreta.config(text=" ".join(palabra_guiones))
    intentos_restantes = 6
    letras_incorrectas = set()
    intentos.config(text=f"Intentos restantes: {intentos_restantes}")
    incorrectas.config(text="Letras incorrectas: ")
    Pganadas.config(text=f"Ganadas: {ganadas}")
    Pperdidas.config(text=f"Perdidas: {perdidas}")
    entradaLetra.config(state=tk.NORMAL)


def adivinarLetra():
    """Lógica para adivinar letras en el juego."""
    global palabra, palabra_guiones, letras_incorrectas, intentos_restantes, ganadas, perdidas

    letra = entradaLetra.get().lower()
    if len(letra) != 1 or not letra.isalpha():
        mb.showwarning("Advertencia", "Por favor, introduce solo una letra válida.")
        return

    if letra in letras_incorrectas or letra in palabra_guiones:
        mb.showwarning("Advertencia", "Ya has adivinado esa letra. Intenta con otra.")
        return

    entradaLetra.delete(0, tk.END)

    if letra in palabra:
        for i in range(len(palabra)):
            if palabra[i] == letra:
                palabra_guiones[i] = letra
        palabraSecreta.config(text=" ".join(palabra_guiones))
        mb.showinfo("Bien", f"¡Bien! La letra '{letra}' está en la palabra.")
    else:
        intentos_restantes -= 1
        letras_incorrectas.add(letra)
        intentos.config(text=f"Intentos restantes: {intentos_restantes}")
        incorrectas.config(text=f"Letras incorrectas: {' '.join(letras_incorrectas)}")
        mb.showinfo("Mal", f"Lo siento, la letra '{letra}' no está en la palabra.")

    if "_" not in palabra_guiones:
        ganadas += 1
        threading.Thread(target=guardar_historial).start()
        Pganadas.config(text=f"Ganadas: {ganadas}")
        mb.showinfo("Felicidades", f"¡Felicidades! Has adivinado la palabra: {palabra}")
        entradaLetra.config(state=tk.DISABLED)
        return

    if intentos_restantes == 0:
        perdidas += 1
        threading.Thread(target=guardar_historial).start()
        Pperdidas.config(text=f"Perdidas: {perdidas}")
        mb.showinfo("Perdido", f"Perdiste. La palabra era: {palabra}")
        entradaLetra.config(state=tk.DISABLED)


def guardar_historial():
    """Guarda el historial en la base de datos en un hilo separado."""
    try:
        conexion_bd.guardarHistorial(usuario_id, ganadas, perdidas)
    except Exception as e:
        juego.after(0, lambda: mb.showerror("Error", f"Error al guardar el historial: {e}"))


def reiniciar():
    """Reinicia el juego a su estado inicial."""
    global palabra, palabra_guiones, letras_incorrectas, intentos_restantes, nombre, usuario_id, ganadas, perdidas

    entradaNombre.delete(0, tk.END)
    menu_temas.set("Personas")
    entradaLetra.delete(0, tk.END)
    entradaLetra.config(state=tk.DISABLED)
    palabra = ""
    nombre = ""
    palabra_guiones = []
    letras_incorrectas = set()
    intentos_restantes = 6
    palabraSecreta.config(text="")
    intentos.config(text="Intentos restantes: ")
    incorrectas.config(text="Letras incorrectas: ")
    Pganadas.config(text="Ganadas: 0")
    Pperdidas.config(text="Perdidas: 0")
    mb.showinfo("Reinicio", "El juego ha sido reiniciado.")


# Configuración de la ventana principal
juego = tk.Tk()
juego.title("Juego de Ahorcado")
juego.geometry("800x600")
juego.configure(bg="#90d5fe")

# Widgets principales
Titulo = tk.Label(juego, text="AHORCADO", font=("Courier New", 28), bg="#90d5fe")
Titulo.pack()

Unombre = tk.Label(juego, text="Introduce tu nombre:", font=("Courier", 16), bg="#90d5fe")
Unombre.pack()

entradaNombre = tk.Entry(juego, font=("Courier", 16))
entradaNombre.pack()

tema = tk.Label(juego, text="Selecciona un tema:", font=("Courier", 16), bg="#90d5fe")
tema.pack()

menu_temas = tk.StringVar(value="Personas")
temas_menu = tk.OptionMenu(juego, menu_temas, "Personas", "Frutas", "Informatico")
temas_menu.pack()

intentos = tk.Label(juego, text="Intentos restantes: 6", font=("Courier", 16), bg="#90d5fe")
intentos.pack()

incorrectas = tk.Label(juego, text="Letras incorrectas: ", font=("Courier", 16), bg="#90d5fe")
incorrectas.pack()

Pganadas = tk.Label(juego, text="Ganadas: 0", font=("Courier", 16), bg="#90d5fe")
Pganadas.pack()

Pperdidas = tk.Label(juego, text="Perdidas: 0", font=("Courier", 16), bg="#90d5fe")
Pperdidas.pack()

palabraSecreta = tk.Label(juego, text="", font=("Courier", 24), bg="white")
palabraSecreta.pack()

entradaLetra = tk.Entry(juego, font=("Courier", 16), state=tk.DISABLED)
entradaLetra.pack()

botonLetra = tk.Button(juego, text="Adivinar letra", font=("Courier", 16), bg="#ffccbe", command=adivinarLetra)
botonLetra.pack()

comenzar = tk.Button(juego, text="Comenzar", font=("Courier New", 24), bg="#ffccbe", command=jugar)
comenzar.pack()

BotonReiniciar = tk.Button(juego, text="Reiniciar", font=("Courier New", 24), bg="#ffccbe", command=reiniciar)
BotonReiniciar.pack()

salir = tk.Button(juego, text="Salir", font=("Courier New", 24), bg="#ffccbe", command=juego.quit)
salir.pack()

# Ejecutar la interfaz
juego.mainloop()