from pathlib import Path
import shutil
import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS = PROJECT_ROOT / "results"

OUTPUT_CROPS = RESULTS / "crops"
OUTPUT_DETECTED = RESULTS / "detected"

OUTPUT_CROPS.mkdir(parents=True, exist_ok=True)
OUTPUT_DETECTED.mkdir(parents=True, exist_ok=True)


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


def detectar_cartas(ruta_imagen):

    limpiar_resultados()

    imagen = cv2.imread(str(ruta_imagen))

    if imagen is None:
        raise FileNotFoundError(ruta_imagen)

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

    area_minima = area_total * 0.02

    print(f"Área mínima: {area_minima:.2f}")

    cartas = []

    contador = 1

    for i, contorno in enumerate(contornos):

        area = cv2.contourArea(contorno)

        print(f"Contorno {i}: {area:.2f}")

        if area < area_minima:
            continue

        x, y, w, h = cv2.boundingRect(contorno)

        print(
            f" -> Posición: ({x}, {y}) "
            f"Tamaño: {w}x{h}"
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
            (x,y -10),
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

    # Guardar imagen original (todavía sin rectángulos)
    salida = OUTPUT_DETECTED / "detectadas.png"

    cv2.imwrite(
        str(salida),
        imagen
    )

    return cartas, salida


if __name__ == "__main__":

    imagen = RESULTS / "temp.png"

    cartas, salida = detectar_cartas(imagen)

    print("\nCartas detectadas:\n")

    for carta in cartas:
        print(carta)

    print("\nImagen generada:")
    print(salida)
