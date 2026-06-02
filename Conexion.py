import sqlite3
URL = "bd/biblioteca.db"

def getConexion():
    try:
        return sqlite3.connect(URL)
    except sqlite3.OperationalError:
        print("Error al conectarse")
        raise