from animacion_sobre import ejecutar_animacion
from inventario import agregar_carta


def abrir_sobre(ventana, cartas_por_tipo):

    todas_las_cartas = []

    for tipo in cartas_por_tipo:

        todas_las_cartas.extend(
            cartas_por_tipo[tipo]
        )

    # ==========================================
    # ABRIR ANIMACIÓN
    # ==========================================

    cartas_obtenidas = ejecutar_animacion(
        todas_las_cartas
    )

    # ==========================================
    # GUARDAR CARTAS EN INVENTARIO
    # ==========================================

    for carta in cartas_obtenidas:

        agregar_carta(
            carta["card_number"]
        )