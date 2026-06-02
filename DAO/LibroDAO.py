from Libro import Libro
from Conexion import getConexion

def add_libro(libro: Libro):
    """En metodo add libro es el encargado de añadir libros a la base de datos"""
    global ultimo_error
    estado_disponible = 1 if libro.disponible else 0

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO libros (id, titulo, autor, disponible, isbn, categoria, fecha_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (libro.id, libro.titulo, libro.autor, estado_disponible,
                 libro.isbn, libro.categoria, libro.fecha_actualizacion)
            )
            conn.commit()
        ultimo_error = ""
    except Exception as e:
        ultimo_error = str(e)

def remove_libro(id_libro: int):
    """El metodo remove es el encargado de eliminar los libros de la base de datos"""

    global ultimo_error
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
            filas_afectadas = cursor.rowcount
            conn.commit()
        ultimo_error = ""
        return filas_afectadas
    except Exception as e:
        ultimo_error = str(e)
        return 0

def get_libro(id_libro: int):
    """El metodo get libro sirve para pedirle a la base de datos los datos de un libro"""

    global ultimo_error
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, autor, disponible, isbn, categoria FROM libros WHERE id = ?",
                           (id_libro,))
            fila = cursor.fetchone()

        if fila:
            ultimo_error = ""
            return Libro(
                id_libro=fila[0],
                titulo=fila[1],
                autor=fila[2],
                disponible=bool(fila[3]),
                isbn=fila[4],
                categoria=fila[5]
            )
        ultimo_error = "Libro no encontrado"
        return None
    except Exception as e:
        ultimo_error = str(e)
        return None

def list_all():
    """List_all da una lista de todos los libros que hay en la base de datos"""

    global ultimo_error
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, autor, disponible, isbn, categoria FROM libros")
            filas = cursor.fetchall()

        lista = []
        for fila in filas:
            lista.append(
                Libro(
                    id_libro=fila[0],
                    titulo=fila[1],
                    autor=fila[2],
                    disponible=bool(fila[3]),
                    isbn=fila[4],
                    categoria=fila[5]
                )
            )
        ultimo_error = ""
        return lista
    except Exception as e:
        ultimo_error = str(e)
        return []