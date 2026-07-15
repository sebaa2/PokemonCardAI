import sqlite3

conexion = sqlite3.connect("database/pokemon.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS historial (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    carta TEXT NOT NULL,

    expansion TEXT NOT NULL,

    similitud REAL NOT NULL,

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente.")