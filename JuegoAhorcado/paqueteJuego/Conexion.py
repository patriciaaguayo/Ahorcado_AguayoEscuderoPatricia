import mysql.connector

class Conexion:
    def __init__(self, host="127.0.0.1", user="root", passwd="", database="ahorcado", port="3306"):
        self.host = host
        self.user = user
        self.password = passwd
        self.database = database
        self.port = port

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
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


    def cargarPalabras(self, tipo): # Según el tipo guardará las palabras en una lista

        db = self.conectar()
        cursor = db.cursor()
        query = "SELECT palabra FROM tematicas WHERE tipo = %s"
        cursor.execute(query, (tipo,))
        palabras = cursor.fetchall()
        db.close()
        return [palabra[0] for palabra in palabras]

    def guardarHistorial(self, usuario_id, ganadas, perdidas):

        db = self.conectar()
        cursor = db.cursor()
        query = """
        UPDATE usuarios SET Ganadas = %s, Perdidas = %s WHERE idUsuario = %s
        """
        cursor.execute(query, (ganadas, perdidas, usuario_id))
        db.commit()
        db.close()

    def obtenerUsuario(self, nombre):

        db = self.conectar()
        cursor = db.cursor()
        query = "SELECT idUsuario, Ganadas, Perdidas FROM usuarios WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        usuario = cursor.fetchone()
        db.close()
        return usuario

    def crearUsuario(self, nombre):

        db = self.conectar()
        cursor = db.cursor()
        query = "INSERT INTO usuarios (nombre, Ganadas, Perdidas) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, 0, 0))
        db.commit()
        db.close()

# Conexion a la base de datos:

conexion = Conexion()
conexion_db = conexion.conectar()
if conexion_db:
    print("\n Conectado a la base de datos")
