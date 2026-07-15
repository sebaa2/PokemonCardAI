import sqlite3


def guardar_busqueda(carta, expansion, similitud):

    conexion = sqlite3.connect("database/pokemon.db")

    cursor = conexion.cursor()

    cursor.execute("""

        INSERT INTO historial(
            carta,
            expansion,
            similitud
        )

        VALUES(?,?,?)

    """, (

        carta,
        expansion,
        similitud

    ))

    conexion.commit()

    conexion.close()


def obtener_historial():

    conexion = sqlite3.connect("database/pokemon.db")

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT carta,
               expansion,
               similitud,
               fecha
        FROM historial
        ORDER BY fecha DESC
        LIMIT 15
    """)

    historial = cursor.fetchall()

    conexion.close()

    return historial
