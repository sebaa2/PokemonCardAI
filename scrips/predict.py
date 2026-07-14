import json
import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input
)

from tensorflow.keras.preprocessing import image

from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

IMG_SIZE = (224, 224)

""" revisar el parametro nombre_archivo """


def obtener_info(nombre_archivo):

    nombre = Path(nombre_archivo).stem

    partes = nombre.split("_")

    expansion = partes[0]

    datos = partes[-1]

    datos = datos.replace("-", " ")

    pokemon = datos.split()[-1]

    codigo = datos.replace(pokemon, "").strip()

    return {
        "expansion": expansion,
        "codigo": codigo,
        "pokemon": pokemon.title()
    }


model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

embeddings = np.load(
    "../dataset/embeddings/pokemon_embeddings.npy"
)

with open(
    "../dataset/embeddings/card_names.json",
    encoding="utf8"
) as f:

    nombres = json.load(f)

# -------------------------

foto = "../results/prueba.png"

img = image.load_img(
    foto,
    target_size=IMG_SIZE
)

x = image.img_to_array(img)

x = np.expand_dims(x, axis=0)

x = preprocess_input(x)

vector = model.predict(x, verbose=0)

similaridad = cosine_similarity(
    vector,
    embeddings
)[0]


# Obtener las 5 mejores coincidencias
top5 = np.argsort(similaridad)[::-1][:5]

print("\n========== TOP 5 CARTAS ==========\n")

for posicion, indice in enumerate(top5, start=1):

    expansion, codigo, pokemon = obtener_info(nombres[indice])

    porcentaje = similaridad[indice] * 100

    print("="*40)
    print(f"Top {posicion}")
    print("="*40)
    print("Carta :", pokemon)
    print("Set   :", expansion)
    print("Código:", codigo)
    print(f"Similitud: {porcentaje:.2f}%")
    print()

""" indice = np.argmax(similaridad)

print("----------------------")
print("Carta encontrada")
print("----------------------")
print(nombres[indice])
print(f"Similitud: {similaridad[indice]*100:.2f}%") """
