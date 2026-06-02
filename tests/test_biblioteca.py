import unittest
from unittest.mock import patch, MagicMock
import biblioteca

class TestBiblioteca(unittest.TestCase):

    def setUp(self):
        biblioteca.ultimo_error = ""

    @patch('biblioteca.add_libro')
    @patch('biblioteca.list_all')
    def test_agregar_libro_exito(self, mock_list, mock_add):
        mock_list.return_value = []
        biblioteca.agregar_libro("El Quijote", "Cervantes")
        self.assertTrue(mock_add.called)
        self.assertEqual(biblioteca.ultimo_error, "")

    @patch('biblioteca.list_all')
    def test_agregar_libro_error(self, mock_list):
        mock_list.side_effect = Exception("Error BD")
        biblioteca.agregar_libro("Titulo", "Autor")
        self.assertEqual(biblioteca.ultimo_error, "Error BD")

    @patch('biblioteca.remove_libro')
    def test_borrar_libro_exito(self, mock_remove):
        mock_remove.return_value = 1
        resultado = biblioteca.borrar_libro(1)
        self.assertEqual(resultado, 1)

    @patch('biblioteca.remove_libro')
    def test_borrar_libro_no_encontrado(self, mock_remove):
        mock_remove.return_value = 0
        resultado = biblioteca.borrar_libro(99)
        self.assertEqual(resultado, 0)
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    @patch('biblioteca.list_all')
    def test_buscar_libro_encontrado(self, mock_list):
        libro_mock = MagicMock()
        libro_mock.to_dict.return_value = {"titulo": "Test", "id": 1, "disponible": True}
        mock_list.return_value = [libro_mock]
        resultado = biblioteca.buscar_libro("Test")
        self.assertEqual(resultado["titulo"], "Test")

    @patch('biblioteca.buscar_libro')
    @patch('biblioteca.actualizar_disponibilidad')
    def test_prestar_libro_exito(self, mock_update, mock_buscar):
        mock_buscar.return_value = {"id": 1, "disponible": True}
        mock_update.return_value = True
        res = biblioteca.prestar_libro("Test")
        self.assertEqual(res, "Libro prestado")

    @patch('biblioteca.buscar_libro')
    def test_prestar_libro_no_disponible(self, mock_buscar):
        mock_buscar.return_value = {"id": 1, "disponible": False}
        res = biblioteca.prestar_libro("Test")
        self.assertEqual(res, "Libro no disponible")

    @patch('biblioteca.buscar_libro')
    def test_devolver_libro_exito(self, mock_buscar):
        mock_buscar.return_value = {"id": 1, "disponible": False}
        with patch('biblioteca.actualizar_disponibilidad', return_value=True):
            res = biblioteca.devolver_libro("Test")
            self.assertEqual(res, "Libro devuelto")

    def test_obtener_estado(self):
        self.assertEqual(biblioteca._obtener_estado({"disponible": True}), "Disponible")
        self.assertEqual(biblioteca._obtener_estado({"disponible": False}), "Prestado")

    @patch('biblioteca.list_all')
    def test_mostrar_libros(self, mock_list):
        mock_list.return_value = []
        with patch('builtins.print') as mock_print:
            biblioteca.mostrar_libros()
            mock_print.assert_called_with("No hay libros")

    @patch('biblioteca.buscar_por_disponibilidad')
    def test_buscar_libros_por_disponibilidad(self, mock_dao):
        libro_mock = MagicMock()
        libro_mock.to_dict.return_value = {"id": 1}
        mock_dao.return_value = [libro_mock]
        res = biblioteca.buscar_libros_por_disponibilidad(True)
        self.assertEqual(len(res), 1)

    @patch('biblioteca.get_libro')
    def test_buscar_libros_por_ID(self, mock_get):
        libro_mock = MagicMock()
        libro_mock.to_dict.return_value = {"id": 1}
        mock_get.return_value = libro_mock
        res = biblioteca.buscar_libros_por_ID(1)
        self.assertEqual(res["id"], 1)

    def test_agregar_libro_modo_desconocido(self):
        biblioteca.modo = "invalido"
        biblioteca.agregar_libro("Test", "Autor")
        self.assertEqual(biblioteca.ultimo_error, "modo desconocido")
        biblioteca.modo = "normal"  # Resetear

    @patch('biblioteca.buscar_libro')
    @patch('biblioteca.actualizar_disponibilidad')
    def test_prestar_libro_error_bd(self, mock_update, mock_buscar):
        mock_buscar.return_value = {"id": 1, "disponible": True}
        mock_update.return_value = False
        res = biblioteca.prestar_libro("Test")
        self.assertEqual(res, "Error")

    @patch('biblioteca.buscar_libro')
    @patch('biblioteca.actualizar_disponibilidad')
    def test_devolver_libro_error_bd(self, mock_update, mock_buscar):
        mock_buscar.return_value = {"id": 1, "disponible": False}
        mock_update.return_value = False
        res = biblioteca.devolver_libro("Test")
        self.assertEqual(res, "Error")

    def test_devolver_libro_ya_disponible(self):
        with patch('biblioteca.buscar_libro', return_value={"id": 1, "disponible": True}):
            res = biblioteca.devolver_libro("Test")
            self.assertEqual(res, "Libro ya disponible")

    def test_buscar_libros_por_autor_excepcion(self):
        with patch('biblioteca.buscar_por_autor', side_effect=Exception("BD Down")):
            res = biblioteca.buscar_libros_por_autor("Cervantes")
            self.assertEqual(res, [])
            self.assertEqual(biblioteca.ultimo_error, "BD Down")

    def test_buscar_libros_por_disponibilidad_excepcion(self):
        with patch('biblioteca.buscar_por_disponibilidad', side_effect=Exception("BD Down")):
            res = biblioteca.buscar_libros_por_disponibilidad(True)
            self.assertEqual(res, [])
            self.assertEqual(biblioteca.ultimo_error, "BD Down")

    def test_buscar_libros_por_ID_error(self):
        with patch('biblioteca.get_libro', return_value=None):
            res = biblioteca.buscar_libros_por_ID(999)
            self.assertIsNone(res)
            self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_buscar_libros_por_ID_excepcion(self):
        with patch('biblioteca.get_libro', side_effect=Exception("Error")):
            res = biblioteca.buscar_libros_por_ID(1)
            self.assertIsNone(res)
            self.assertEqual(biblioteca.ultimo_error, "Error")

    @patch('biblioteca.list_all', side_effect=Exception("Error BD"))
    def test_agregar_libro_excepcion_list_all(self, mock_list):
        biblioteca.agregar_libro("Titulo", "Autor")
        self.assertEqual(biblioteca.ultimo_error, "Error BD")

    @patch('biblioteca.list_all', side_effect=Exception("Error BD"))
    def test_mostrar_libros_error(self, mock_list):
        biblioteca.mostrar_libros()

    def test_borrar_libro_excepcion(self):
        with patch('biblioteca.remove_libro', side_effect=Exception("Error fatal")):
            resultado = biblioteca.borrar_libro(1)
            self.assertEqual(resultado, 0)
            self.assertEqual(biblioteca.ultimo_error, "Error fatal")

    def test_print_comentario_tipos(self):
        with patch('builtins.print') as mock_print:
            biblioteca._print_comentario("Hola", " Mundo", 1)
            mock_print.assert_called_with("Hola Mundo")

            biblioteca._print_comentario("Solo", "", 2)
            mock_print.assert_called_with("Solo")

    @patch('biblioteca.list_all')
    def test_buscar_libro_formato_invalido(self, mock_list):
        mock_libro = MagicMock()
        mock_libro.to_dict.return_value = {"id": 1}
        mock_list.return_value = [mock_libro]

        resultado = biblioteca.buscar_libro("Cualquiera")
        self.assertIsNone(resultado)

    @patch('biblioteca.buscar_libro', return_value=None)
    def test_prestar_libro_no_encontrado(self, mock_buscar):
        res = biblioteca.prestar_libro("Inexistente")
        self.assertEqual(res, "Libro no encontrado")

    @patch('biblioteca.buscar_libro', return_value=None)
    def test_devolver_libro_no_encontrado(self, mock_buscar):
        res = biblioteca.devolver_libro("Inexistente")
        self.assertEqual(res, "Libro no encontrado")

if __name__ == '__main__':
    unittest.main()