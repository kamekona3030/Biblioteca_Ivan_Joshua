class Usuario:
    def __init__(self, id_usuario: int, nombre: str, apellidos: str, email: str, habilitado: bool):
        self.id=id_usuario
        self.nombre=nombre
        self.apellidos=apellidos
        self.email=email
        self.habilitado=habilitado
        self.libros_prestados=[]



def __str__(self):
    return f"{self.id} - {self.nombre} {self.apellidos} - {self.email} - {self.habilitado}"


