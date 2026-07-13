from pathlib import Path
import shutil

# Carpeta donde está el dataset original
ORIGINAL = Path("../dataset/original")

# Carpeta donde se copiarán todas las imágenes
PROCESSED = Path("../dataset/processed")

PROCESSED.mkdir(parents=True, exist_ok=True)

copiadas = 0
omitidas = 0

for expansion in ORIGINAL.iterdir():

    if not expansion.is_dir():
        continue

    for imagen in expansion.iterdir():

        if imagen.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
            continue

        nuevo_nombre = f"{expansion.name}_{imagen.name}"

        destino = PROCESSED / nuevo_nombre

        if destino.exists():
            omitidas += 1
            continue

        shutil.copy2(imagen, destino)
        copiadas += 1

print("=" * 40)
print("Preparación del dataset finalizada")
print("=" * 40)
print(f"Nuevas imágenes copiadas: {copiadas}")
print(f"Imágenes ya existentes: {omitidas}")