import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch, MagicMock
from Main import biblioteca
from DTO.Libro import Libro
from DTO.Usuario import Usuario


class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        """Prepara el entorno: limpia el estado"""
        biblioteca.ultimo_error = ""

    @patch('Main.biblioteca.UsuarioDAO.get_Usuario')
    @patch('Main.biblioteca.get_libro')
    @patch('Main.biblioteca.actualizar_disponibilidad')
    @patch('Main.biblioteca.PrestamoDAO.registrar_prestamo')
    def test_prestamo_exitoso(self,mock_registrar_prestamo, mock_actualizar, mock_get_libro, mock_get_usuario):
        mock_registrar_prestamo.return_value = True
        mock_get_usuario.return_value = Usuario(500, "Juan", "Pérez", "juan@email.com", habilitado=True)
        mock_get_libro.return_value = Libro(901, "Libro Test", "Autor A", "111", disponible=True)
        resultado = biblioteca.prestar_libro(901, 500)
        self.assertTrue(resultado, f"El prestamo fallo: {biblioteca.ultimo_error}")
        mock_actualizar.assert_called_once_with(901, False)

    @patch('Main.biblioteca.UsuarioDAO.get_Usuario')
    @patch('Main.biblioteca.get_libro')
    def test_prestamo_usuario_deshabilitado(self, mock_get_libro, mock_get_usuario):
        mock_get_usuario.return_value = Usuario(600, "Luis", "Soto", "luis@email.com", habilitado=False)
        mock_get_libro.return_value = Libro(901, "Libro Test", "Autor", "111", disponible=True)
        resultado = biblioteca.prestar_libro(901, 600)
        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Usuario deshabilitado")

    @patch('Main.biblioteca.UsuarioDAO.get_Usuario')
    @patch('Main.biblioteca.get_libro')
    def test_prestamo_libro_no_disponible(self, mock_get_libro, mock_get_usuario):
        mock_get_usuario.return_value = Usuario(500, "Juan", "Pérez", "juan@email.com", habilitado=True)
        mock_get_libro.return_value = Libro(902, "Libro Test", "Autor", "111", disponible=False)
        resultado = biblioteca.prestar_libro(902, 500)
        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Libro no disponible")


    @patch('Main.biblioteca.list_all')
    def test_devolver_libro_no_encontrado(self, mock_list):
        """Test de devolver libro que no existe"""
        mock_list.return_value = []
        pantalla = StringIO()
        with redirect_stdout(pantalla):
            resultado = biblioteca.devolver_libro(0, 1)

        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    @patch('Main.biblioteca.get_libro')
    def test_devolver_libro_ya_disponible(self, mock_get_libro):
        """Test de devolver libro que ya está disponible"""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", True, "Clasico")
        mock_get_libro.return_value = libro_mock

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            resultado = biblioteca.devolver_libro(1, 1)

        self.assertEqual(resultado, "Libro ya disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro ya disponible")

    @patch('Main.biblioteca.PrestamoDAO.get_prestamo_activo')
    @patch('Main.biblioteca.get_libro')
    @patch('Main.biblioteca.actualizar_disponibilidad')
    def test_devolver_libro_error_actualizacion(self, mock_actualizar, mock_get_libro, mock_get_prestamo):
        """Test de error al actualizar disponibilidad"""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", False, "Clasico")
        mock_get_libro.return_value = libro_mock
        mock_actualizar.return_value = False
        mock_get_prestamo.return_value = MagicMock()

        resultado = biblioteca.devolver_libro(1, 1)
        self.assertEqual(resultado, "Error")

    @patch('Main.biblioteca.list_all')
    @patch('Main.biblioteca.add_libro')
    def test_agregar_libro_exitoso(self, mock_add, mock_list):
        """Test de agregar libro con éxito"""
        mock_list.return_value = [Libro(1, "Libro1", "Autor1", "111", True, "Cat1")]

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.agregar_libro("Nuevo Libro", "Nuevo Autor")

        self.assertIn("Libro agregado:", pantalla.getvalue())
        self.assertEqual(biblioteca.ultimo_error, "")

    @patch('Main.biblioteca.list_all')
    @patch('Main.biblioteca.add_libro')
    def test_agregar_libro_error(self, mock_add, mock_list):
        """Test de error al agregar libro"""
        mock_list.side_effect = Exception("Error de BD")

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.agregar_libro("Nuevo Libro", "Nuevo Autor")

        self.assertEqual(biblioteca.ultimo_error, "Error de BD")

    @patch('Main.biblioteca.list_all')
    @patch('Main.biblioteca.add_libro')
    def test_agregar_libro_modo_desconocido(self, mock_add, mock_list):
        """Test de modo desconocido"""
        biblioteca.modo = "desconocido"

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.agregar_libro("Nuevo Libro", "Nuevo Autor")

        self.assertEqual(biblioteca.ultimo_error, "modo desconocido")
        biblioteca.modo = "normal"  # Restaurar

    @patch('Main.biblioteca.remove_libro')
    def test_borrar_libro_exitoso(self, mock_remove):
        """Test de borrar libro con éxito"""
        mock_remove.return_value = 1

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            resultado = biblioteca.borrar_libro(1)

        self.assertEqual(resultado, 1)
        self.assertIn("eliminado", pantalla.getvalue())

    @patch('Main.biblioteca.remove_libro')
    def test_borrar_libro_no_encontrado(self, mock_remove):
        """Test de borrar libro no encontrado"""
        mock_remove.return_value = 0

        resultado = biblioteca.borrar_libro(999)
        self.assertEqual(resultado, 0)
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    @patch('Main.biblioteca.remove_libro')
    def test_borrar_libro_error(self, mock_remove):
        """Test de error al borrar libro"""
        mock_remove.side_effect = Exception("Error de BD")

        resultado = biblioteca.borrar_libro(1)
        self.assertEqual(resultado, 0)
        self.assertEqual(biblioteca.ultimo_error, "Error de BD")

    @patch('Main.biblioteca.list_all')
    def test_buscar_libro_encontrado(self, mock_list):
        """Test de buscar libro que existe"""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", True, "Clasico")
        mock_list.return_value = [libro_mock]

        resultado = biblioteca.buscar_libro("El Quijote")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["titulo"], "El Quijote")

    @patch('Main.biblioteca.list_all')
    def test_buscar_libro_no_encontrado(self, mock_list):
        """Test de buscar libro que no existe"""
        mock_list.return_value = []

        resultado = biblioteca.buscar_libro("LibroFantasma")
        self.assertIsNone(resultado)

    @patch('Main.biblioteca.list_all')
    def test_mostrar_libros_vacio(self, mock_list):
        """Test para verificar salida cuando no hay libros"""
        mock_list.return_value = []
        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.mostrar_libros()

        self.assertIn("No hay libros", pantalla.getvalue())

    @patch('Main.biblioteca.list_all')
    def test_mostrar_libros_con_datos(self, mock_list):
        """Test de mostrar libros con datos"""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", True, "Clasico")
        mock_list.return_value = [libro_mock]

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.mostrar_libros()

        self.assertIn("El Quijote", pantalla.getvalue())

    @patch('Main.biblioteca.list_all')
    def test_mostrar_libros_error(self, mock_list):
        """Test de error al mostrar libros"""
        mock_list.side_effect = Exception("Error de BD")

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.mostrar_libros()

        self.assertIn("Error al listar", pantalla.getvalue())

    @patch('Main.biblioteca.UsuarioDAO.add_Usuario')
    def test_agregar_usuario(self, mock_add):
        """Test de agregar usuario"""
        biblioteca.UsuarioDAO.ultimo_error = ""
        biblioteca.agregar_usuario(1, "Juan", "Perez", "juan@test.com", True)
        self.assertEqual(biblioteca.ultimo_error, "")

    @patch('Main.biblioteca.UsuarioDAO.get_Usuario')
    def test_obtener_usuario(self, mock_get):
        """Test de obtener usuario"""
        usuario_mock = Usuario(1, "Juan", "Perez", "juan@test.com", True)
        mock_get.return_value = usuario_mock
        biblioteca.UsuarioDAO.ultimo_error = ""

        resultado = biblioteca.obtener_usuario(1)
        self.assertIsNotNone(resultado)

    @patch('Main.biblioteca.UsuarioDAO.remove_Usuario')
    def test_eliminar_usuario(self, mock_remove):
        """Test de eliminar usuario"""
        mock_remove.return_value = 1
        biblioteca.UsuarioDAO.ultimo_error = ""

        resultado = biblioteca.eliminar_usuario(1)
        self.assertEqual(resultado, 1)

    @patch('Main.biblioteca.UsuarioDAO.list_all_Usuarios')
    def test_mostrar_usuarios_vacio(self, mock_list):
        """Test de mostrar usuarios vacío"""
        mock_list.return_value = []
        biblioteca.UsuarioDAO.ultimo_error = ""

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.mostrar_usuarios()

        self.assertIn("No hay usuarios", pantalla.getvalue())

    @patch('Main.biblioteca.UsuarioDAO.list_all_Usuarios')
    def test_mostrar_usuarios_con_datos(self, mock_list):
        """Test de mostrar usuarios con datos"""
        usuario_mock = Usuario(1, "Juan", "Perez", "juan@test.com", True)
        mock_list.return_value = [usuario_mock]
        biblioteca.UsuarioDAO.ultimo_error = ""

        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca.mostrar_usuarios()

        self.assertNotIn("No hay usuarios", pantalla.getvalue())

    @patch('Main.biblioteca.UsuarioDAO.buscar_por_email')
    def test_buscar_usuario_por_email(self, mock_buscar):
        """Test de buscar usuario por email"""
        usuario_mock = Usuario(1, "Juan", "Perez", "juan@test.com", True)
        mock_buscar.return_value = usuario_mock
        biblioteca.UsuarioDAO.ultimo_error = ""

        resultado = biblioteca.buscar_usuario_por_email("juan@test.com")
        self.assertIsNotNone(resultado)

    @patch('Main.biblioteca.UsuarioDAO.buscar_por_nombre_parcial')
    def test_buscar_usuario_por_nombre_parcial(self, mock_buscar):
        """Test de buscar usuario por nombre parcial"""
        usuario_mock = Usuario(1, "Juan", "Perez", "juan@test.com", True)
        mock_buscar.return_value = [usuario_mock]
        biblioteca.UsuarioDAO.ultimo_error = ""

        resultado = biblioteca.buscar_usuario_por_nombre_parcial("Juan")
        self.assertEqual(len(resultado), 1)

    @patch('Main.biblioteca.UsuarioDAO.habilitar_usuario')
    def test_habilitar_usuario(self, mock_habilitar):
        """Test de habilitar usuario"""
        mock_habilitar.return_value = True
        biblioteca.UsuarioDAO.ultimo_error = ""

        resultado = biblioteca.habilitar_usuario(1)
        self.assertTrue(resultado)

    @patch('Main.biblioteca.UsuarioDAO.deshabilitar_usuario')
    def test_deshabilitar_usuario(self, mock_deshabilitar):
        """Test de deshabilitar usuario"""
        mock_deshabilitar.return_value = True
        biblioteca.UsuarioDAO.ultimo_error = ""

        resultado = biblioteca.deshabilitar_usuario(1)
        self.assertTrue(resultado)

    @patch('Main.biblioteca.buscar_por_disponibilidad')
    def test_buscar_libros_por_disponibilidad_exitoso(self, mock_buscar):
        """Test de buscar libros por disponibilidad"""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", True, "Clasico")
        mock_buscar.return_value = [libro_mock]

        resultado = biblioteca.buscar_libros_por_disponibilidad(True)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(biblioteca.ultimo_error, "")

    @patch('Main.biblioteca.buscar_por_disponibilidad')
    def test_buscar_libros_por_disponibilidad_error(self, mock_buscar):
        """Test de error al buscar libros por disponibilidad"""
        mock_buscar.side_effect = Exception("Error de BD")

        resultado = biblioteca.buscar_libros_por_disponibilidad(True)
        self.assertEqual(resultado, [])
        self.assertEqual(biblioteca.ultimo_error, "Error de BD")

    @patch('Main.biblioteca.buscar_por_autor')
    def test_buscar_libros_por_autor_exitoso(self, mock_buscar):
        """Test de buscar libros por autor"""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", True, "Clasico")
        mock_buscar.return_value = [libro_mock]

        resultado = biblioteca.buscar_libros_por_autor("Cervantes")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(biblioteca.ultimo_error, "")

    @patch('Main.biblioteca.buscar_por_autor')
    def test_buscar_libros_por_autor_error(self, mock_buscar):
        """Test de error al buscar libros por autor"""
        mock_buscar.side_effect = Exception("Error de BD")

        resultado = biblioteca.buscar_libros_por_autor("Cervantes")
        self.assertEqual(resultado, [])
        self.assertEqual(biblioteca.ultimo_error, "Error de BD")

    @patch('Main.biblioteca.get_libro')
    def test_buscar_libros_por_ID_exitoso(self, mock_get):
        """Test de buscar libro por ID"""
        libro_mock = Libro(1, "El Quijote", "Cervantes", "123", True, "Clasico")
        mock_get.return_value = libro_mock

        resultado = biblioteca.buscar_libros_por_ID(1)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["titulo"], "El Quijote")
        self.assertEqual(biblioteca.ultimo_error, "")

    @patch('Main.biblioteca.get_libro')
    def test_buscar_libros_por_ID_no_encontrado(self, mock_get):
        """Test de buscar libro por ID no encontrado"""
        mock_get.return_value = None

        resultado = biblioteca.buscar_libros_por_ID(999)
        self.assertIsNone(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    @patch('Main.biblioteca.get_libro')
    def test_buscar_libros_por_ID_error(self, mock_get):
        """Test de error al buscar libro por ID"""
        mock_get.side_effect = Exception("Error de BD")

        resultado = biblioteca.buscar_libros_por_ID(1)
        self.assertIsNone(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Error de BD")

    def test_print_comentario_tipo_1(self):
        """Test de _print_comentario tipo 1"""
        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca._print_comentario("Test", " extra", 1)
        self.assertIn("Test extra", pantalla.getvalue())

    def test_print_comentario_tipo_2(self):
        """Test de _print_comentario tipo 2"""
        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca._print_comentario("Test", "extra", 2)
        self.assertIn("Test", pantalla.getvalue())

    def test_print_comentario_tipo_0(self):
        """Test de _print_comentario tipo 0"""
        pantalla = StringIO()
        with redirect_stdout(pantalla):
            biblioteca._print_comentario("Test", "extra", 0)
        self.assertIn("Test", pantalla.getvalue())

    def test_verificar_libro_con_titulo(self):
        """Test de _verificar_libro con título correcto"""
        libro_dict = {"titulo": "El Quijote"}
        resultado = biblioteca._verificar_libro(libro_dict, "El Quijote")
        self.assertTrue(resultado)

    def test_verificar_libro_sin_titulo(self):
        """Test de _verificar_libro sin campo título"""
        libro_dict = {"autor": "Cervantes"}
        resultado = biblioteca._verificar_libro(libro_dict, "El Quijote")
        self.assertFalse(resultado)

    def test_verificar_libro_titulo_diferente(self):
        """Test de _verificar_libro con título diferente"""
        libro_dict = {"titulo": "Don Juan"}
        resultado = biblioteca._verificar_libro(libro_dict, "El Quijote")
        self.assertFalse(resultado)

    def test_obtener_estado_disponible(self):
        """Test de _obtener_estado cuando está disponible"""
        libro_dict = {"disponible": True}
        resultado = biblioteca._obtener_estado(libro_dict)
        self.assertEqual(resultado, "Disponible")

    def test_obtener_estado_prestado(self):
        """Test de _obtener_estado cuando está prestado"""
        libro_dict = {"disponible": False}
        resultado = biblioteca._obtener_estado(libro_dict)
        self.assertEqual(resultado, "Prestado")


    @patch('Main.biblioteca.registrar_log')
    @patch('Main.biblioteca.PrestamoDAO.registrar_prestamo')
    @patch('Main.biblioteca.get_libro')
    @patch('Main.biblioteca.UsuarioDAO.get_Usuario')
    def test_prestamo_registra_log(self, mock_get_usuario, mock_get_libro, mock_registrar_prestamo,
                                   mock_registrar_log):
        """Test que verifica que se registre un log al realizar un préstamo exitoso"""
        mock_get_usuario.return_value = Usuario(500, "Juan", "Pérez", "juan@email.com", habilitado=True)
        mock_get_libro.return_value = Libro(901, "El Quijote", "Cervantes", "111", disponible=True)
        mock_registrar_prestamo.return_value = True

        resultado = biblioteca.prestar_libro(901, 500)
        self.assertTrue(resultado)
        mock_registrar_log.assert_called_once_with("Usuario 500 ha prestado Libro El Quijote")

    def test_generar_isbn_secuencial(self):
        """Test de que el ISBN se genera a partir del id de forma secuencial"""
        self.assertEqual(biblioteca._generar_isbn(1), "000-00001-0")
        self.assertEqual(biblioteca._generar_isbn(42), "000-00042-0")
        self.assertNotEqual(biblioteca._generar_isbn(1), biblioteca._generar_isbn(2))



if __name__ == "__main__":
    unittest.main()
