from DTO.Usuario import Usuario
from Conexion import getConexion

ultimo_error = ""

def add_Usuario(usuario:Usuario):
    """El metodo add usuario es el encargado de añadir usuarios a la base de datos"""

    global ultimo_error

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuarios (id_usuario, nombre, apellidos, email, habilitado)
                VALUES (?, ?, ?, ?, ?)
                """,
                (usuario.id, usuario.nombre, usuario.apellidos, usuario.email, usuario.habilitado),
            )
            conn.commit()
            ultimo_error = ""
            return 1
    except Exception as e:
        ultimo_error = str(e)
        return 0


def get_Usuario(id_usuario:int):
    """El metodo get usuario sirve para pedirle a la base de datos los datos de un usuario"""

    global ultimo_error

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, apellidos, email, habilitado FROM usuarios WHERE id_usuario = ?",
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
    """El metodo remove es el encargado de eliminar los usuarios de la base de datos"""

    global ultimo_error

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
            filas_afectadas = cursor.rowcount
            conn.commit()
        ultimo_error = ""
        return filas_afectadas
    except Exception as e:
        ultimo_error = str(e)
        return 0

def list_all_Usuarios():
    """list_all_Usuarios da una lista de todos los usuarios que hay en la base de datos"""
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


def buscar_por_email(email: str):
    """Filtra usuarios por su email"""

    global ultimo_error


    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, apellidos, email, habilitado FROM usuarios WHERE email = ?",
                           (email,))
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
        ultimo_error = "Email no encontrado"
        return None

    except Exception as e:
        ultimo_error = str(e)
        return None

def buscar_por_nombre_parcial(nombre: str):
    """Filtra usuarios por su nombre o apellidos"""
    global ultimo_error


    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            termino_busqueda = f"%{nombre}%"
            cursor.execute(
                """
                SELECT id_usuario, nombre, apellidos, email, habilitado
                FROM usuarios
                WHERE nombre LIKE ?
                   OR apellidos LIKE ?
                """,
                (termino_busqueda, termino_busqueda)
            )

            filas = cursor.fetchall()
            lista = []
            for fila in filas:
                lista.append(
                    Usuario(
                        id_usuario=fila[0],
                        nombre=fila[1],
                        apellidos=fila[2],
                        email=fila[3],
                        habilitado=bool(fila[4])
                    )
                )

            ultimo_error = ""
            return lista
    except Exception as e:
        ultimo_error = str(e)
        return []


def cambiar_estado (id_usuario:int, habilitar:bool) -> bool:
    """Cambia el estado de un usuario gracias a su id"""
    global ultimo_error

    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            estado_int = 1 if habilitar else 0
            cursor.execute(
                "UPDATE usuarios SET habilitado = ? WHERE id_usuario = ?",
                (estado_int, id_usuario)
            )
            filas_afectadas = cursor.rowcount
            conn.commit()

        if filas_afectadas > 0:
            ultimo_error = ""
            return True

        ultimo_error = "Usuario no encontrado"
        return False
    except Exception as e:
        ultimo_error = str(e)
        return False


def habilitar_usuario(id_usuario:int) -> bool:
    """Llama a cambiar estado para habilitar un usuario segun su id"""
    return cambiar_estado(id_usuario, True)


def deshabilitar_usuario(id_usuario:int) -> bool:
    """Llama a cambiar estado para deshabilitar un usuario segun su id"""
    return cambiar_estado(id_usuario, False)


