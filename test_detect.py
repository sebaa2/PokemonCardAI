from pathlib import Path

from vision.detect_cards import detectar_cartas

PROJECT_ROOT = Path(__file__).resolve().parent

imagen = PROJECT_ROOT / "results" / "temp.png"

cartas, salida = detectar_cartas(imagen)

print("\nCartas encontradas:")

for carta in cartas:
    print(carta)

print("\nImagen con detecciones:")
print(salida)