class Prestamo:
    """Representa un préstamo de un libro a un usuario."""

    def __init__(self, id_prestamo=None, libro_id=None, usuario_id=None, 
                 fecha_prestamo=None, fecha_devolucion=None, estado='prestado'):
        self.id_prestamo = id_prestamo
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado

    def __str__(self):
        return f"Prestamo(id={self.id_prestamo}, libro={self.libro_id}, usuario={self.usuario_id}, estado={self.estado})"
