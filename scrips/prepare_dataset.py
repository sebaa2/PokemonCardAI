from pathlib import Path
import shutil

# Ubicacion de las imagenes originales
ORIGINAL = Path("../dataset/original")

# Carpeta destino
PROCESSED = Path("../dataset/processed")

PROCESSED.mkdir(parents=True, exist_ok=True)

cantidad = 0

for expansion in ORIGINAL.iterdir():

    if not expansion.is_dir():
        continue

    nombre_set = expansion.name

    for imagen in expansion.iterdir():

        if imagen.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
            continue

        nuevo_nombre = f"{nombre_set}_{imagen.name}"

        shutil.copy2(
            imagen,
            PROCESSED / nuevo_nombre
        )

        cantidad += 1

print(f"Se copiaron {cantidad} imágenes.")