from DTO.Libro import Libro
from Conexion import getConexion

"""Clase encargada de hacer las llamada y peticiones a la base de datos"""
ultimo_error = ""

def add_libro(libro: Libro):
    """En metodo add libro es el encargado de añadir libros a la base de datos"""
    global ultimo_error
    estado_disponible = 1 if libro.disponible else 0

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO libros (id, titulo, autor, isbn, disponible,  categoria, fecha_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (libro.id, libro.titulo, libro.autor, libro.isbn,
                 estado_disponible,libro.categoria, libro.fecha_actualizacion)
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
            cursor.execute("SELECT id, titulo, autor,isbn, disponible,  categoria FROM libros WHERE id = ?",
                           (id_libro,))
            fila = cursor.fetchone()

        if fila:
            ultimo_error = ""
            return Libro(
                id_libro=fila[0],
                titulo=fila[1],
                autor=fila[2],
                isbn=fila[3],
                disponible=bool(fila[4]),
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
            cursor.execute("SELECT id, titulo, autor,isbn, disponible,  categoria FROM libros")
            filas = cursor.fetchall()

        lista = []
        for fila in filas:
            lista.append(
                Libro(
                    id_libro=fila[0],
                    titulo=fila[1],
                    autor=fila[2],
                    isbn=fila[3],
                    disponible=bool(fila[4]),
                    categoria=fila[5]
                )
            )
        ultimo_error = ""
        return lista
    except Exception as e:
        ultimo_error = str(e)
        return []

def buscar_por_disponibilidad(disponible: bool):
    """Filtra libros diferenciando si están disponibles o prestados """
    estado = 1 if disponible else 0
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, autor, isbn, disponible, categoria FROM libros WHERE disponible = ?",
                           (estado,))
            filas = cursor.fetchall()

        return [Libro(f[0], f[1], f[2], f[3], bool(f[4]), f[5]) for f in filas]
    except Exception:
        return []

def buscar_por_autor(autor: str):
    """Busca libros cuyo autor coincida """
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, autor, isbn, disponible, categoria FROM libros WHERE autor LIKE ?",
                           (f"%{autor}%",))
            filas = cursor.fetchall()

        return [Libro(id_libro=f[0], titulo=f[1], autor=f[2], isbn=f[3], disponible=bool(f[4]), categoria=f[5]) for f in
                filas]
    except Exception:
        return []

def actualizar_disponibilidad(id_libro: int, disponible: bool) :
    """Actualiza el estado de disponibilidad de un libro gracias a su ID"""
    global ultimo_error
    estado = 1 if disponible else 0
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE libros SET disponible = ? WHERE id = ?", (estado, id_libro))
            conn.commit()
            filas_afectadas = cursor.rowcount
        ultimo_error = ""
        return filas_afectadas > 0
    except Exception as e:
        ultimo_error = str(e)
        return False