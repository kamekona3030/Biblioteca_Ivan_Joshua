from Conexion import getConexion

def registrar_log(accion: str):
    """Registra una acción en la base de datos de logs """
    try:
        with getConexion() as conn:
            cursor = conn.cursor()
            # Asegura la existencia de la tabla antes de insertar
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    accion TEXT,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("INSERT INTO logs (accion) VALUES (?)", (accion,))
            conn.commit()
    except Exception as e:
        print(f"Error al registrar log: {e}")