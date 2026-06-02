from Usuario import Usuario
from Conexion import getConexion

def add_Usuario(usuario:Usuario):
    global ultimo_error


    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO libros (id_usuario, nombre, apellidos, email, habilitado)
                VALUES (?, ?, ?, ?, ?)
                """,
                (usuario.id, usuario.nombre, usuario.apellidos, usuario.email, usuario.habilitado),
            )
            conn.commit()
            ultimo_error= ""
    except Exception as e:
        ultimo_error = str(e)


def get_Usuario(id_usuario:int):
    global ultimo_error

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, apellidos, email, habilitado FROM usuarios WHERE id = ?",
                           (id_usuario,))
            fila = cursor.fetchone()

        if fila:
            ultimo_error = ""
            return Usuario(
                id_usuario=fila[0],
                nombre=fila[1],
                apellidos=fila[2],
                email=fila[3],
                habilitado=bool(fila[4])
            )

        ultimo_error = "Usuario no encontrado"
        return None
    except Exception as e:
        ultimo_error = str(e)
        return None

def remove_Usuario(id_usuario:int):
    global ultimo_error

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            filas_afectadas = cursor.rowcount
            conn.commit()
        ultimo_error = ""
        return filas_afectadas
    except Exception as e:
        ultimo_error = str(e)
        return 0

def list_all_Usuarios():
    global ultimo_error

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, apellidos, email, habilitado FROM usuarios")
            filas = cursor.fetchall()

            lista = []
            for fila in filas:
                lista.append(
                    Usuario(
                        id_usuario=fila[0],
                        nombre=fila[1],
                        apellidos=fila[2],
                        email=fila[3],
                        habilitado=bool(fila[4]),
                    )
                )

            ultimo_error = ""
            return lista
    except Exception as e:
        ultimo_error = str(e)
        return []
