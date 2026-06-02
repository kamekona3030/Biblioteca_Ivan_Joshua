import sqlite3
URL = "bd/biblioteca.db"

def getConexion():

    """Establece y devuelve la conexión con la base de datos """
    try:
        return sqlite3.connect(URL)
    except sqlite3.OperationalError:
        print("Error al conectarse")
        raise