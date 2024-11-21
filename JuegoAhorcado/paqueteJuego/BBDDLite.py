import sqlite3

def ver_base_datos():
    conexion = sqlite3.connect("ahorcado.db")
    cursor = conexion.cursor()

    # Mostrar las tablas disponibles
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    print("Tablas en la base de datos:")
    for tabla in tablas:
        print(tabla[0])

    # Mostrar datos de la tabla 'usuarios'
    print("\nContenido de la tabla 'usuarios':")
    cursor.execute("SELECT * FROM usuarios;")
    for fila in cursor.fetchall():
        print(fila)

    # Mostrar datos de la tabla 'tematicas'
    print("\nContenido de la tabla 'tematicas':")
    cursor.execute("SELECT * FROM tematicas;")
    for fila in cursor.fetchall():
        print(fila)

    conexion.close()

ver_base_datos()