import tkinter as tk
import random
from PIL import Image, ImageTk
from cache import cache, precargar
from inventario import agregar_carta

def abrir_sobre(ventana, cartas_por_tipo):

    todas_las_cartas = []

    for tipo in cartas_por_tipo:
        todas_las_cartas.extend(
            cartas_por_tipo[tipo]
        )

    sobre = []

    for _ in range(5):
        sobre.append(
            random.choice(todas_las_cartas)
        )
    for carta in sobre:
        agregar_carta(carta)

    for carta in sobre:

        numero = carta["card_number"]

        if numero not in cache:

            import threading

            threading.Thread(
                target=precargar,
                args=(numero,),
                daemon=True
            ).start()

    mostrar_sobre(
        ventana,
        sobre
    )


def mostrar_sobre(ventana, cartas):

    ventana_sobre = tk.Toplevel(ventana)

    ventana_sobre.title("Apertura de sobre")

    ventana_sobre.geometry("700x900")

    ventana_sobre.configure(bg="#151922")
    ventana_sobre.focus_force()
    ventana_sobre.focus_set()

    indice = 0

    label_imagen = tk.Label(
        ventana_sobre,
        bg="#151922"
    )

    label_nombre = tk.Label(
        ventana_sobre,
        text="",
        font=("Arial", 20, "bold"),
        bg="#151922",
        fg="white"
    )

    label_nombre.pack(pady=20)

    label_texto = tk.Label(
        ventana_sobre,
        text="ESPACIO → siguiente carta",
        font=("Arial", 14),
        bg="#151922",
        fg="white"
    )

    label_texto.pack(pady=20)

    def mostrar_carta():

        carta = cartas[indice]

        numero = carta["card_number"]

        if numero not in cache:
            precargar(numero)

        imagen = cache[numero]["imagen"]

        imagen_grande = imagen.resize(
            (
                imagen.width * 2,
                imagen.height * 2
            ),
            Image.Resampling.LANCZOS
        )

        imagen_tk = ImageTk.PhotoImage(
            imagen_grande
        )

        label_imagen.config(
            image=imagen_tk
        )

        label_imagen.image = imagen_tk

        label_nombre.config(
            text=carta["name"]
        )

        x = -imagen_grande.width

        label_imagen.place(
            x=x,
            y=20
        )

        def animar():

            nonlocal x

            x += 40

            if x >= 50:

                x = 50

                label_imagen.place(
                    x=x,
                    y=20
                )

                return

            label_imagen.place(
                x=x,
                y=20
            )

            ventana_sobre.after(
                15,
                animar
            )

        animar()

    def siguiente(event=None):

        nonlocal indice

        indice += 1

        if indice >= len(cartas):

            ventana_sobre.destroy()

            return

        mostrar_carta()

    ventana_sobre.bind(
        "<space>",
        siguiente
    )

    mostrar_carta()