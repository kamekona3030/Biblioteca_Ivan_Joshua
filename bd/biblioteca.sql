BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn TEXT,
    disponible INTEGER NOT NULL DEFAULT 1,
    categoria TEXT DEFAULT 'General',
    fecha_actualizacion TEXT
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT NOT NULL,
    habilitado BOOLEAN NOT NULL DEFAULT 1
);

COMMIT;
