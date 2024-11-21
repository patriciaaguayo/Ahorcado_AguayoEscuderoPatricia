import sqlite3
import tkinter as tk
from tkinter import messagebox as mb
import random

# Función para crear la base de datos
def crear_base_datos():
    conexion = sqlite3.connect("ahorcado.db")
    cursor = conexion.cursor()

    # Crear tabla usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            Ganadas INTEGER DEFAULT 0,
            Perdidas INTEGER DEFAULT 0
        );
    """)

    # Crear tabla tematicas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tematicas (
            idPalabra INTEGER PRIMARY KEY AUTOINCREMENT,
            palabra TEXT NOT NULL,
            tipo TEXT NOT NULL
        );
    """)

    # Insertar datos en la tabla tematicas
    datos_tematicas = [
        ('carla', 'Personas'),
        ('alberto', 'Personas'),
        ('andrea', 'Personas'),
        ('mariano', 'Personas'),
        ('martin', 'Personas'),
        ('naranja', 'Frutas'),
        ('pera', 'Frutas'),
        ('manzana', 'Frutas'),
        ('uva', 'Frutas'),
        ('platano', 'Frutas'),
        ('pantalla', 'Conceptos_Informaticos'),
        ('intezfaz', 'Conceptos_Informaticos'),
        ('metodo', 'Conceptos_Informaticos'),
        ('variable', 'Conceptos_Informaticos'),
        ('clase', 'Conceptos_Informaticos'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO tematicas (palabra, tipo)
        VALUES (?, ?);
    """, datos_tematicas)

    conexion.commit()
    conexion.close()
    print("Base de datos creada exitosamente.")

# Variables globales
palabra = ""
palabra_guiones = []
letras_incorrectas = set()
intentos_restantes = 6
usuario_id = None
ganadas = 0
perdidas = 0
nombre = ""

# Conexión a la base de datos
def conectar_bd():
    return sqlite3.connect("ahorcado.db")

def obtener_usuario(nombre):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT idUsuario, Ganadas, Perdidas FROM usuarios WHERE nombre = ?", (nombre,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def crear_usuario(nombre):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, Ganadas, Perdidas) VALUES (?, 0, 0)", (nombre,))
    conn.commit()
    conn.close()

def guardar_historial(id_usuario, ganadas, perdidas):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET Ganadas = ?, Perdidas = ? WHERE idUsuario = ?",
        (ganadas, perdidas, id_usuario),
    )
    conn.commit()
    conn.close()

def cargar_palabras(tema):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT palabra FROM tematicas WHERE tipo = ?", (tema,))
    palabras = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return palabras

# Lógica del juego
def jugar():
    global nombre, usuario_id, ganadas, perdidas, palabra, palabra_guiones, letras_incorrectas, intentos_restantes

    nombre = entradaNombre.get().strip()
    if not nombre:
        mb.showwarning("Advertencia", "Por favor, introduce tu nombre antes de comenzar.")
        return

    usuario = obtener_usuario(nombre)
    if not usuario:
        crear_usuario(nombre)
        usuario = obtener_usuario(nombre)

    usuario_id, ganadas, perdidas = usuario
    tema = Tipos.get()
    palabras = cargar_palabras(tema)

    if not palabras:
        mb.showerror("Error", "No hay palabras disponibles para el tema seleccionado.")
        return

    palabra = random.choice(palabras)
    palabra_guiones = ["_"] * len(palabra)
    letras_incorrectas = set()
    intentos_restantes = 6

    actualizar_pantalla()

def actualizar_pantalla():
    palabraSecreta.config(text=" ".join(palabra_guiones))
    intentos.config(text=f"Intentos restantes: {intentos_restantes}")
    incorrectas.config(text="Letras incorrectas: ")
    Pganadas.config(text=f"Ganadas: {ganadas}")
    Pperdidas.config(text=f"Perdidas: {perdidas}")
    entradaLetra.config(state=tk.NORMAL)

def adivinar_letra():
    global palabra, palabra_guiones, letras_incorrectas, intentos_restantes, ganadas, perdidas

    letra = entradaLetra.get().lower()
    if len(letra) != 1 or not letra.isalpha():
        mb.showwarning("Advertencia", "Por favor, introduce solo una letra válida.")
        return

    if letra in letras_incorrectas or letra in palabra_guiones:
        mb.showwarning("Advertencia", "Ya has probado esa letra. Intenta con otra.")
        return

    entradaLetra.delete(0, tk.END)

    if letra in palabra:
        for i, l in enumerate(palabra):
            if l == letra:
                palabra_guiones[i] = letra
        palabraSecreta.config(text=" ".join(palabra_guiones))
    else:
        letras_incorrectas.add(letra)
        intentos_restantes -= 1
        intentos.config(text=f"Intentos restantes: {intentos_restantes}")
        incorrectas.config(text=f"Letras incorrectas: {', '.join(sorted(letras_incorrectas))}")

    if "_" not in palabra_guiones:
        mb.showinfo("Victoria", f"¡Felicidades! Has adivinado la palabra: {palabra}")
        ganadas += 1
        guardar_historial(usuario_id, ganadas, perdidas)
        reiniciar_juego()
        return

    if intentos_restantes == 0:
        mb.showinfo("Derrota", f"Perdiste. La palabra era: {palabra}")
        perdidas += 1
        guardar_historial(usuario_id, ganadas, perdidas)
        reiniciar_juego()

def reiniciar_juego():
    global palabra, palabra_guiones, letras_incorrectas, intentos_restantes
    palabra = ""
    palabra_guiones = []
    letras_incorrectas = set()
    intentos_restantes = 6
    palabraSecreta.config(text="")
    entradaLetra.config(state=tk.DISABLED)
    Pganadas.config(text=f"Ganadas: {ganadas}")
    Pperdidas.config(text=f"Perdidas: {perdidas}")
    palabraSecreta.config(text="")
    entradaNombre.config(state=tk.NORMAL)

# Configuración de la interfaz gráfica
juego = tk.Tk()
juego.title("Juego de Ahorcado")
juego.geometry("1200x800")
juego.configure(bg="#90d5fe")

Titulo = tk.Label(juego, text="AHORCADO", font=("Courier New", 28), bg="#90d5fe")
Titulo.place(x=510, y=50)

palabraSecreta = tk.Label(juego, text="", font=("Courier", 24), bg="white")
palabraSecreta.place(x=500, y=200)

Unombre = tk.Label(juego, text="Introduce tu nombre:", font=("Courier", 16), bg="#90d5fe")
Unombre.place(x=500, y=300)

entradaNombre = tk.Entry(juego, font=("Courier", 16), bg="#E2D8FE")
entradaNombre.place(x=500, y=350)

tema = tk.Label(juego, text="Selecciona un tema:", font=("Courier", 16), bg="#90d5fe")
tema.place(x=500, y=400)

Tipos = tk.StringVar(value="Personas")
menu_temas = tk.OptionMenu(juego, Tipos, "Personas", "Frutas", "Conceptos Informaticos")
menu_temas.place(x=520, y=450)
menu_temas.config(font=("Courier New", 12))

intentos = tk.Label(juego, text="Intentos restantes: ", font=("Courier", 16), bg="#90d5fe")
intentos.place(x=100, y=550)

incorrectas = tk.Label(juego, text="Letras incorrectas: ", font=("Courier", 16), bg="#90d5fe")
incorrectas.place(x=100, y=600)

Pganadas = tk.Label(juego, text="Ganadas: 0", font=("Courier", 16), bg="#90d5fe")
Pganadas.place(x=130, y=650)

Pperdidas = tk.Label(juego, text="Perdidas: 0", font=("Courier", 16), bg="#90d5fe")
Pperdidas.place(x=120, y=700)

entradaLetra = tk.Entry(juego, font=("Courier", 16), state=tk.DISABLED)
entradaLetra.place(x=495, y=550)

botonLetra = tk.Button(
    juego,
    text="Adivinar letra",
    font=("Courier", 16),
    bg="#ffccbe",
    width=15,
    height=2,
    command=adivinar_letra
)
botonLetra.place(x=505, y=600)

comenzar = tk.Button(
    juego,
    text="Comenzar",
    font=("Courier New", 24),
    bg="#ffccbe",
    width=10,
    command=jugar
)
comenzar.place(x=950, y=150)

BotonReiniciar = tk.Button(
    juego,
    text="Reiniciar",
    font=("Courier New", 24),
    bg="#ffccbe",
    width=10,
    command=reiniciar_juego
)
BotonReiniciar.place(x=950, y=50)

salir = tk.Button(
    juego,
    text="Salir",
    font=("Courier New", 24),
    bg="#ffccbe",
    width=10,
    command=juego.quit
)
salir.place(x=50, y=50)

crear_base_datos()
juego.mainloop()