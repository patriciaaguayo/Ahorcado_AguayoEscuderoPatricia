import mysql.connector

class Conexion:
    def __init__(self, host="127.0.0.1", user="root", passwd="", database="ahorcado", port="3307"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.port = port

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


# Conexion a la base de datos:

conexion = Conexion()
conexion_db = conexion.conectar()
if conexion_db:
    print("\n Conectado a la base de datos")
