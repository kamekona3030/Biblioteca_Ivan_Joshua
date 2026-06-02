BEGIN TRANSACTION;
CREATE TABLE libros (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    disponible INTEGER NOT NULL DEFAULT 1,
    isbn TEXT,
    categoria TEXT,
    fecha_actualizacion TEXT
);
COMMIT;
