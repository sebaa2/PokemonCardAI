import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("POKEMON_API_KEY")

HEADERS = {
    "X-Api-Key": API_KEY
}

BASE_URL = "https://api.pokemontcg.io/v2/cards"


def buscar_carta(nombre):
    """
    Busca una carta por nombre.
    Devuelve la primera coincidencia encontrada.
    """

    params = {
        "q": f'name:"{nombre}"'
    }

    try:
        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        datos = response.json()

        if not datos["data"]:
            return None

        return datos["data"][0]

    except requests.RequestException:
        return None


def buscar_carta_por_nombre_y_set(nombre, set_dataset):
    """Busca cartas antiguas cuyo archivo no trae un ID compatible con la API."""
    set_api = set_dataset.replace("-", " ").title()
    params = {"q": f'name:"{nombre}" set.name:"{set_api}"'}

    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        datos = response.json()
        return datos["data"][0] if datos.get("data") else None
    except requests.RequestException:
        return None


def buscar_carta_id(card_id):
    """
    Busca una carta utilizando su ID.
    Ejemplo:
        ex6-105
        sv3-197
    """

    try:

        response = requests.get(
            f"{BASE_URL}/{card_id}",
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()["data"]

    except requests.RequestException:
        return None


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


def obtener_info_carta(card_id, nombre=None, set_dataset=None):
    """
    Obtiene toda la información necesaria para mostrar
    la carta en la aplicación.
    """

    card = buscar_carta_id(card_id) if card_id else None

    if card is None and nombre and set_dataset:
        card = buscar_carta_por_nombre_y_set(nombre, set_dataset)

    if card is None:
        return None

    return {
        "id": card.get("id"),
        "nombre": card.get("name"),
        "hp": card.get("hp"),
        "tipos": card.get("types", []),
        "rareza": card.get("rarity"),
        "artista": card.get("artist"),
        "numero": card.get("number"),

        "imagen": card.get("images", {}).get("large"),

        "set": card.get("set", {}).get("name"),
        "serie": card.get("set", {}).get("series"),
        "fecha": card.get("set", {}).get("releaseDate"),

        "logo_set": card.get("set", {}).get("images", {}).get("logo"),
        "simbolo_set": card.get("set", {}).get("images", {}).get("symbol"),

        "precio": obtener_precio(card),

        "ataques": card.get("attacks", []),
        "habilidades": card.get("abilities", []),
        "debilidades": card.get("weaknesses", []),
        "resistencias": card.get("resistances", []),
        "retirada": card.get("convertedRetreatCost"),
        "reglas": card.get("rules", [])
    }
