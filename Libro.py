import datetime


class Libro:
    """
    Esta clase se encarga de contener la información de los campos de la base de datos
    """
    def __init__(self, id_libro: int,titulo: str,autor: str,isbn: str,disponible: bool = True,categoria: str = "General"):
        self.id = id_libro
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible
        self.categoria = categoria
        self.fecha_actualizacion = datetime.date.today().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        """
        Convierte la instancia del objeto a un diccionario para que sea compatible con el código de biblioteca
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "disponible": self.disponible,
            "categoria": self.categoria,
            "fecha_ingreso": self.fecha_actualizacion
        }

    def __str__(self):
        """
        Un toString para poder ver el contenido de los libros
        """
        return f"{self.titulo} - {self.autor} ({self.isbn}) - [{self.categoria}] - {self.disponible}"