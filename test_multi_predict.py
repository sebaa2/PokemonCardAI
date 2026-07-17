from pathlib import Path

from vision.mutli_predict import analizar_imagen

PROJECT_ROOT = Path(__file__).resolve().parent

imagen = PROJECT_ROOT / "results" / "temp.png"

resultados, salida = analizar_imagen(imagen)

print("\n=========== RESULTADOS ===========\n")

for carta in resultados:

    print(f"Carta #{carta['id']}")
    print(f"Posición : ({carta['x']}, {carta['y']})")
    print(f"Archivo  : {carta['ruta']}")

    mejor = carta["coincidencias"][0]

    print(f"Detectada: {mejor['carta']}")
    print(f"Set      : {mejor['set']}")
    print(f"Similitud: {mejor['similitud']}%")

    print("-" * 50)

print("\nImagen detectada:")
print(salida)