import json
import os
import re
from pathlib import Path

import requests
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("POKEMON_API_KEY")

HEADERS = {
    "X-Api-Key": API_KEY
}

BASE_URL = "https://api.pokemontcg.io/v2/cards"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_INDEX = PROJECT_ROOT / "dataset" / "embeddings" / "processed_index.json"


@st.cache_data(show_spinner=False)
def cargar_archivos_procesados():
    """Carga los nombres completos usados por el índice de embeddings."""
    try:
        with PROCESSED_INDEX.open(encoding="utf-8") as archivo_indice:
            nombres = json.load(archivo_indice)
    except (OSError, json.JSONDecodeError):
        return frozenset()

    if not isinstance(nombres, list):
        return frozenset()
    return frozenset(
        nombre for nombre in nombres if isinstance(nombre, str)
    )


def obtener_nombre_indexado(archivo):
    """Devuelve el nombre canónico del archivo según processed_index.json."""
    if not archivo:
        return None

    nombre = os.path.basename(str(archivo))
    archivos = cargar_archivos_procesados()
    return nombre if nombre in archivos else None


def _obtener_datos(url, params=None):
    """Realiza una consulta y devuelve sus cartas, o una lista vacía."""
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        datos = response.json()
    except (requests.RequestException, ValueError):
        return []

    cartas = datos.get("data", []) if isinstance(datos, dict) else []
    if isinstance(cartas, dict):
        return [cartas]
    return cartas if isinstance(cartas, list) else []


def _texto_query(valor):
    """Escapa comillas para mantener válido el lenguaje de búsqueda de la API."""
    return str(valor).replace("\\", "\\\\").replace('"', '\\"')


def buscar_carta(nombre):
    """
    Busca una carta por nombre.
    Devuelve la primera coincidencia encontrada.
    """

    cartas = _obtener_datos(
        BASE_URL,
        {"q": f'name:"{_texto_query(nombre)}"'},
    )
    return cartas[0] if cartas else None


def buscar_carta_por_nombre_y_set(nombre, set_dataset):
    """Busca cartas antiguas cuyo archivo no trae un ID compatible con la API."""
    set_api = set_dataset.replace("-", " ").title()
    params = {
        "q": (
            f'name:"{_texto_query(nombre)}" '
            f'set.name:"{_texto_query(set_api)}"'
        )
    }
    cartas = _obtener_datos(BASE_URL, params)
    return cartas[0] if cartas else None


def extraer_numero_carta(archivo):
    """Extrae el número de colección del nombre canónico del índice."""
    if not archivo:
        return None

    nombre = os.path.splitext(
        obtener_nombre_indexado(archivo) or os.path.basename(str(archivo))
    )[0]
    coincidencias = re.findall(r"(?:^|[-_])(\d+[A-Za-z]?)(?:[-_]|$)", nombre)
    return coincidencias[-1].lower() if coincidencias else None


def buscar_carta_por_set_y_numero(set_dataset, numero):
    """Busca una carta por el nombre de la expansión y su número."""
    if not set_dataset or not numero:
        return None

    params = {
        "q": (
            f'set.name:"{_texto_query(set_dataset.replace("-", " ").title())}" '
            f'number:"{_texto_query(numero)}"'
        )
    }
    cartas = _obtener_datos(BASE_URL, params)
    return cartas[0] if cartas else None


def reconstruir_id(archivo, codigo=None):
    """Reconstruye el ID de la API a partir del nombre del archivo local."""
    if not archivo:
        return None

    nombre_indexado = obtener_nombre_indexado(archivo)
    nombre = os.path.splitext(
        nombre_indexado or os.path.basename(str(archivo))
    )[0]
    coincidencia = re.search(
        r"(?:^|[-_])([A-Za-z]*\d[A-Za-z0-9]*)[-_](\d+[A-Za-z]?)(?:[-_]|$)",
        nombre,
    )
    if coincidencia:
        return (
            f"{coincidencia.group(1).lower()}-"
            f"{coincidencia.group(2).lower()}"
        )

    partes = nombre.split("_")
    if len(partes) < 3:
        return None

    codigo_archivo = partes[1] or codigo
    if not codigo_archivo:
        return None

    for parte in partes[2:]:
        if parte.isdigit():
            return f"{codigo_archivo}-{int(parte)}"

    return None


def buscar_carta_id(card_id):
    """
    Busca una carta utilizando su ID.
    Ejemplo:
        ex6-105
        sv3-197
    """

    cartas = _obtener_datos(f"{BASE_URL}/{card_id}")
    return cartas[0] if cartas else None


def obtener_precio(card):
    """
    Obtiene el precio de mercado de la carta.
    """

    if "tcgplayer" not in card:
        return None

    precios = card["tcgplayer"].get("prices", {})

    for tipo in precios.values():

        if isinstance(tipo, dict) and "market" in tipo:
            return tipo["market"]

    return None


@st.cache_data(show_spinner=False)
def obtener_info_carta(codigo, nombre=None, set_dataset=None, archivo=None):
    """
    Obtiene toda la información necesaria para mostrar
    la carta en la aplicación.
    """
    card_id = reconstruir_id(archivo, codigo)
    card = buscar_carta_id(card_id) if card_id else None
    numero = extraer_numero_carta(archivo)

    # Algunos códigos del dataset no coinciden con el ID oficial del set.
    if card is not None and numero and str(card.get("number", "")).lower() != numero:
        card = None

    if card is None and nombre and set_dataset:
        card = buscar_carta_por_nombre_y_set(nombre, set_dataset)

    if card is None and set_dataset and numero:
        card = buscar_carta_por_set_y_numero(set_dataset, numero)

    if card is None and nombre:
        card = buscar_carta(nombre)

    if card is None:
        return None
    if not isinstance(card, dict):
        return None

    set_info = card.get("set", {})
    images = card.get("images", {})

    return {
        "id": card.get("id"),
        "nombre": card.get("name"),
        "hp": card.get("hp"),
        "tipos": card.get("types") or [],
        "rareza": card.get("rarity"),
        "artista": card.get("artist"),
        "numero": card.get("number"),

        "imagen": images.get("large") if isinstance(images, dict) else None,

        "set": set_info.get("name") if isinstance(set_info, dict) else None,
        "serie": set_info.get("series") if isinstance(set_info, dict) else None,
        "fecha": set_info.get("releaseDate") if isinstance(set_info, dict) else None,

        "logo_set": (
            set_info.get("images", {}).get("logo")
            if isinstance(set_info, dict)
            and isinstance(set_info.get("images"), dict)
            else None
        ),
        "simbolo_set": (
            set_info.get("images", {}).get("symbol")
            if isinstance(set_info, dict)
            and isinstance(set_info.get("images"), dict)
            else None
        ),

        "precio": obtener_precio(card),

        "ataques": card.get("attacks") or [],
        "habilidades": card.get("abilities") or [],
        "debilidades": card.get("weaknesses") or [],
        "resistencias": card.get("resistances") or [],
        "retirada": card.get("convertedRetreatCost"),
        "reglas": card.get("rules") or []
    }
