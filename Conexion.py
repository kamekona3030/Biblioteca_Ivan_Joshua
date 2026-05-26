import sqlite3

def getConexion():
    conn=sqlite3.connect("bd/biblioteca.db")
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS biblioteca (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT
    )
    """)

    conn.commit()
    conn.close()
if __name__ == '__main__':
    getConexion()