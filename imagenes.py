import requests
from PIL import Image
from io import BytesIO


def descargar_imagen(url, timeout=10):
    respuesta = requests.get(url, timeout=timeout)
    respuesta.raise_for_status()

    imagen = Image.open(BytesIO(respuesta.content))
    imagen = imagen.resize((250, 350))

    return imagen