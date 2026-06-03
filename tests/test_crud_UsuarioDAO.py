import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DAO import UsuarioDAO
from DTO.Usuario import Usuario


class TestUsuarioDAO(unittest.TestCase):

    def setUp(self):
        UsuarioDAO.ultimo_error = ""


    @patch('DAO.UsuarioDAO.getConexion')
    def test_metodos_exitosos(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_conn.cursor.return_value.fetchone.return_value = (1, "Juan", "Perez", "juan@test.com", 1)
        mock_conn.cursor.return_value.fetchall.return_value = [(1, "Juan", "Perez", "juan@test.com", 1)]
        mock_conn.cursor.return_value.rowcount = 1

        self.assertIsNotNone(UsuarioDAO.get_Usuario(1))
        self.assertEqual(len(UsuarioDAO.list_all_Usuarios()), 1)
        self.assertIsNotNone(UsuarioDAO.buscar_por_email("juan@test.com"))
        self.assertEqual(len(UsuarioDAO.buscar_por_nombre_parcial("Juan")), 1)
        self.assertTrue(UsuarioDAO.habilitar_usuario(1))
        self.assertTrue(UsuarioDAO.deshabilitar_usuario(1))
        self.assertEqual(UsuarioDAO.remove_Usuario(1), 1)


    @patch('DAO.UsuarioDAO.getConexion')
    def test_excepciones_forzadas(self, mock_get_conn):
        mock_get_conn.side_effect = Exception("Error de BD")

        user = Usuario(1, "A", "B", "C", True)
        self.assertEqual(UsuarioDAO.add_Usuario(user), 0)
        self.assertIsNone(UsuarioDAO.get_Usuario(1))
        self.assertEqual(UsuarioDAO.remove_Usuario(1), 0)
        self.assertEqual(UsuarioDAO.list_all_Usuarios(), [])
        self.assertIsNone(UsuarioDAO.buscar_por_email("test@test.com"))
        self.assertEqual(UsuarioDAO.buscar_por_nombre_parcial("Juan"), [])
        self.assertFalse(UsuarioDAO.cambiar_estado(1, True))

        self.assertEqual(UsuarioDAO.ultimo_error, "Error de BD")


    @patch('DAO.UsuarioDAO.getConexion')
    def test_usuario_no_encontrado(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.fetchone.return_value = None

        self.assertIsNone(UsuarioDAO.get_Usuario(99))
        self.assertEqual(UsuarioDAO.ultimo_error, "Usuario no encontrado")


if __name__ == '__main__':
    unittest.main()