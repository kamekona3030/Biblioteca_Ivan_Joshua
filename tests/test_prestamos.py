import unittest
from unittest.mock import patch
import biblioteca
from Usuario import Usuario
from Libro import Libro

class TestPrestamos(unittest.TestCase):

    def setUp(self):
        biblioteca.ultimo_error = ""

    @patch('biblioteca.UsuarioDAO.get_Usuario')
    @patch('biblioteca.get_libro')
    @patch('biblioteca.actualizar_disponibilidad')
    def test_prestamo_exitoso(self, mock_actualizar, mock_get_libro, mock_get_usuario):
        mock_get_usuario.return_value = Usuario(500, "Juan", "Pérez", "juan@email.com", habilitado=True)
        mock_get_libro.return_value = Libro(901, "Libro Test", "Autor A", "111", disponible=True)
        resultado = biblioteca.prestar_libro(901, 500)
        self.assertTrue(resultado, f"El prestamo fallo: {biblioteca.ultimo_error}")
        mock_actualizar.assert_called_once_with(901, False)

    @patch('biblioteca.UsuarioDAO.get_Usuario')
    @patch('biblioteca.get_libro')
    def test_prestamo_usuario_deshabilitado(self, mock_get_libro, mock_get_usuario):
        mock_get_usuario.return_value = Usuario(600, "Luis", "Soto", "luis@email.com", habilitado=False)
        mock_get_libro.return_value = Libro(901, "Libro Test", "Autor", "111", disponible=True)
        resultado = biblioteca.prestar_libro(901, 600)
        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Usuario deshabilitado")

    @patch('biblioteca.UsuarioDAO.get_Usuario')
    @patch('biblioteca.get_libro')
    def test_prestamo_libro_no_disponible(self, mock_get_libro, mock_get_usuario):
        mock_get_usuario.return_value = Usuario(500, "Juan", "Pérez", "juan@email.com", habilitado=True)
        mock_get_libro.return_value = Libro(902, "Libro Test", "Autor", "111", disponible=False)
        resultado = biblioteca.prestar_libro(902, 500)
        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Libro no disponible")