import random

from cache import cache, precargar
from inventario import agregar_carta
from animacion_sobre import ejecutar_animacion


def abrir_sobre(ventana, cartas_por_tipo):

    todas_las_cartas = []

    for tipo in cartas_por_tipo:
        todas_las_cartas.extend(
            cartas_por_tipo[tipo]
        )

    # ==========================================
    # ELEGIR 5 CARTAS
    # ==========================================

    sobre = []

    for _ in range(5):
        sobre.append(
            random.choice(todas_las_cartas)
        )

    # ==========================================
    # GUARDAR EN INVENTARIO
    # ==========================================

    for carta in sobre:
        agregar_carta(carta)

    # ==========================================
    # PRECARGAR IMÁGENES
    # ==========================================

    for carta in sobre:

        numero = carta["card_number"]

        if numero not in cache:

            import threading

            threading.Thread(
                target=precargar,
                args=(numero,),
                daemon=True
            ).start()

    # ==========================================
    # ASEGURAR LA PRIMERA CARTA
    # ==========================================

    primera_carta = sobre[0]

    numero = primera_carta["card_number"]

    if numero not in cache:
        precargar(numero)

    # ==========================================
    # ABRIR ANIMACIÓN
    # ==========================================

    ejecutar_animacion(
        sobre
    )