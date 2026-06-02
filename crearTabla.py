import sqlite3
import os
from pathlib import Path

# Definir las rutas correctamente
BASE_DIR = Path(__file__).resolve().parent
RUTA_DB = BASE_DIR / "bd" / "biblioteca.db"
ARCHIVO_SQL = BASE_DIR / "bd" / "biblioteca.sql"

def inicializar_base_datos():
    # 1. Borramos la base de datos vieja para evitar conflictos de estructura
    if RUTA_DB.exists():
        os.remove(RUTA_DB)
        print("Base de datos antigua eliminada.")

    # 2. Leemos el archivo SQL
    with open(ARCHIVO_SQL, 'r', encoding='utf-8') as f:
        script_sql = f.read()

    # 3. Conectamos y ejecutamos
    with sqlite3.connect(RUTA_DB) as conexion:
        cursor = conexion.cursor()
        cursor.executescript(script_sql)
        print(f"Base de datos creada exitosamente desde {ARCHIVO_SQL}")

if __name__ == "__main__":
    inicializar_base_datos()