import sqlite3
from Conexion import getConexion
import os

def inicializar_bd():
    """Lee y ejecuta el archivo biblioteca.sql"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQL_FILE = os.path.join(BASE_DIR, "bd", "biblioteca.sql")
    
    conn = getConexion()
    cursor = conn.cursor()
    
    try:
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        conn.commit()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar BD: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    inicializar_bd()
