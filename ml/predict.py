import json
import sys
import logging
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

# Configurar logging
logger = logging.getLogger(__name__)

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
    """
    Genera un embedding para una imagen.
    
    Raises:
        FileNotFoundError: Si la imagen no existe
        ValueError: Si la imagen es inválida o el embedding contiene NaN
    """
    if not Path(ruta_imagen).exists():
        raise FileNotFoundError(f"Imagen no encontrada: {ruta_imagen}")
    
    try:
        img = image.load_img(
            ruta_imagen,
            target_size=IMG_SIZE
        )
    except Exception as e:
        logger.error(f"Error cargando imagen {ruta_imagen}: {str(e)}")
        raise ValueError(f"Imagen corrupta o inválida: {str(e)}")

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    embedding = model.predict(x, verbose=0)
    
    # Validar que el embedding es válido
    if embedding is None or embedding.size == 0:
        raise ValueError("Embedding vacío o inválido")
    
    if np.isnan(embedding).any() or np.isinf(embedding).any():
        raise ValueError("Embedding contiene valores NaN o Inf")
    
    return embedding


def buscar_cartas(ruta_imagen, cantidad=5):
    """
    Busca las cartas más similares a una imagen.
    
    Raises:
        ValueError: Si no se puede procesar la imagen
    """
    try:
        vector = generar_embedding(ruta_imagen)
    except Exception as e:
        logger.error(f"Error generando embedding: {str(e)}")
        raise ValueError(f"Error procesando imagen: {str(e)}")

    try:
        similitud = cosine_similarity(
            vector,
            embeddings
        )[0]
    except Exception as e:
        logger.error(f"Error calculando similitud: {str(e)}")
        raise ValueError(f"Error en búsqueda de similitud: {str(e)}")
    
    # Validar que tenemos similitudes válidas
    if similitud is None or len(similitud) == 0:
        raise ValueError("No se pudo calcular similitud")
    
    indices = np.argsort(similitud)[::-1][:cantidad]

    resultados = []

    for indice in indices:

        expansion, codigo, pokemon = obtener_info(
            nombres[indice]
        )

        similitud_valor = float(similitud[indice])
        
        # Validar que la similitud está en rango válido (0-1 o 0-100)
        if similitud_valor > 1:
            similitud_valor = min(similitud_valor, 100)
        else:
            similitud_valor = similitud_valor * 100

        resultados.append({
            "carta": pokemon,
            "set": expansion,
            "codigo": codigo,
            "similitud": round(similitud_valor, 2),
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