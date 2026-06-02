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
    if modo == "normal":
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

            add_libro(nuevo_libro)
            ultimo_error = ""
        except Exception as e:
            ultimo_error = str(e)
    else:
        ultimo_error = "modo desconocido"

    _print_comentario("Libro agregado: ", titulo, 1)

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


def devolver_libro(titulo):
    """Cambia el estado de un libro a disponible"""
    global ultimo_error
    libro_dict = buscar_libro(titulo)

    if libro_dict is None:
        _print_comentario("No se encontro el libro", "", 2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"

    if not libro_dict["disponible"]:
        if actualizar_disponibilidad(libro_dict["id"], True):
            ultimo_error = ""
            _print_comentario("Se devolvio el libro", "", 2)
            return "Libro devuelto"
        else:
            return "Error"
    else:
        _print_comentario("El libro ya estaba disponible", "", 2)
        ultimo_error = "Libro ya disponible"
        return "Libro ya disponible"

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