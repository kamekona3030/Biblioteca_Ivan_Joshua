from DAO import PrestamoDAO
from Usuario import Usuario
from DAO import UsuarioDAO
from datetime import datetime
from Libro import Libro
from DAO.LibroDAO import (add_libro,get_libro,
                          remove_libro,list_all,buscar_por_autor,
                          buscar_por_disponibilidad,actualizar_disponibilidad)

"""Clase encargada de la gestión de los metodos"""
modo = "normal"
ultimo_error = ""

def _print_comentario(comentario, comentario_extra="", tipo_comentario=0):
    if tipo_comentario == 1:
        print(comentario + comentario_extra)
    elif tipo_comentario == 2:
        print(comentario)
    else:
        print(str(comentario))

def agregar_libro(titulo, autor):
    """Crea y registra un nuevo libro en la base de datos"""
    global ultimo_error
    if modo != "normal":
        ultimo_error = "modo desconocido"
        _print_comentario("Modo de operación no soportado", "", 2)
        return
    try:
        libros_actuales = list_all()
        nuevo_id = max([l.id for l in libros_actuales], default=0) + 1

        nuevo_libro = Libro(
            id_libro=nuevo_id,
            titulo=titulo,
            autor=autor,
            isbn="000-00000-0",
            disponible=True,
            categoria="General"
        )

        nuevo_libro.id = nuevo_id
        nuevo_libro.fecha_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_libro(nuevo_libro)
        from DAO import LibroDAO
        if LibroDAO.ultimo_error:
            ultimo_error = LibroDAO.ultimo_error
            _print_comentario(f" Error en el DAO: {ultimo_error}", "", 2)
        else:
            ultimo_error = ""
            _print_comentario("Libro agregado: ", titulo, 1)
    except Exception as e:
        ultimo_error = str(e)
        _print_comentario(f" Error en gestión: {e}", "", 2)


def borrar_libro(id_libro: int):
    """Elimina un libro por su ID"""
    global ultimo_error
    try:
        filas_eliminadas = remove_libro(id_libro)
        ultimo_error = ""
        if filas_eliminadas > 0:
            _print_comentario(f"Libro con ID {id_libro} eliminado.", "", 2)
        else:
            ultimo_error = "Libro no encontrado"
        return filas_eliminadas
    except Exception as e:
        ultimo_error = str(e)
        return 0

def _verificar_libro(libro, titulo):
    if "titulo" in libro:
        return libro.get("titulo") == titulo
    return False

def buscar_libro(titulo):
    """Busca un libro por su título. Devuelve el diccionario del libro o None"""
    for libro_objeto in list_all():
        libro_dict = libro_objeto.to_dict()
        if _verificar_libro(libro_dict, titulo):
            return libro_dict
    return None


