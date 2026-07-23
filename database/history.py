import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().with_name("pokemon.db")


def _obtener_conexion():
    """Abre la base de datos y garantiza que exista la tabla de historial."""
    conexion = sqlite3.connect(DATABASE_PATH)
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carta TEXT NOT NULL,
            expansion TEXT NOT NULL,
            similitud REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conexion


def guardar_busqueda(carta, expansion, similitud):
    with _obtener_conexion() as conexion:
        conexion.execute(
            """
            INSERT INTO historial(carta, expansion, similitud)
            VALUES (?, ?, ?)
            """,
            (carta, expansion, float(similitud)),
        )


def obtener_historial():
    with _obtener_conexion() as conexion:
        return conexion.execute(
            """
            SELECT carta, expansion, similitud, fecha
            FROM historial
            ORDER BY fecha DESC
            LIMIT 15
            """
        ).fetchall()


def obtener_historial_completo():
    """Obtiene todos los registros para la vista de estadísticas."""
    with _obtener_conexion() as conexion:
        return conexion.execute(
            """
            SELECT carta, expansion, similitud, fecha
            FROM historial
            ORDER BY fecha DESC, id DESC
            """
        ).fetchall()
