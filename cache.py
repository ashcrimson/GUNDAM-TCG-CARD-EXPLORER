import requests
from PIL import Image
from io import BytesIO
from api import obtener_carta
from imagenes import descargar_imagen

cache = {}


def precargar(numero):
    if numero in cache:
        return

    try:
        print("Precargando:", numero)

        carta = obtener_carta(numero)

        imagen = descargar_imagen(carta["image_url"])

        cache[numero] = {
            "carta": carta,
            "imagen": imagen
        }

        print("Precargada:", numero)

    except (requests.RequestException, KeyError, ValueError):
        print("No se pudo precargar:", numero)