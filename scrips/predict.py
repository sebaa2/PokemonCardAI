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

    if len(partes) < 3:
        return (
            "Desconocido",
            "Desconocido",
            nombre
        )

    expansion = partes[0]

    codigo = partes[1]

    pokemon = " ".join(partes[2:])
    pokemon = pokemon.replace("-", " ").title()

    return expansion, codigo, pokemon


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


def generar_embedding(ruta_imagen):

    img = image.load_img(
        ruta_imagen,
        target_size=IMG_SIZE
    )

    x = image.img_to_array(img)

    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)

    vector = model.predict(
        x,
        verbose=0
    )

    return vector


def buscar_cartas(ruta_imagen, cantidad=5):

    vector = generar_embedding(ruta_imagen)

    similitud = cosine_similarity(
        vector,
        embeddings
    )[0]

    indices = np.argsort(similitud)[::-1][:cantidad]

    resultados = []

    for indice in indices:

        expansion, codigo, pokemon = obtener_info(
            nombres[indice]
        )

        resultados.append({

            "carta": pokemon,

            "set": expansion,

            "codigo": codigo,

            "similitud": round(
                similitud[indice]*100,
                2
            ),

            "archivo": nombres[indice]

        })

    return resultados


# Obtener las 5 mejores coincidencias
if __name__ == "__main__":

    resultados = buscar_cartas(
        "../results/prueba.png"
    )

    print("\n========== TOP 5 CARTAS ==========\n")

    for posicion, carta in enumerate(resultados, start=1):

        print("="*40)

        print(f"Top {posicion}")

        print("="*40)

        print("Carta :", carta["carta"])

        print("Set   :", carta["set"])

        print("Código:", carta["codigo"])

        print(
            f"Similitud: {carta['similitud']}%"
        )

        print()

# Bloque de diagnóstico comentado anteriormente
# indice = np.argmax(similaridad)
#
# print("----------------------")
# print("Carta encontrada")
# print("----------------------")
# print(nombres[indice])
# print(f"Similitud: {similaridad[indice]*100:.2f}%")
