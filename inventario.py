import json
import os

ARCHIVO = "inventario.json"


def cargar_inventario():

    if not os.path.exists(ARCHIVO):
        return {}

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_inventario(inventario):

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(
            inventario,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def agregar_carta(carta):

    inventario = cargar_inventario()

    numero = carta["card_number"]

    if numero in inventario:

        inventario[numero]["quantity"] += 1

    else:

        inventario[numero] = {
            "card_number": numero,
            "name": carta["name"],
            "rarity": carta["rarity"],
            "quantity": 1
        }

    guardar_inventario(inventario)