from vision.detect_cards import detectar_cartas
from ml.predict import buscar_cartas


def analizar_imagen(ruta_imagen, top=5):
    """
    Analiza una imagen para detectar cartas Pokémon y buscar
    las más parecidas en el dataset.
    """

    # Detectar cartas en la imagen
    cartas, imagen_detectada = detectar_cartas(ruta_imagen)

    resultados = []

    for carta in cartas:
        coincidencias = buscar_cartas(
            carta["ruta"],
            cantidad=top
        )

        resultados.append({
            "id": carta["id"],
            "ruta": carta["ruta"],
            "x": carta["x"],
            "y": carta["y"],
            "w": carta["w"],
            "h": carta["h"],
            "coincidencias": coincidencias
        })

        return resultados, imagen_detectada