def prestar_libro(titulo):
    """Cambia el estado de un libro a 'prestado' si está disponible"""
    global ultimo_error
    libro_dict = buscar_libro(titulo)

    if libro_dict is None:
        _print_comentario("No se ha encontrado el libro", "", 2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"

    if libro_dict["disponible"]:
        if actualizar_disponibilidad(libro_dict["id"], False):
            ultimo_error = ""
            _print_comentario("Se presto el libro", "", 2)
            return "Libro prestado"
        else:
            return "Error"
    else:
        _print_comentario("El libro no esta disponible", "", 2)
        ultimo_error = "Libro no disponible"
        return "Libro no disponible"


def devolver_libro(titulo: str, usuario_id: int):
    """
    Registra la devolución de un libro prestado.

    Busca el libro por título, verifica que esté prestado, actualiza su
    disponibilidad a True y registra la devolución en la tabla de préstamos.
    """
    global ultimo_error
    libro_dict = buscar_libro(titulo)

    if libro_dict is None:
        _print_comentario("No se encontro el libro", "", 2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"

    if libro_dict["disponible"]:
        _print_comentario("El libro ya estaba disponible", "", 2)
        ultimo_error = "Libro ya disponible"
        return "Libro ya disponible"

    prestamo = PrestamoDAO.get_prestamo_activo(libro_dict["id"], usuario_id)
    if prestamo is None:
        _print_comentario("No se encontro un prestamo activo para este usuario", "", 2)
        ultimo_error = "Préstamo no encontrado"
        return "Préstamo no encontrado"

    if not actualizar_disponibilidad(libro_dict["id"], True):
        ultimo_error = "Error al actualizar disponibilidad"
        return "Error"

    if not PrestamoDAO.registrar_devolucion(libro_dict["id"], usuario_id):
        ultimo_error = PrestamoDAO.ultimo_error
        return "Error"

    ultimo_error = ""
    _print_comentario("Se devolvio el libro", "", 2)
    return "Libro devuelto"


def _obtener_estado(libro):
    if libro["disponible"]:
        return "Disponible"
    return "Prestado"

def mostrar_libros():
    """Imprime en consola la lista completa de libros registrados"""
    try:
        libros_bd = list_all()
        if len(libros_bd) == 0:
            _print_comentario("No hay libros", "", 2)
        else:
            for libro in libros_bd:
                print(libro)
    except Exception as e:
        _print_comentario(f"Error al listar: {e}", "", 2)

def agregar_usuario(id_usuario: int, nombre: str, apellidos: str, email: str, habilitado: bool):
    global ultimo_error
    nuevo_usuariio = Usuario(id_usuario, nombre, apellidos, email, habilitado)
    UsuarioDAO.add_Usuario(nuevo_usuariio)
    ultimo_error = UsuarioDAO.ultimo_error

def obtener_usuario(id_usuario: int):
    global ultimo_error
    usuario = UsuarioDAO.get_Usuario(id_usuario)
    ultimo_error = UsuarioDAO.ultimo_error
    return usuario

def eliminar_usuario(id_usuario: int):
    global ultimo_error
    filas = UsuarioDAO.remove_Usuario(id_usuario)
    ultimo_error = UsuarioDAO.ultimo_error
    return filas

def mostrar_usuarios():
    global ultimo_error
    lista_usuarios = UsuarioDAO.list_all_Usuarios()
    ultimo_error = UsuarioDAO.ultimo_error
    if len(lista_usuarios) == 0:
        _print_comentario("No hay usuarios", "", 2)
    else:
        for usuario in lista_usuarios:
            print(usuario)

def buscar_usuario_por_email(email: str):
    global ultimo_error
    usuario = UsuarioDAO.buscar_por_email(email)
    ultimo_error = UsuarioDAO.ultimo_error
    return usuario

def buscar_usuario_por_nombre_parcial(nombre: str):
    global ultimo_error
    lista = UsuarioDAO.buscar_por_nombre_parcial(nombre)
    ultimo_error = UsuarioDAO.ultimo_error
    return lista


def habilitar_usuario(id_usuario: int):
    global ultimo_error
    resultado = UsuarioDAO.habilitar_usuario(id_usuario)
    ultimo_error = UsuarioDAO.ultimo_error
    return resultado

def deshabilitar_usuario(id_usuario: int):
    global ultimo_error
    resultado = UsuarioDAO.deshabilitar_usuario(id_usuario)
    ultimo_error = UsuarioDAO.ultimo_error
    return resultado

def buscar_libros_por_disponibilidad(disponible: bool):
    """Llama al DAO para obtener libros por el estado y los convierte en diccionario"""
    global ultimo_error
    try:
        resultados = buscar_por_disponibilidad(disponible)
        ultimo_error = ""
        return [libro.to_dict() for libro in resultados]
    except Exception as e:
        ultimo_error = str(e)
        return []

def buscar_libros_por_autor(autor: str):
    """Llama al DAO para obtener los libros que coincidan con el autor"""
    global ultimo_error
    try:
        resultados = buscar_por_autor(autor)
        ultimo_error = ""
        return [libro.to_dict() for libro in resultados]
    except Exception as e:
        ultimo_error = str(e)
        return []

def buscar_libros_por_ID(id_libro: int):
    """Busca un libro por su ID y lo devuelve como diccionario"""
    global ultimo_error
    try:
        libro_obj = get_libro(id_libro)
        if libro_obj:
            ultimo_error = ""
            return libro_obj.to_dict()
        ultimo_error = "Libro no encontrado"
        return None
    except Exception as e:
        ultimo_error = str(e)
        return None
