import sqlite3

def guardar(carta, expansion, similitud):

    conexion = sqlite3.connect("database/historial.db")

    cursor = conexion.cursor()

    cursor.execute("""

    INSERT INTO historial(carta,set_pokemon,similitud)

    VALUES(?,?,?)

    """,(carta, expansion, similitud))

    conexion.commit()

    conexion.close()