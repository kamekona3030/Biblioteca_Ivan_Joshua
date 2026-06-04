import sys
from biblioteca import (
    agregar_libro, borrar_libro, buscar_libro, prestar_libro, devolver_libro,
    mostrar_libros, agregar_usuario, obtener_usuario, eliminar_usuario,
    mostrar_usuarios, buscar_usuario_por_email, buscar_usuario_por_nombre_parcial,
    habilitar_usuario, deshabilitar_usuario, buscar_libros_por_disponibilidad,
    buscar_libros_por_autor, buscar_libros_por_ID
)


def menu_principal():
    """Menu principal del sistema"""
    while True:
        print("\n" + "=" * 40)
        print("     SISTEMA DE GESTIÓN DE BIBLIOTECA    ")
        print("=" * 40)
        print("1. Gestión de Libros")
        print("2. Gestión de Usuarios")
        print("3. Préstamos y Devoluciones")
        print("0. Salir")
        print("=" * 40)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_libros()
        elif opcion == "2":
            menu_usuarios()
        elif opcion == "3":
            menu_prestamos()
        elif opcion == "0":
            print("\n¡Hasta luego! Cerramos la biblioteca. ")
            sys.exit()
        else:
            print(" Opción no válida. Intenta de nuevo.")


def menu_libros():
    """Menu secundario del sistema encargado de la parte de libros"""
    while True:
        print("\n--- SUBMENÚ: GESTIÓN DE LIBROS ---")
        print("1. Añadir nuevo libro")
        print("2. Mostrar todos los libros")
        print("3. Buscar libro por Título")
        print("4. Buscar libro por ID")
        print("5. Buscar libros por Autor")
        print("6. Buscar por Disponibilidad (Disponibles/Prestados)")
        print("7. Eliminar un libro")
        print("0.  Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            titulo = input("Título del libro: ")
            autor = input("Autor del libro: ")
            categoria = input("Categoria del libro: ")
            agregar_libro(titulo, autor, categoria)

        elif opcion == "2":
            print("\n--- Listado de Libros ---")
            mostrar_libros()

        elif opcion == "3":
            titulo = input("Introduce el título a buscar: ")
            resultado = buscar_libro(titulo)
            print(f"\nResultado: {resultado}")

        elif opcion == "4":
            try:
                id_lib = int(input("Introduce el ID del libro: "))
                resultado = buscar_libros_por_ID(id_lib)
                print(f"\nResultado: {resultado}")
            except ValueError:
                print(" El ID debe ser un número entero.")

        elif opcion == "5":
            autor = input("Introduce el autor a buscar: ")
            resultados = buscar_libros_por_autor(autor)
            print(f"\nLibros encontrados de {autor}:")
            for lib in resultados:
                print(lib)

        elif opcion == "6":
            disp_input = input("¿Buscar disponibles? (S/N): ").strip().lower()
            disponible = disp_input == 's'
            resultados = buscar_libros_por_disponibilidad(disponible)
            estado = "Disponibles" if disponible else "Prestados"
            print(f"\n--- Libros {estado} ---")
            for lib in resultados:
                print(lib)

        elif opcion == "7":
            try:
                id_lib = int(input("Introduce el ID del libro a eliminar: "))
                filas = borrar_libro(id_lib)
                if filas == 0:
                    print("️ No se pudo eliminar el libro.")
            except ValueError:
                print(" El ID debe ser un número entero.")

        elif opcion == "0":
            break
        else:
            print(" Opción no válida.")


def menu_usuarios():
    """Menu secundario del sistema encargado de la parte de usuarios"""

    while True:
        print("\n---  SUBMENÚ: GESTIÓN DE USUARIOS ---")
        print("1. Registrar nuevo usuario")
        print("2. Mostrar todos los usuarios")
        print("3. Obtener usuario por ID")
        print("4. Buscar usuario por Email")
        print("5. Buscar usuario por Nombre (Parcial)")
        print("6. Habilitar usuario")
        print("7. Deshabilitar usuario")
        print("8. Eliminar usuario")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                id_usu = int(input("ID de usuario (Número): "))
                nombre = input("Nombre: ")
                apellidos = input("Apellidos: ")
                email = input("Email: ")
                hab_input = input("¿Habilitado de inicio? (S/N): ").strip().lower()
                habilitado = hab_input == 's'

                agregar_usuario(id_usu, nombre, apellidos, email, habilitado)
                print(" Operación de registro completada.")
            except ValueError:
                print(" El ID debe ser un número entero.")

        elif opcion == "2":
            print("\n--- Listado de Usuarios ---")
            mostrar_usuarios()

        elif opcion == "3":
            try:
                id_usu = int(input("ID del usuario: "))
                usuario = obtener_usuario(id_usu)
                print(f"\nUsuario encontrado: {usuario}")
            except ValueError:
                print(" El ID debe ser un número entero.")

        elif opcion == "4":
            email = input("Introduce el Email exacto: ")
            usuario = buscar_usuario_por_email(email)
            print(f"\nUsuario encontrado: {usuario}")

        elif opcion == "5":
            nombre = input("Introduce el texto/nombre a buscar: ")
            lista = buscar_usuario_por_nombre_parcial(nombre)
            print(f"\nUsuarios que coinciden:")
            for usu in lista:
                print(usu)

        elif opcion == "6":
            try:
                id_usu = int(input("ID del usuario a habilitar: "))
                if habilitar_usuario(id_usu):
                    print(" Usuario habilitado con éxito.")
                else:
                    print(" No se pudo habilitar al usuario.")
            except ValueError:
                print(" El ID debe ser un número entero.")

        elif opcion == "7":
            try:
                id_usu = int(input("ID del usuario a deshabilitar: "))
                if deshabilitar_usuario(id_usu):
                    print(" Usuario deshabilitado con éxito.")
                else:
                    print(" No se pudo deshabilitar al usuario.")
            except ValueError:
                print(" El ID debe ser un número entero.")

        elif opcion == "8":
            try:
                id_usu = int(input("ID del usuario a eliminar: "))
                filas = eliminar_usuario(id_usu)
                print(f"Filas afectadas: {filas}")
            except ValueError:
                print("El ID debe ser un número entero.")

        elif opcion == "0":
            break
        else:
            print(" Opción no válida.")


def menu_prestamos():
    """Menu secundario del sistema encargado de la parte de prestamos"""

    while True:
        print("\n--- SUBMENÚ: PRÉSTAMOS Y DEVOLUCIONES ---")
        print("1. Prestar un libro")
        print("2. Devolver un libro")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                id_lib = int(input("ID del libro que se va a prestar: "))
                id_usu = int(input("ID del usuario que lo solicita: "))
                resultado = prestar_libro(id_lib, id_usu)
                print(f"Resultado del préstamo: {'Préstamo realizado con éxito' if resultado else 'No se pudo realizar el préstamo'}")
            except ValueError:
                print(" Los IDs deben ser números enteros.")

        elif opcion == "2":
            id_libro = int(input("ID del libro que se va a devolver: "))
            try:
                id_usu = int(input("ID del usuario que lo devuelve: "))
                resultado = devolver_libro(id_libro, id_usu)
                print(f"Resultado de la devolución: {resultado}")
            except ValueError:
                print(" El ID del usuario debe ser un número entero.")

        elif opcion == "0":
            break
        else:
            print(" Opción no válida.")


if __name__ == "__main__":
    menu_principal()