import sqlite3
import unittest
from pathlib import Path


RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"


class TestBaseDatosInicial(unittest.TestCase):
    def test_biblioteca_db_existe_con_tabla_libros_vacia(self):
        self.assertTrue(RUTA_BD.exists())

        with sqlite3.connect(RUTA_BD) as conexion:
            tablas = conexion.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
            columnas = conexion.execute("PRAGMA table_info(libros)").fetchall()
            columnas_obtenidas = [info[1] for info in columnas]

        columnas_esperadas = ["id", "titulo", "autor", "disponible", "isbn", "categoria", "fecha_actualizacion"]
        self.assertEqual(columnas_obtenidas, columnas_esperadas)

        conexion.close()
