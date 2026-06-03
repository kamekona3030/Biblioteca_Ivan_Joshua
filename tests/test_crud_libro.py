import unittest
from unittest.mock import patch, MagicMock
import DAO.LibroDAO
from DAO.LibroDAO import (add_libro, remove_libro, get_libro, list_all,
                          buscar_por_disponibilidad, buscar_por_autor,
                          actualizar_disponibilidad)
from DTO.Libro import Libro

class TestLibroDAO(unittest.TestCase):

    def setUp(self):
        self.libro_mock = Libro(1, "Titulo", "Autor", "ISBN", True, "Cat")

    @patch('DAO.LibroDAO.getConexion')
    def test_add_libro(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        add_libro(self.libro_mock)
        self.assertTrue(mock_conn.commit.called)

    @patch('DAO.LibroDAO.getConexion')
    def test_add_libro_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("DB Error")
        add_libro(self.libro_mock)
        self.assertEqual(DAO.LibroDAO.ultimo_error, "DB Error")

    @patch('DAO.LibroDAO.getConexion')
    def test_remove_libro_success(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = remove_libro(1)
        self.assertEqual(res, 1)

    @patch('DAO.LibroDAO.getConexion')
    def test_remove_libro_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Error")
        res = remove_libro(1)
        self.assertEqual(res, 0)
        self.assertEqual(DAO.LibroDAO.ultimo_error, "Error")

    @patch('DAO.LibroDAO.getConexion')
    def test_get_libro_found(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1, "T", "A", "I", 1, "C"]
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = get_libro(1)
        self.assertIsNotNone(res)

    @patch('DAO.LibroDAO.getConexion')
    def test_get_libro_not_found(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = get_libro(1)
        self.assertIsNone(res)

    @patch('DAO.LibroDAO.getConexion')
    def test_get_libro_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Err")
        res = get_libro(1)
        self.assertIsNone(res)

    @patch('DAO.LibroDAO.getConexion')
    def test_list_all_success(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [[1, "T", "A", "I", 1, "C"]]
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = list_all()
        self.assertEqual(len(res), 1)

    @patch('DAO.LibroDAO.getConexion')
    def test_list_all_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Err")
        res = list_all()
        self.assertEqual(res, [])

    @patch('DAO.LibroDAO.getConexion')
    def test_buscar_por_disponibilidad_success(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [[1, "T", "A", "I", 1, "C"]]
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = buscar_por_disponibilidad(True)
        self.assertEqual(len(res), 1)

    @patch('DAO.LibroDAO.getConexion')
    def test_buscar_por_disponibilidad_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Err")
        res = buscar_por_disponibilidad(True)
        self.assertEqual(res, [])

    @patch('DAO.LibroDAO.getConexion')
    def test_buscar_por_autor_success(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [[1, "T", "A", "I", 1, "C"]]
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = buscar_por_autor("A")
        self.assertEqual(len(res), 1)

    @patch('DAO.LibroDAO.getConexion')
    def test_buscar_por_autor_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Err")
        res = buscar_por_autor("A")
        self.assertEqual(res, [])

    @patch('DAO.LibroDAO.getConexion')
    def test_actualizar_disponibilidad_success(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = actualizar_disponibilidad(1, True)
        self.assertTrue(res)

    @patch('DAO.LibroDAO.getConexion')
    def test_actualizar_disponibilidad_fail(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_get_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        res = actualizar_disponibilidad(1, True)
        self.assertFalse(res)

    @patch('DAO.LibroDAO.getConexion')
    def test_actualizar_disponibilidad_exception(self, mock_get_conn):
        mock_get_conn.return_value.__enter__.return_value.cursor.side_effect = Exception("Err")
        res = actualizar_disponibilidad(1, True)
        self.assertFalse(res)

if __name__ == '__main__':
    unittest.main()