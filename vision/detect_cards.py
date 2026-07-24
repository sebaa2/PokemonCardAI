from pathlib import Path
import shutil
import logging
import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS = PROJECT_ROOT / "results"

OUTPUT_CROPS = RESULTS / "crops"
OUTPUT_DETECTED = RESULTS / "detected"

OUTPUT_CROPS.mkdir(parents=True, exist_ok=True)
OUTPUT_DETECTED.mkdir(parents=True, exist_ok=True)

# Configurar logging
logger = logging.getLogger(__name__)

# Constantes de validación
MIN_ASPECT_RATIO = 0.5  # Cartas deben ser más altas que anchas
MAX_ASPECT_RATIO = 1.2  # Pero no demasiado
MIN_CARTA_AREA = 2000   # Píxeles mínimos para ser una carta válida


def limpiar_resultados():
    """Elimina resultados anteriores."""

    if OUTPUT_CROPS.exists():
        shutil.rmtree(OUTPUT_CROPS)

    OUTPUT_CROPS.mkdir(parents=True)

    if OUTPUT_DETECTED.exists():
        shutil.rmtree(OUTPUT_DETECTED)

    OUTPUT_DETECTED.mkdir(parents=True)


def preparar_imagen(imagen):
    """Convierte la imagen en una máscara apta para detectar cartas."""

    gris = cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gris,
        (7, 7),
        0
    )

    threshold = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        8
    )

    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    threshold = cv2.morphologyEx(
        threshold,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    return gris, threshold


def validar_carta(x, y, w, h, area, area_minima, ancho_imagen, alto_imagen):
    """
    Valida si un contorno detectado es una carta válida.
    
    Returns:
        tuple: (es_válida: bool, razón: str)
    """
    # Validar área mínima
    if area < area_minima:
        return False, f"Área insuficiente ({area:.0f} < {area_minima:.0f})"
    
    # Validar que no ocupe más del 90% de la imagen
    if area > (ancho_imagen * alto_imagen * 0.9):
        return False, "Objeto demasiado grande"
    
    # Validar que el recorte no esté fuera de bounds
    if x < 0 or y < 0 or x + w > ancho_imagen or y + h > alto_imagen:
        return False, "Ubicación fuera de límites"
    
    # Validar dimensiones mínimas
    if w < 50 or h < 50:
        return False, f"Demasiado pequeño ({w}x{h})"
    
    # Validar aspect ratio (cartas Pokémon típicamente 2.3:1)
    aspect_ratio = h / w if w > 0 else 0
    if aspect_ratio < 0.4 or aspect_ratio > 3.5:
        return False, f"Proporción inválida (ratio {aspect_ratio:.1f})"
    
    return True, "OK"


def detectar_cartas(ruta_imagen):

    limpiar_resultados()

    imagen = cv2.imread(str(ruta_imagen))

    if imagen is None:
        raise FileNotFoundError(f"No se puede leer la imagen: {ruta_imagen}")
    
    # Validar que la imagen tenga contenido
    if imagen.size == 0:
        raise ValueError("Imagen vacía o corrupta")

    original = imagen.copy()

    gris, mascara = preparar_imagen(imagen)

    # Guardar imágenes para depuración
    cv2.imwrite(
        str(OUTPUT_DETECTED / "1_grises.png"),
        gris
    )

    cv2.imwrite(
        str(OUTPUT_DETECTED / "2_mascara.png"),
        mascara
    )

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print(f"\nContornos encontrados: {len(contornos)}")

    alto, ancho = imagen.shape[:2]

    area_total = alto * ancho

    area_minima = max(area_total * 0.02, MIN_CARTA_AREA)

    print(f"Área mínima: {area_minima:.2f}")

    cartas = []

    contador = 1

    for i, contorno in enumerate(contornos):

        area = cv2.contourArea(contorno)

        print(f"Contorno {i}: {area:.2f}")

        if area < area_minima:
            continue

        x, y, w, h = cv2.boundingRect(contorno)

        # Validar que la carta sea válida
        es_valida, razon = validar_carta(x, y, w, h, area, area_minima, ancho, alto)
        if not es_valida:
            logger.debug(f"Contorno descartado: {razon}")
            continue

        print(
            f" -> Posición: ({x}, {y}) "
            f"Tamaño: {w}x{h} ✓"
        )
        
        cv2.rectangle(
            imagen,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )
        
        cv2.putText(
            imagen,
            str(contador),
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        recorte = original[
            y:y+h,
            x:x+w
        ]

        ruta = OUTPUT_CROPS / f"carta_{contador}.png"

        cv2.imwrite(
            str(ruta),
            recorte
        )

        cartas.append({
            "id": contador,
            "ruta": ruta,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "area": area
        })

        contador += 1

    # Validar que se detectaron cartas
    if not cartas:
        logger.warning("No se detectaron cartas válidas en la imagen")
        raise ValueError("No se detectaron cartas en la imagen. Intenta con una foto más clara o con mejor iluminación.")

    # Guardar imagen original con rectángulos
    salida = OUTPUT_DETECTED / "detectadas.png"

    cv2.imwrite(
        str(salida),
        imagen
    )

    print(f"\n✓ Cartas detectadas: {len(cartas)}")

    return cartas, salida


if __name__ == "__main__":

    imagen = RESULTS / "temp.png"

    cartas, salida = detectar_cartas(imagen)

    print("\nCartas detectadas:\n")

    for carta in cartas:
        print(carta)

    print("\nImagen generada:")
    print(salida)
