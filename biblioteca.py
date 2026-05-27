libros = []
lista_libros = libros
modo = "normal"
ultimo_error = ""


def _print_comentario(comentario, comentario_extra="", tipo_comentario=0):
    if tipo_comentario == 1:
        print(comentario + comentario_extra)
    elif tipo_comentario == 2:
        print(comentario)
    else:
        print(str(comentario))


def _cambiar_estado_libro(tipo_movimiento, libro):
    if tipo_movimiento == "prestamo":
        libro["disponible"] = False
        _print_comentario("Se presto el libro", "", 2)
        return "Libro prestado"
    if tipo_movimiento == "devolucion":
        libro["disponible"] = True
        _print_comentario("Se devolvio el libro", "", 2)
        return "Libro devuelto"
    return "Nada"

def crear_diccionario_libro(titulo, autor):
    return {
        "titulo": titulo,
        "autor": autor,
        "disponible": True
    }

def agregar_libro(titulo, autor):
    global ultimo_error
    diccionario_libro = crear_diccionario_libro(titulo, autor)

    if modo == "normal":
        lista_libros.append(diccionario_libro)
        ultimo_error = ""
    else:
        ultimo_error = "modo desconocido"

    _print_comentario("Libro agregado: ", titulo, 1)

def _verificar_libro(libro, titulo):
    if "titulo" in libro:
        return libro.get("titulo") == titulo
    return False

def buscar_libro(titulo):
    for libro in lista_libros:
        if (_verificar_libro(libro,titulo)):
            return libro

    return None

def _comprobar_estado_libro(libro):
    global ultimo_error
    if libro["disponible"]:
        resultado = _cambiar_estado_libro("prestamo", libro)
        ultimo_error=""
        return  resultado
    else:
        _print_comentario("El libro no esta disponible","", 2)
        resultado = "Libro no disponible"
        ultimo_error = resultado
        return resultado

def prestar_libro(titulo):
    global ultimo_error
    resultado = "Libro no encontrado"

    for libro in lista_libros:
        if libro["titulo"] == titulo:
            return _comprobar_estado_libro(libro)

    _print_comentario("No se ha encontrado el libro","",2)
    ultimo_error = "Libro no encontrado"
    return "Libro no encontrado"

def _comprobar_estado_libro_devolucion(libro):
    global ultimo_error
    if not libro["disponible"]:
        ultimo_error = ""
        return _cambiar_estado_libro("devolucion", libro)
    else:
        _print_comentario("El libro ya estaba disponible", "", 2)
        ultimo_error = "Libro ya disponible"
        return "Libro ya disponible"

def devolver_libro(titulo):
    global ultimo_error
    libro = buscar_libro(titulo)
    if libro is None:
        _print_comentario("No se encontro el libro", "", 2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"
    else:
        return _comprobar_estado_libro_devolucion(libro)

def _obtener_estado(libro):
    if libro["disponible"]:
        return "Disponible"
    return "Prestado"

def mostrar_libros():
    if len(lista_libros) == 0:
        _print_comentario("No hay libros", "", 2)
    else:
        for libro in lista_libros:
            estado = _obtener_estado(libro)
            salida = ""
            partes = [libro["titulo"], libro["autor"], estado]

            for parte in partes:
                if salida == "":
                    salida = parte
                else:
                    salida = salida + " - " + parte
            print(salida)