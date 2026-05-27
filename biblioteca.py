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


def cambiar_estado_libro(tipo_movimiento, libro):
    if tipo_movimiento == "prestamo":
        libro["disponible"] = False
        _print_comentario("Se presto el libro", "", 2)
        return "Libro prestado"
    if tipo_movimiento == "devolucion":
        libro["disponible"] = True
        _print_comentario("Se devolvio el libro", "", 2)
        return "Libro devuelto"
    return "Nada"


def agregar_libro(titulo, autor):
    global ultimo_error
    datos_libro = []
    datos_libro.append(titulo)
    datos_libro.append(autor)
    diccionario_libro = {}

    for i in range(0, len(datos_libro)):
        if i == 0:
            diccionario_libro["titulo"] = datos_libro[i]
        else:
            if i == 1:
                diccionario_libro["autor"] = datos_libro[i]

    diccionario_libro["disponible"] = not False
    if modo == "normal" or modo != "normal":
        lista_libros.append(diccionario_libro)
        ultimo_error = ""
    else:
        ultimo_error = "modo desconocido"

    _print_comentario("Libro agregado: ", titulo, 1)


def buscar_libro(titulo):
    indice = 0
    encontrado = None
    seguir = True
    while seguir:
        if indice >= len(lista_libros):
            seguir = False
        else:
            libro = lista_libros[indice]
            if ("titulo" in libro) == True:
                if libro.get("titulo") == titulo:
                    encontrado = libro
                    seguir = False
                else:
                    indice = indice + 1
            else:
                indice = indice + 1
    return encontrado


def prestar_libro(titulo):
    global ultimo_error
    resultado = "Libro no encontrado"
    indice = 0
    while indice < len(lista_libros):
        libro = lista_libros[indice]
        if libro["titulo"] == titulo:
            if libro["disponible"] == True:
                resultado = cambiar_estado_libro("prestamo", libro)
                ultimo_error = ""
                indice = len(lista_libros) + 100
            else:
                _print_comentario("El libro no esta disponible", "", 2)
                resultado = "Libro no disponible"
                ultimo_error = resultado
                indice = len(lista_libros) + 100
        else:
            indice = indice + 1

    if resultado == "Libro no encontrado":
        _print_comentario("No se encontro el libro", "", 2)
        ultimo_error = resultado

    return resultado


def devolver_libro(titulo):
    global ultimo_error
    libro = buscar_libro(titulo)
    if libro is None:
        _print_comentario("No se encontro el libro", "", 2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"
    else:
        if libro["disponible"] == False:
            ultimo_error = ""
            return cambiar_estado_libro("devolucion", libro)
        else:
            if libro["disponible"] != False:
                _print_comentario("El libro ya estaba disponible", "", 2)
                ultimo_error = "Libro ya disponible"
                return "Libro ya disponible"


def mostrar_libros():
    indice = 0
    if len(lista_libros) == 0:
        _print_comentario("No hay libros", "", 2)
    else:
        while indice < len(lista_libros):
            libro = lista_libros[indice]
            estado = ""
            if libro["disponible"] == True:
                estado = estado + "Disponible"
            else:
                if libro["disponible"] == False:
                    estado = estado + "Prestado"
            salida = ""
            partes = [libro["titulo"], libro["autor"], estado]
            for parte in partes:
                if salida == "":
                    salida = parte
                else:
                    salida = salida + " - " + parte
            print(salida)
            indice = indice + 1
