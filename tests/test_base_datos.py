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
            total_libros = conexion.execute("SELECT COUNT(*) FROM libros").fetchone()[0]

        self.assertEqual(tablas, [('libros',), ('biblioteca',), ('sqlite_sequence',)])
        self.assertEqual(
            [columna[1] for columna in columnas],
            ["id", "titulo", "autor", "disponible"],
        )
        self.assertEqual(total_libros, 0)


if __name__ == "__main__":
    unittest.main()
