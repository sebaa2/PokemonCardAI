import sqlite3

conexion = sqlite3.connect("database/historial.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS historial(

id INTEGER PRIMARY KEY AUTOINCREMENT,

carta TEXT,

set_pokemon TEXT,

similitud REAL,

fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conexion.commit()
conexion.close()