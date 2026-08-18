import tkinter as tk
import os
import sys
from PIL import Image, ImageTk

from inventario import cargar_inventario
from cache import cache, precargar
from api import obtener_carta
from imagenes import descargar_imagen

FUENTE_UI = "Neo Gen"

def obtener_ruta_imagen(nombre):

    if getattr(sys, "frozen", False):

        carpeta_base = sys._MEIPASS

    else:

        carpeta_base = os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.join(
        carpeta_base,
        "imagenes",
        nombre
    )
def obtener_imagen_carta(numero):

    if numero in cache:
        return cache[numero]["imagen"]

    carta = obtener_carta(numero)

    imagen = descargar_imagen(
        carta["image_url"]
    )

    cache[numero] = {
        "carta": carta,
        "imagen": imagen
    }

    return imagen


def abrir_carta(ventana, carta):

    ventana_carta = tk.Toplevel(ventana)

    ventana_carta.title(
        carta["name"]
    )

    ventana_carta.geometry("650x850")

    ventana_carta.configure(
        bg="#151922"
    )

    imagen = obtener_imagen_carta(
        carta["card_number"]
    )

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

    label_imagen = tk.Label(
        ventana_carta,
        image=imagen_tk,
        bg="#151922"
    )

    label_imagen.image = imagen_tk

    label_imagen.pack(
        pady=20
    )

    label_nombre = tk.Label(
        ventana_carta,
        text=carta["name"],
        font=("Arial", 22, "bold"),
        bg="#151922",
        fg="white"
    )

    label_nombre.pack(
        pady=5
    )

    label_info = tk.Label(
        ventana_carta,
        text=(
            f'Código: {carta["card_number"]}\n'
            f'Rareza: {carta["rarity"]}\n'
            f'Cantidad: ×{carta["quantity"]}'
        ),
        font=("Arial", 15),
        bg="#151922",
        fg="white"
    )

    label_info.pack(
        pady=10
    )


def abrir_coleccion(ventana):

    ventana_coleccion = tk.Toplevel(
        ventana
    )

    ventana_coleccion.title(
        "Mi Colección"
    )

    ventana_coleccion.geometry("1400x900")

    ventana_coleccion.configure(
        bg="#151922"
    )



    # ==========================================
    # TÍTULO
    # ==========================================

    titulo = tk.Label(
        ventana_coleccion,
        text="MI COLECCIÓN",
        font=(FUENTE_UI, 28, "bold"),
        bg="#0b0f16",
        fg="white"
    )

    titulo.pack(
        pady=(20, 5)
    )

    # ==========================================
    # INVENTARIO
    # ==========================================

    inventario = cargar_inventario()

    cantidad_cartas = len(
        inventario
    )

    total_copias = sum(
        carta["quantity"]
        for carta in inventario.values()
    )

    contador = tk.Label(
        ventana_coleccion,
        text=(
            f"COLECCIÓN: {cantidad_cartas} "
            f"cartas  |  "
            f"COPIAS: {total_copias}"
        ),
        font=("Arial", 14, "bold"),
        bg="#0b0f16",
        fg="white",
        padx=20,
        pady=8
    )

    contador.pack(
        pady=(5, 15)
    )

    # ==========================================
    # ÁREA SCROLL
    # ==========================================

    contenedor = tk.Frame(
        ventana_coleccion,
        bg="black"
    )

    contenedor.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    canvas = tk.Canvas(
        contenedor,
        bg="#151922",
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        contenedor,
        orient="vertical",
        command=canvas.yview
    )

    frame_cartas = tk.Frame(
        canvas,
        bg="#151922"
    )

    frame_cartas.bind(
        "<Configure>",
        lambda event:
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )
    )

    canvas.create_window(
        (0, 0),
        window=frame_cartas,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ==========================================
    # CARTAS
    # ==========================================

    columnas = 5

    for indice, carta in enumerate(
            inventario.values()
    ):
        fila = indice // columnas
        columna = indice % columnas

        crear_ficha(
            frame_cartas,
            ventana_coleccion,
            carta,
            fila,
            columna
        )

    # ==========================================
    # CERRAR
    # ==========================================

    boton_cerrar = tk.Button(
        ventana_coleccion,
        text="CERRAR",
        command=ventana_coleccion.destroy,
        font=("Arial", 12, "bold"),
        bg="#303747",
        fg="white",
        activebackground="#4a556b",
        activeforeground="white",
        relief="raised",
        bd=3,
        padx=20,
        pady=8
    )

    boton_cerrar.pack(
        pady=15
    )


def crear_ficha(
    frame,
    ventana_coleccion,
    carta,
    fila,
    columna
):

    # ==========================================
    # FICHA
    # ==========================================

    ficha = tk.Frame(
        frame,
        bg="#303747",
        padx=8,
        pady=8
    )

    ficha.grid(
        row=fila,
        column=columna,
        padx=15,
        pady=15
    )

    # ==========================================
    # IMAGEN
    # ==========================================

    label_imagen = tk.Label(
        ficha,
        text="CARGANDO...",
        bg="#303747",
        fg="white"
    )

    label_imagen.pack()

    label_imagen.bind(
        "<Button-1>",
        lambda event,
               c=carta:
        abrir_carta(
            ventana_coleccion,
            c
        )
    )

    def cargar_imagen():

        try:

            imagen = obtener_imagen_carta(
                carta["card_number"]
            )

            imagen_miniatura = imagen.copy()

            imagen_miniatura.thumbnail(
                (
                    180,
                    250
                ),
                Image.Resampling.LANCZOS
            )

            def mostrar_imagen():

                imagen_tk = ImageTk.PhotoImage(
                    imagen_miniatura
                )

                label_imagen.config(
                    image=imagen_tk,
                    text=""
                )

                label_imagen.image = imagen_tk

            ventana_coleccion.after(
                0,
                mostrar_imagen
            )

        except Exception as error:

            print(
                "Error cargando carta:",
                carta["card_number"],
                error
            )

    import threading

    threading.Thread(
        target=cargar_imagen,
        daemon=True
    ).start()

    # ==========================================
    # NOMBRE
    # ==========================================

    label_nombre = tk.Label(
        ficha,
        text=carta["name"],
        font=("Arial", 11, "bold"),
        bg="#303747",
        fg="white",
        width=22,
        wraplength=190
    )

    label_nombre.pack(
        pady=(8, 3)
    )

    # ==========================================
    # RAREZA
    # ==========================================

    label_rareza = tk.Label(
        ficha,
        text=f'Rareza: {carta["rarity"]}',
        font=("Arial", 10),
        bg="#303747",
        fg="gold"
    )

    label_rareza.pack()

    # ==========================================
    # CANTIDAD
    # ==========================================

    label_cantidad = tk.Label(
        ficha,
        text=f'×{carta["quantity"]}',
        font=("Arial", 14, "bold"),
        bg="#303747",
        fg="white"
    )

    label_cantidad.pack(
        pady=(3, 0)
    )