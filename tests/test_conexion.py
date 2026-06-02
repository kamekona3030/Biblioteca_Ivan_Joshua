import unittest
from unittest.mock import patch
import sqlite3
from Conexion import getConexion


class TestConexion(unittest.TestCase):

    @patch('Conexion.sqlite3.connect')
    def test_getConexion_exito(self, mock_connect):
        mock_conn = "conexion_objeto"
        mock_connect.return_value = mock_conn

        resultado = getConexion()

        self.assertEqual(resultado, mock_conn)
        mock_connect.assert_called_with("bd/biblioteca.db")

    @patch('builtins.print')
    @patch('Conexion.sqlite3.connect')
    def test_getConexion_error(self, mock_connect, mock_print):
        mock_connect.side_effect = sqlite3.OperationalError("Error simulado")

        with self.assertRaises(sqlite3.OperationalError):
            getConexion()

        mock_print.assert_called_with("Error al conectarse")


if __name__ == '__main__':
    unittest.main()