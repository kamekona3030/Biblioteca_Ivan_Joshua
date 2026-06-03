from DTO.Prestamo import Prestamo
from Conexion import getConexion

"""DAO encargado de gestionar los préstamos en la base de datos"""
ultimo_error = ""


def registrar_prestamo(libro_id: int, usuario_id: int) -> bool:
    """
    Inserta un nuevo préstamo activo en la tabla prestamos
    """
    global ultimo_error
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo, estado)
                VALUES (?, ?, DATE('now'), 'prestado')
                """,
                (libro_id, usuario_id)
            )
            conn.commit()
        ultimo_error = ""
        return True
    except Exception as e:
        ultimo_error = str(e)
        return False


def registrar_devolucion(libro_id: int, usuario_id: int):
    """
    Registra la devolución de un préstamo activo
    """
    global ultimo_error
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE prestamos
                SET estado = 'devuelto', fecha_devolucion = DATE('now')
                WHERE libro_id = ? AND usuario_id = ? AND estado = 'prestado'
                """,
                (libro_id, usuario_id)
            )
            filas_afectadas = cursor.rowcount
            conn.commit()

        if filas_afectadas > 0:
            ultimo_error = ""
            return True

        ultimo_error = "Préstamo activo no encontrado"
        return False
    except Exception as e:
        ultimo_error = str(e)
        return False


def get_prestamo_activo(libro_id: int, usuario_id: int):
    """
    Obtiene el préstamo activo de un libro para un usuario
    """
    global ultimo_error
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_prestamo, libro_id, usuario_id, fecha_prestamo, fecha_devolucion, estado
                FROM prestamos
                WHERE libro_id = ? AND usuario_id = ? AND estado = 'prestado'
                """,
                (libro_id, usuario_id)
            )
            fila = cursor.fetchone()

        if fila:
            ultimo_error = ""
            return Prestamo(
                id_prestamo=fila[0],
                libro_id=fila[1],
                usuario_id=fila[2],
                fecha_prestamo=fila[3],
                fecha_devolucion=fila[4],
                estado=fila[5]
            )

        ultimo_error = "Préstamo no encontrado"
        return None
    except Exception as e:
        ultimo_error = str(e)
        return None


def list_prestamos_usuario(usuario_id: int):
    """
    Lista todos los préstamos de un usuario.

    """
    global ultimo_error
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_prestamo, libro_id, usuario_id, fecha_prestamo, fecha_devolucion, estado
                FROM prestamos
                WHERE usuario_id = ?
                """,
                (usuario_id,)
            )
            filas = cursor.fetchall()

        ultimo_error = ""
        return [
            Prestamo(
                id_prestamo=f[0],
                libro_id=f[1],
                usuario_id=f[2],
                fecha_prestamo=f[3],
                fecha_devolucion=f[4],
                estado=f[5]
            )
            for f in filas
        ]
    except Exception as e:
        ultimo_error = str(e)
        return []