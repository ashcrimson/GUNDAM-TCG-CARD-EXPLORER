import requests


def obtener_cartas_por_tipo(tipo):
    url = "https://api.gcgapi.com/v1/cards"

    params = {
        "card_type": tipo
    }

    respuesta = requests.get(url, params=params)
    respuesta.raise_for_status()

    return respuesta.json()["data"]


def obtener_carta(numero):
    url = f"https://api.gcgapi.com/v1/cards/{numero}"

    respuesta = requests.get(url)
    respuesta.raise_for_status()

    return respuesta.json()["data"]