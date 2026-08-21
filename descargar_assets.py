import os
import requests

from api import obtener_cartas_por_tipo


# =====================================================
# CONFIGURACIÓN
# =====================================================

CARPETA_CARTAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "cartas"
)

TIPOS = [
    "UNIT",
    "PILOT",
    "COMMAND",
    "BASE",
    "RESOURCE"
]


# =====================================================
# CREAR CARPETA
# =====================================================

os.makedirs(
    CARPETA_CARTAS,
    exist_ok=True
)


# =====================================================
# DESCARGAR CARTAS
# =====================================================

total = 0
descargadas = 0
existentes = 0
errores = 0


for tipo in TIPOS:

    print()
    print("=" * 50)
    print(f"DESCARGANDO {tipo}")
    print("=" * 50)

    try:

        cartas = obtener_cartas_por_tipo(tipo)

    except requests.RequestException as e:

        print(
            f"Error obteniendo {tipo}: {e}"
        )

        errores += 1
        continue

    for carta in cartas:

        total += 1

        numero = carta["card_number"]
        url = carta["image_url"]

        ruta = os.path.join(
            CARPETA_CARTAS,
            f"{numero}.webp"
        )

        # ---------------------------------------------
        # YA EXISTE
        # ---------------------------------------------

        if os.path.exists(ruta):

            print(
                f"[YA EXISTE] {numero}"
            )

            existentes += 1
            continue

        # ---------------------------------------------
        # DESCARGAR
        # ---------------------------------------------

        print(
            f"[DESCARGANDO] {numero}"
        )

        try:

            respuesta = requests.get(
                url,
                timeout=30
            )

            respuesta.raise_for_status()

            with open(
                ruta,
                "wb"
            ) as archivo:

                archivo.write(
                    respuesta.content
                )

            descargadas += 1

            print(
                f"[OK] {numero}"
            )

        except requests.RequestException as e:

            print(
                f"[ERROR] {numero}: {e}"
            )

            errores += 1


# =====================================================
# RESUMEN
# =====================================================

print()
print("=" * 50)
print("DESCARGA TERMINADA")
print("=" * 50)

print(
    f"Total encontradas: {total}"
)

print(
    f"Descargadas:       {descargadas}"
)

print(
    f"Ya existentes:     {existentes}"
)

print(
    f"Errores:            {errores}"
)

print(
    f"Carpeta:            {CARPETA_CARTAS}"
)