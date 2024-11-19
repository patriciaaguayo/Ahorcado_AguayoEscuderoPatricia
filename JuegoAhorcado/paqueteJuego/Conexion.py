import mysql.connector

class Conexion:
    def __init__(self, host="127.0.0.1", user="root", passwd="", database="ahorcado", port="3307"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.port = port
        self.users = []

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                port=self.port
            )
            return self.conexion
        except mysql.connector.Error as err:
            print("\n Error al conectar: {}".format(err))
            return None

    def cerrar_conexion(self):
        if 'conexion' in locals() and self.conexion.is_connected():
            self.conexion.close()
            print("\n Conexión cerrada")


    def buscarUsuario(self):
        try:
            if self.conexion.is_connected():
                cursor = self.conexion.cursor()
                cursor.execute("SELECT nombre FROM usuarios")
                usuarios_db = cursor.fetchall()

                # Guardar resultados como una lista de cadenas
                self.users = [usuario[0] for usuario in usuarios_db]
                cursor.close()
            else:
                print("\n La conexión no está activa.")
        except mysql.connector.Error as err:
            print(f"\n Error al buscar usuarios: {err}")

# Conexion a la base de datos:

conexion = Conexion()
conexion_db = conexion.conectar()
if conexion_db:
    print("\n Conectado a la base de datos")
