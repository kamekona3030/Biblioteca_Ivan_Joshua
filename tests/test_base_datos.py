import sqlite3
import unittest
from pathlib import Path

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"

class TestBaseDatosInicial(unittest.TestCase):
    def test_biblioteca_db_estructura_correcta(self):
        self.assertTrue(RUTA_BD.exists(), "La base de datos no existe en la ruta definida")

        with sqlite3.connect(RUTA_BD) as conexion:
            tablas_existentes = [t[0] for t in
                                 conexion.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            self.assertIn('libros', tablas_existentes, "La tabla 'libros' no existe")

            columnas_info = conexion.execute("PRAGMA table_info(libros)").fetchall()
            columnas_obtenidas = {info[1] for info in columnas_info}

            columnas_esperadas = {"id", "titulo", "autor", "disponible"}

            self.assertTrue(columnas_esperadas.issubset(columnas_obtenidas),
                            f"Faltan columnas en la tabla libros. Esperadas: {columnas_esperadas}, Obtenidas: {columnas_obtenidas}")
        conexion.close()

if __name__ == "__main__":
    unittest.main()