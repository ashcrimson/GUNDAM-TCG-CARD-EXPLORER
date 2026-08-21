from api import obtener_cartas_por_tipo


cartas_por_tipo = {}

tipo_actual = "UNIT"
indice_actual = 0
carta_actual = "GD01-001"


def cargar_cartas_tipo(tipo):

    cartas = obtener_cartas_por_tipo(tipo)

    cartas_unicas = {}

    for carta in cartas:
        numero = carta["card_number"]

        if numero not in cartas_unicas:
            cartas_unicas[numero] = carta

    cartas_por_tipo[tipo] = list(
        cartas_unicas.values()
    )

def cambiar_tipo(tipo):
    global tipo_actual, indice_actual, carta_actual

    tipo_actual = tipo
    indice_actual = 0

    carta = cartas_por_tipo[tipo_actual][indice_actual]

    carta_actual = carta["card_number"]

    return carta


def siguiente():
    global indice_actual, carta_actual

    cartas = cartas_por_tipo[tipo_actual]

    if indice_actual < len(cartas) - 1:
        indice_actual += 1

    carta = cartas[indice_actual]

    carta_actual = carta["card_number"]

    return carta


def anterior():
    global indice_actual, carta_actual

    cartas = cartas_por_tipo[tipo_actual]

    if indice_actual > 0:
        indice_actual -= 1

    carta = cartas[indice_actual]

    carta_actual = carta["card_number"]

    return carta


def obtener_indice_actual():
    return indice_actual


def obtener_tipo_actual():
    return tipo_actual