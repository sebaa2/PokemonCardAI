import json
import sys
from pathlib import Path

# Permite ejecutar este archivo directamente con `python -m scripts.predict`
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input
)
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

from database.history import guardar_busqueda

IMG_SIZE = (224, 224)


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


print("Cargando modelo...")
model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

print("Cargando embeddings...")
embeddings = np.load(
    PROJECT_ROOT / "dataset" / "embeddings" / "pokemon_embeddings.npy"
)

with open(
    PROJECT_ROOT / "dataset" / "embeddings" / "card_names.json",
    encoding="utf8"
) as f:
    nombres = json.load(f)


def generar_embedding(ruta_imagen):
    img = image.load_img(
        ruta_imagen,
        target_size=IMG_SIZE
    )

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    return model.predict(
        x,
        verbose=0
    )


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
                similitud[indice] * 100,
                2
            ),

            "archivo": nombres[indice]

        })

    return resultados


if __name__ == "__main__":

    imagen = PROJECT_ROOT / "results" / "prueba.png"

    resultados = buscar_cartas(imagen)

    # Guardar únicamente el mejor resultado
    guardar_busqueda(
        resultados[0]["carta"],
        resultados[0]["set"],
        resultados[0]["similitud"]
    )

    print("\n========== TOP 5 ==========\n")

    for i, carta in enumerate(resultados, start=1):

        print("=" * 40)
        print(f"Top {i}")
        print("=" * 40)
        print(f"Carta     : {carta['carta']}")
        print(f"Set        : {carta['set']}")
        print(f"Código     : {carta['codigo']}")
        print(f"Similitud  : {carta['similitud']}%")
        print()