import os
import requests
from PIL import Image

from api import obtener_carta


cache = {}


# =====================================================
# CARPETA DE IMÁGENES LOCALES
# =====================================================

CARPETA_CARTAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "cartas"
)


# =====================================================
# CARGAR IMAGEN LOCAL
# =====================================================

def cargar_imagen_local(numero):

    ruta = os.path.join(
        CARPETA_CARTAS,
        f"{numero}.webp"
    )

    if not os.path.exists(ruta):

        raise FileNotFoundError(
            f"No existe la imagen local: {ruta}"
        )

    return Image.open(ruta).convert("RGB")


# =====================================================
# PRECARGAR CARTA
# =====================================================

def precargar(numero):

    if numero in cache:
        return

    try:

        print("Precargando:", numero)

        # Datos de la carta desde la API
        carta = obtener_carta(numero)

        # Imagen desde el disco
        imagen = cargar_imagen_local(numero)

        cache[numero] = {
            "carta": carta,
            "imagen": imagen
        }

        print("Precargada:", numero)

    except (
        requests.RequestException,
        KeyError,
        ValueError,
        FileNotFoundError
    ) as e:

        print(
            "No se pudo precargar:",
            numero,
            "-",
            e
        )