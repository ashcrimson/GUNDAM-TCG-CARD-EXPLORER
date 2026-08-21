import requests
from collections import defaultdict

url = "https://api.gcgapi.com/v1/cards"

params = {
    "set_code": "ST10",
    "limit": 250
}

respuesta = requests.get(url, params=params)
datos = respuesta.json()["data"]

grupos = defaultdict(list)

for carta in datos:
    grupos[carta["card_number"]].append(carta)

for numero, cartas in grupos.items():
    print(f"\n{numero} - {cartas[0]['name']}")
    print(f"Copias: {len(cartas)}")

    for carta in cartas:
        print("  ", carta)