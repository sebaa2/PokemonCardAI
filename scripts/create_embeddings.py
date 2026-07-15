from pathlib import Path
import numpy as np
import json

from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input
)

from tensorflow.keras.preprocessing import image

# --------------------------

IMG_SIZE = (224,224)

DATASET = Path("../dataset/processed")

EMBEDDINGS = Path("../dataset/embeddings")

EMBEDDINGS.mkdir(exist_ok=True)

# --------------------------

print("Cargando MobileNetV2...")

model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

vectores = []
nombres = []

imagenes = list(DATASET.glob("*"))

print(f"{len(imagenes)} imágenes encontradas.")

for i, img_path in enumerate(imagenes):

    img = image.load_img(img_path, target_size=IMG_SIZE)

    x = image.img_to_array(img)

    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)

    embedding = model.predict(x, verbose=0)[0]

    vectores.append(embedding)

    nombres.append(img_path.name)

    if (i+1) % 500 == 0:
        print(f"{i+1} imágenes procesadas")

vectores = np.array(vectores)

np.save(
    EMBEDDINGS/"pokemon_embeddings.npy",
    vectores
)

with open(
    EMBEDDINGS/"card_names.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        nombres,
        f,
        ensure_ascii=False,
        indent=4
    )

print("Embeddings creados correctamente.")