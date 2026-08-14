def actualizar_labels(
    carta,
    label_codigo,
    label_nombre,
    label_tipo,
    label_color,
    label_rareza,
    label_level,
    label_cost,
    label_ap,
    label_hp,
    label_effect
):

    label_codigo.config(
        text=f'Código: {carta["card_number"]}'
    )

    label_nombre.config(
        text=carta["name"]
    )

    label_tipo.config(
        text=f'Tipo: {carta["card_type"]}'
    )

    label_color.config(
        text=f'Color: {carta["color"]}'
    )

    label_rareza.config(
        text=f'Rareza: {carta["rarity"]}'
    )

    label_level.config(
        text=f'LV\n{carta["level"]}'
    )

    label_cost.config(
        text=f'COST\n{carta["cost"]}'
    )

    label_ap.config(
        text=f'AP\n{carta["ap"]}'
    )

    label_hp.config(
        text=f'HP\n{carta["hp"]}'
    )

    label_effect.config(
        text=f'Efecto:\n{carta["effect"]}'
    )


def actualizar_contador(
    label_contador,
    indice_actual,
    total_cartas
):

    label_contador.config(
        text=f'Carta {indice_actual + 1} / {total_cartas}'
    )