BEGIN TRANSACTION;
-- biblioteca.sql
DROP TABLE IF EXISTS libros;
CREATE TABLE libros (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    disponible INTEGER NOT NULL DEFAULT 1,
    isbn TEXT,
    categoria TEXT,
    fecha_actualizacion TEXT
);

DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT NOT NULL,
    habilitado BOOLEAN NOT NULL
);
CREATE TABLE IF NOT EXISTS biblioteca (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT
);
COMMIT;