class Usuario:
    """
    Esta clase se encarga de contener la información de los campos de la base de datos
    """
    def __init__(self, id_usuario: int, nombre: str, apellidos: str, email: str, habilitado: bool):
        self.id=id_usuario
        self.nombre=nombre
        self.apellidos=apellidos
        self.email=email
        self.habilitado=habilitado
        self.libros_prestados=[]

    def __str__(self):
        """
        Un toString para poder ver el contenido de los usuarios
        """
        return f"{self.id} - {self.nombre} {self.apellidos} - {self.email} - {self.habilitado}"


