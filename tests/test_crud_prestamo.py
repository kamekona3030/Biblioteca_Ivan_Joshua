import unittest
from unittest.mock import patch, MagicMock
import DAO.PrestamoDAO
from DAO.PrestamoDAO import registrar_devolucion, get_prestamo_activo, list_prestamos_usuario
from DTO.Prestamo import Prestamo


class TestPrestamoDAO(unittest.TestCase):

    @patch('DAO.PrestamoDAO.getConexion')
    def test_registrar_devolucion_success(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        res = registrar_devolucion(1, 101)
        self.assertTrue(res)
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_registrar_devolucion_fail(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        res = registrar_devolucion(1, 101)
        self.assertFalse(res)
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "Préstamo activo no encontrado")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_registrar_devolucion_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("DB Error")

        res = registrar_devolucion(1, 101)
        self.assertFalse(res)
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "DB Error")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_get_prestamo_activo_found(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1, 5, 101, "2026-06-01", None, "prestado"]
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        res = get_prestamo_activo(5, 101)
        self.assertIsNotNone(res)
        self.assertIsInstance(res, Prestamo)
        self.assertEqual(res.id_prestamo, 1)
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_get_prestamo_activo_not_found(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        res = get_prestamo_activo(5, 101)
        self.assertIsNone(res)
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "Préstamo no encontrado")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_get_prestamo_activo_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Err")

        res = get_prestamo_activo(5, 101)
        self.assertIsNone(res)
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "Err")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_list_prestamos_usuario_success(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            [1, 5, 101, "2026-06-01", "2026-06-03", "devuelto"],
            [2, 8, 101, "2026-06-03", None, "prestado"]
        ]
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        res = list_prestamos_usuario(101)
        self.assertEqual(len(res), 2)
        self.assertIsInstance(res[0], Prestamo)
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "")

    @patch('DAO.PrestamoDAO.getConexion')
    def test_list_prestamos_usuario_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Err")

        res = list_prestamos_usuario(101)
        self.assertEqual(res, [])
        self.assertEqual(DAO.PrestamoDAO.ultimo_error, "Err")


if __name__ == '__main__':
    unittest.main()