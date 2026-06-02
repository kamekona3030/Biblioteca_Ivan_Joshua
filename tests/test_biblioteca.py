import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import biblioteca


class TestBiblioteca(unittest.TestCase):

    def setUp(self):
        biblioteca.lista_libros = []
        biblioteca.modo = "normal"

    def test_libros_funcionalidad(self):
        biblioteca.agregar_libro("Libro1", "Autor1")
        self.assertEqual(len(biblioteca.lista_libros), 1)

        biblioteca.modo = "test"
        biblioteca.agregar_libro("LibroError", "Autor")
        self.assertEqual(biblioteca.ultimo_error, "modo desconocido")

        biblioteca.modo = "normal"
        self.assertEqual(biblioteca.prestar_libro("Libro1"), "Libro prestado")
        self.assertEqual(biblioteca.prestar_libro("Libro1"), "Libro no disponible")
        self.assertEqual(biblioteca.devolver_libro("Libro1"), "Libro devuelto")
        self.assertEqual(biblioteca.devolver_libro("Libro1"), "Libro ya disponible")

        self.assertEqual(biblioteca.prestar_libro("Inexistente"), "Libro no encontrado")
        self.assertEqual(biblioteca.devolver_libro("Inexistente"), "Libro no encontrado")

    def test_print_y_mostrar(self):
        biblioteca._print_comentario("t", "e", 1)
        biblioteca._print_comentario("t", "e", 2)
        biblioteca._print_comentario("t", "e", 0)

        biblioteca.lista_libros = []
        biblioteca.mostrar_libros()

        biblioteca.agregar_libro("T", "A")
        biblioteca.mostrar_libros()

    @patch('biblioteca.UsuarioDAO')
    def test_usuarios_wrappers(self, mock_dao):
        biblioteca.agregar_usuario(1, "N", "A", "E", True)
        biblioteca.obtener_usuario(1)
        biblioteca.eliminar_usuario(1)
        biblioteca.mostrar_usuarios()
        biblioteca.buscar_usuario_por_email("E")
        biblioteca.habilitar_usuario(1)
        biblioteca.deshabilitar_usuario(1)
        self.assertTrue(mock_dao.add_Usuario.called)


if __name__ == '__main__':
    unittest.main()