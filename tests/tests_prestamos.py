import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch, MagicMock

import biblioteca
from Libro import Libro
from Prestamo import Prestamo


class TestDevolverLibroFase6(unittest.TestCase):
    """
    Tests de la Fase 6 para la función devolver_libro
    Verifica la integración con PrestamoDAO y la lógica de devolución
    """

    def setUp(self):
        biblioteca.ultimo_error = ""

    @patch('biblioteca.PrestamoDAO.registrar_devolucion')
    @patch('biblioteca.PrestamoDAO.get_prestamo_activo')
    @patch('biblioteca.actualizar_disponibilidad')
    @patch('biblioteca.list_all')
    def test_devolver_libro_exitoso(self, mock_list, mock_actualizar, mock_get_prestamo, mock_registrar):
        """Devolver un libro prestado con préstamo activo registra la devolución correctamente."""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", False, "Clasico")
        mock_list.return_value = [libro_mock]
        mock_actualizar.return_value = True
        mock_get_prestamo.return_value = Prestamo(id_prestamo=1, libro_id=1, usuario_id=5)
        mock_registrar.return_value = True

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            resultado = biblioteca.devolver_libro("El Quijote", 5)

        self.assertEqual(resultado, "Libro devuelto")
        self.assertEqual(biblioteca.ultimo_error, "")
        self.assertIn("Se devolvio el libro", pantalla.getvalue())
        mock_registrar.assert_called_once_with(1, 5)

    @patch('biblioteca.list_all')
    def test_devolver_libro_no_encontrado(self, mock_list):
        """Intentar devolver un libro que no existe en el sistema."""
        mock_list.return_value = []

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            resultado = biblioteca.devolver_libro("LibroFantasma", 5)

        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    @patch('biblioteca.list_all')
    def test_devolver_libro_ya_disponible(self, mock_list):
        """Intentar devolver un libro que ya estaba disponible (no está prestado)."""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", True, "Clasico")
        mock_list.return_value = [libro_mock]

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            resultado = biblioteca.devolver_libro("El Quijote", 5)

        self.assertEqual(resultado, "Libro ya disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro ya disponible")

    @patch('biblioteca.PrestamoDAO.get_prestamo_activo')
    @patch('biblioteca.list_all')
    def test_devolver_libro_sin_prestamo_activo(self, mock_list, mock_get_prestamo):
        """Intentar devolver un libro prestado pero sin préstamo activo para ese usuario."""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", False, "Clasico")
        mock_list.return_value = [libro_mock]
        mock_get_prestamo.return_value = None  # No hay préstamo activo para este usuario

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            resultado = biblioteca.devolver_libro("El Quijote", 99)

        self.assertEqual(resultado, "Préstamo no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Préstamo no encontrado")

    @patch('biblioteca.PrestamoDAO.get_prestamo_activo')
    @patch('biblioteca.actualizar_disponibilidad')
    @patch('biblioteca.list_all')
    def test_devolver_libro_error_actualizar_disponibilidad(self, mock_list, mock_actualizar, mock_get_prestamo):
        """Error al actualizar disponibilidad del libro durante la devolución."""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", False, "Clasico")
        mock_list.return_value = [libro_mock]
        mock_get_prestamo.return_value = Prestamo(id_prestamo=1, libro_id=1, usuario_id=5)
        mock_actualizar.return_value = False  # Falla la actualización

        resultado = biblioteca.devolver_libro("El Quijote", 5)
        self.assertEqual(resultado, "Error")

    @patch('biblioteca.PrestamoDAO.registrar_devolucion')
    @patch('biblioteca.PrestamoDAO.get_prestamo_activo')
    @patch('biblioteca.actualizar_disponibilidad')
    @patch('biblioteca.list_all')
    def test_devolver_libro_error_registrar_devolucion(self, mock_list, mock_actualizar, mock_get_prestamo,
                                                       mock_registrar):
        """Error al registrar la devolución en la tabla de préstamos."""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", False, "Clasico")
        mock_list.return_value = [libro_mock]
        mock_get_prestamo.return_value = Prestamo(id_prestamo=1, libro_id=1, usuario_id=5)
        mock_actualizar.return_value = True
        mock_registrar.return_value = False  # Falla el registro de devolución

        resultado = biblioteca.devolver_libro("El Quijote", 5)
        self.assertEqual(resultado, "Error")


class TestPrestamoDAO(unittest.TestCase):
    """Tests del PrestamoDAO, específicamente los métodos de devolución."""

    @patch('DAO.PrestamoDAO.getConexion')
    def test_registrar_devolucion_exitoso(self, mock_get_conn):
        """Registrar una devolución cuando existe un préstamo activo."""
        from DAO import PrestamoDAO
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        resultado = PrestamoDAO.registrar_devolucion(1, 5)
        self.assertTrue(resultado)
        self.assertEqual(PrestamoDAO.ultimo_error, "")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_registrar_devolucion_no_encontrado(self, mock_get_conn):
        """Intentar registrar devolución cuando no hay préstamo activo."""
        from DAO import PrestamoDAO
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Ninguna fila afectada
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        resultado = PrestamoDAO.registrar_devolucion(1, 99)
        self.assertFalse(resultado)
        self.assertEqual(PrestamoDAO.ultimo_error, "Préstamo activo no encontrado")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_registrar_devolucion_excepcion(self, mock_get_conn):
        """Error de base de datos al registrar devolución."""
        from DAO import PrestamoDAO
        mock_get_conn.side_effect = Exception("Error de BD")

        resultado = PrestamoDAO.registrar_devolucion(1, 5)
        self.assertFalse(resultado)
        self.assertEqual(PrestamoDAO.ultimo_error, "Error de BD")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_get_prestamo_activo_encontrado(self, mock_get_conn):
        """Obtener un préstamo activo existente."""
        from DAO import PrestamoDAO
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 1, 5, "2025-01-01", None, "prestado")
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        resultado = PrestamoDAO.get_prestamo_activo(1, 5)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.estado, "prestado")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_get_prestamo_activo_no_encontrado(self, mock_get_conn):
        """Buscar préstamo activo cuando no existe."""
        from DAO import PrestamoDAO
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        resultado = PrestamoDAO.get_prestamo_activo(1, 99)
        self.assertIsNone(resultado)
        self.assertEqual(PrestamoDAO.ultimo_error, "Préstamo no encontrado")


if __name__ == '__main__':
    unittest.main()






























