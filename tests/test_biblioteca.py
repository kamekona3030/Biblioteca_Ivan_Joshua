import unittest

import biblioteca


class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        biblioteca.libros.clear()

    def test_agregar_libro_guarda_titulo_autor_y_estado_disponible(self):
        biblioteca.agregar_libro("El Quijote", "Miguel de Cervantes")

        self.assertEqual(len(biblioteca.libros), 1)
        self.assertEqual(biblioteca.libros[0]["titulo"], "El Quijote")
        self.assertEqual(biblioteca.libros[0]["autor"], "Miguel de Cervantes")
        self.assertTrue(biblioteca.libros[0]["disponible"])

    def test_prestar_libro_cambia_estado_si_existe_y_esta_disponible(self):
        biblioteca.agregar_libro("Nada", "Carmen Laforet")

        resultado = biblioteca.prestar_libro("Nada")

        self.assertEqual(resultado, "Libro prestado")
        self.assertFalse(biblioteca.libros[0]["disponible"])

    def test_devolver_libro_cambia_estado_si_estaba_prestado(self):
        biblioteca.agregar_libro("La colmena", "Camilo Jose Cela")
        biblioteca.prestar_libro("La colmena")

        resultado = biblioteca.devolver_libro("La colmena")

        self.assertEqual(resultado, "Libro devuelto")
        self.assertTrue(biblioteca.libros[0]["disponible"])

    def test_buscar_libro_existente_devuelve_diccionario(self):
        biblioteca.agregar_libro("La vuelta al mundo en 80 dias", "Julio Verne")
        libro = biblioteca.buscar_libro("La vuelta al mundo en 80 dias")

        self.assertIsNotNone(libro)
        self.assertEqual(libro["autor"], "Julio Verne")

    def test_buscar_libro_no_existente_devuelve_none(self):
        libro = biblioteca.buscar_libro("Inventado")
        self.assertIsNone(libro)

    def test_prestar_libro_no_existente_error(self):
        resultado = biblioteca.prestar_libro("Inexistente")

        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_prestar_lbro_ya_prestado(self):
        biblioteca.agregar_libro("La odisea", "Homero")
        biblioteca.prestar_libro("La odisea")
        resultado = biblioteca.prestar_libro("La odisea")
        self.assertEqual(resultado, "Libro no disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro no disponible")

    def test_devolver_libro_disponible(self):
        biblioteca.agregar_libro("Moby dick", "Herman Melville")
        resultado = biblioteca.devolver_libro("Moby dick")
        self.assertEqual(resultado, "Libro ya disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro ya disponible")


    def test_print_comentario_tipos_alternativos(self):
        biblioteca.agregar_libro("El principito", "Antoine de Saint-Exupéry")
        biblioteca._print_comentario("Libro agregado")

    def test_cambiar_estado_libro_accion_inexistente(self):
        ejemplo = {"titulo": "Prueba", "autor": "prueba", "disponible":True}
        resultado = biblioteca._cambiar_estado_libro("accion inexistente", ejemplo)
        self.assertEqual(resultado, "Nada")

    def test_verificar_libro_sin_titulo(self):
        ejemplo = {"autor": "prueba"}
        resultado = biblioteca._verificar_libro(ejemplo, "Titulo")
        self.assertFalse(resultado)


    def test_devolver_libro_inexistente(self):
        resultado = biblioteca.devolver_libro("Libro fantasma")
        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_mostrar_flujos_vacio_lleno(self):
        biblioteca.mostrar_libros()

        biblioteca.agregar_libro("One piece", "Oda")
        biblioteca.agregar_libro("Hamlet", "William Shakespeare")
        biblioteca.prestar_libro("Hamlet")

        biblioteca.mostrar_libros()





if __name__ == "__main__":
    unittest.main()
