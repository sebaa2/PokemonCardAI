import json
from pathlib import Path
import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input
)
from tensorflow.keras.preprocessing import image

# -----------------------------
# Rutas
# -----------------------------
PROCESSED = Path("../dataset/processed")
EMBEDDINGS_DIR = Path("../dataset/embeddings")

INDEX = EMBEDDINGS_DIR / "processed_index.json"
CARD_NAMES = EMBEDDINGS_DIR / "card_names.json"
EMBEDDINGS = EMBEDDINGS_DIR / "pokemon_embeddings.npy"

IMG_SIZE = (224, 224)

# -----------------------------
# Cargar índice
# -----------------------------
with open(INDEX, encoding="utf8") as f:
    procesadas = set(json.load(f))

# -----------------------------
# Buscar imágenes nuevas
# -----------------------------
imagenes = list(PROCESSED.glob("*"))

nuevas = [img for img in imagenes if img.name not in procesadas]

print(f"Nuevas cartas encontradas: {len(nuevas)}")

if len(nuevas) == 0:
    print("No hay cartas nuevas.")
    exit()

# -----------------------------
# Cargar modelo
# -----------------------------
print("Cargando MobileNetV2...")

model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

# -----------------------------
# Crear nuevos embeddings
# -----------------------------
nuevos_embeddings = []

for i, img_path in enumerate(nuevas):

    img = image.load_img(img_path, target_size=IMG_SIZE)

    x = image.img_to_array(img)

    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)

    embedding = model.predict(x, verbose=0)[0]

    nuevos_embeddings.append(embedding)

    if (i + 1) % 100 == 0:
        print(f"{i+1}/{len(nuevas)} procesadas")

nuevos_embeddings = np.array(nuevos_embeddings)

# -----------------------------
# Cargar embeddings existentes
# -----------------------------
embeddings = np.load(EMBEDDINGS)

embeddings = np.vstack([embeddings, nuevos_embeddings])

np.save(EMBEDDINGS, embeddings)

# -----------------------------
# Actualizar nombres
# -----------------------------
with open(CARD_NAMES, encoding="utf8") as f:
    nombres = json.load(f)

for img in nuevas:
    nombres.append(img.name)

with open(CARD_NAMES, "w", encoding="utf8") as f:
    json.dump(nombres, f, indent=4)

# -----------------------------
# Actualizar índice
# -----------------------------
procesadas.update(img.name for img in nuevas)

with open(INDEX, "w", encoding="utf8") as f:
    json.dump(sorted(list(procesadas)), f, indent=4)

print("\nEmbeddings actualizados correctamente.")