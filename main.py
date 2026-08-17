import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import winsound
import os
import sys
import random

from sobres import abrir_sobre
from coleccion import abrir_coleccion
from musica import reproducir_musica

from api import obtener_carta, obtener_cartas_por_tipo
from cartas import (
    cartas_por_tipo,
    cargar_cartas_tipo,
    cambiar_tipo as cambiar_tipo_carta,
    siguiente as siguiente_carta,
    anterior as anterior_carta,
    obtener_indice_actual,
    obtener_tipo_actual

)
from cache import cache, precargar
from imagenes import descargar_imagen
from ui import (
    actualizar_labels,
    actualizar_contador
)


def cambiar_tipo(event=None):
    tipo = menu_tipo.get()

    carta = cambiar_tipo_carta(tipo)

    entrada.delete(0, tk.END)
    entrada.insert(0, carta["card_number"])

    buscar(carta["card_number"])

def buscar(numero=None):
    print("Buscar ejecutado")
    global carta_actual

    imagen_carta.config(image="")
    imagen_carta.image = None

    if numero is None:
        numero = entrada.get()

    carta_actual = numero

    try:
        if numero in cache:
            print("Cargando desde caché:", numero)

            carta = cache[numero]["carta"]
            imagen = cache[numero]["imagen"]

        else:
            print("Consultando API:", numero)

            carta = obtener_carta(numero)

            imagen = descargar_imagen(carta["image_url"])

            cache[numero] = {
                "carta": carta,
                "imagen": imagen
            }

            print()
            print("Número recibido:", numero)
            print("Número de la carta:", carta["card_number"])
            print("Nombre:", carta["name"])
            print()

        # ==========================================
        # ACTUALIZAR DATOS DE LA CARTA
        # ==========================================
        actualizar_labels(
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
        )
        # ==========================================
        # MOSTRAR IMAGEN GRANDE
        # ==========================================

        imagen_grande = imagen.resize(
            (imagen.width * 2, imagen.height * 2),
            Image.Resampling.LANCZOS
        )

        imagen_tk = ImageTk.PhotoImage(imagen_grande)

        imagen_carta.config(image=imagen_tk)
        imagen_carta.image = imagen_tk

        # ==========================================
        # PRECARGAR SIGUIENTES CARTAS
        # ==========================================

        indice_actual = obtener_indice_actual()

        tipo_actual = obtener_tipo_actual()

        total_cartas = len(
            cartas_por_tipo[tipo_actual]
        )

        actualizar_contador(
            label_contador,
            indice_actual,
            total_cartas
        )
        actualizar_botones()

        for i in range(1, 4):
            indice_precargar = indice_actual + i

            if indice_precargar < len(cartas_por_tipo[menu_tipo.get()]):
                carta_precargar = cartas_por_tipo[menu_tipo.get()][indice_precargar]
                numero_precargar = carta_precargar["card_number"]

                threading.Thread(
                    target=precargar,
                    args=(numero_precargar,),
                    daemon=True
                ).start()

    except (KeyError, ValueError):
        label_nombre.config(
            text="No se encontró la carta"
        )
animando = False


def deslizar_carta(direccion, numero):
    global animando

    if animando:
        return

    animando = True

    # Obtener la imagen desde caché
    if numero in cache:
        imagen = cache[numero]["imagen"]
    else:
        # Si todavía no está en caché, dejamos que buscar() la cargue
        animando = False
        buscar(numero)
        return

    imagen_grande = imagen.resize(
        (imagen.width * 2, imagen.height * 2),
        Image.Resampling.LANCZOS
    )

    imagen_tk = ImageTk.PhotoImage(imagen_grande)

    # Guardamos la referencia
    imagen_carta.imagen_nueva = imagen_tk

    # Posición inicial
    ancho_frame = frame_imagen.winfo_width()

    if direccion == 1:
        # Derecha: la nueva carta entra desde la derecha
        x_inicio = ancho_frame
    else:
        # Izquierda: la nueva carta entra desde la izquierda
        x_inicio = -imagen_grande.width

    imagen_carta.config(image=imagen_tk)
    imagen_carta.place(
        x=x_inicio,
        y=0
    )

    velocidad = 40
    posicion_final = 0

    def animar(x):
        global animando

        if direccion == 1:
            nuevo_x = x - velocidad

            if nuevo_x <= posicion_final:
                nuevo_x = posicion_final
        else:
            nuevo_x = x + velocidad

            if nuevo_x >= posicion_final:
                nuevo_x = posicion_final

        imagen_carta.place(
            x=nuevo_x,
            y=0
        )

        if nuevo_x == posicion_final:
            animando = False

            # Ahora actualizamos el resto de la información
            buscar(numero)

        else:
            ventana.after(15, lambda: animar(nuevo_x))

    animar(x_inicio)

def sonido_pagina():

    if getattr(sys, "frozen", False):
        carpeta_base = sys._MEIPASS
    else:
        carpeta_base = os.path.dirname(os.path.abspath(__file__))

    ruta_sonido = os.path.join(
        carpeta_base,
        "sonidos",
        "pagina.wav"
    )

    winsound.PlaySound(
        ruta_sonido,
        winsound.SND_ASYNC
    )


def siguiente():
    print("Tecla derecha")

    indice = obtener_indice_actual()
    total = len(cartas_por_tipo[menu_tipo.get()])

    if indice >= total - 1:
        return

    sonido_pagina()

    carta = siguiente_carta()

    entrada.delete(0, tk.END)
    entrada.insert(0, carta["card_number"])

    deslizar_carta(
        1,
        carta["card_number"]
    )

def anterior():

    indice = obtener_indice_actual()

    if indice <= 0:
        return

    sonido_pagina()

    carta = anterior_carta()

    entrada.delete(0, tk.END)
    entrada.insert(0, carta["card_number"])

    deslizar_carta(
        -1,
        carta["card_number"]
    )

def efecto_boton(boton):
    boton.config(relief="sunken")

    ventana.after(
        120,
        lambda: boton.config(relief="raised")
    )

def actualizar_botones():

    indice = obtener_indice_actual()

    total = len(cartas_por_tipo[menu_tipo.get()])

    if indice == 0:
        boton_anterior.config(state="disabled")
    else:
        boton_anterior.config(state="normal")

    if indice >= total - 1:
        boton_siguiente.config(state="disabled")
    else:
        boton_siguiente.config(state="normal")

ventana = tk.Tk()

carta = obtener_carta("GD01-002")

print("AMURO:", obtener_carta("ST01-010"))
print("HEERO:", obtener_carta("ST02-010"))
print("MIKAZUKI:", obtener_carta("ST05-010"))


cargar_cartas_tipo("UNIT")
print("========== PILOTOS ==========")

pilotos = obtener_cartas_por_tipo("PILOT")

for carta in pilotos:
    print(carta["card_number"], "-", carta["name"])

print("TOTAL:", len(pilotos))

print("=============================")
cargar_cartas_tipo("PILOT")
cargar_cartas_tipo("COMMAND")
cargar_cartas_tipo("BASE")
cargar_cartas_tipo("RESOURCE")
print("UNIT:", len(cartas_por_tipo["UNIT"]))
print("PILOT:", len(cartas_por_tipo["PILOT"]))
print("COMMAND:", len(cartas_por_tipo["COMMAND"]))
print("BASE:", len(cartas_por_tipo["BASE"]))
print("RESOURCE:", len(cartas_por_tipo["RESOURCE"]))

print("========== RAREZAS ==========")

rarezas = set()

for tipo in cartas_por_tipo:
    for carta in cartas_por_tipo[tipo]:
        rarezas.add(carta["rarity"])

for rareza in sorted(rarezas):
    print(rareza)

print("=============================")

print("========== CANTIDAD POR RAREZA ==========")

for rareza in sorted(rarezas):

    cantidad = 0

    for tipo in cartas_por_tipo:
        for carta in cartas_por_tipo[tipo]:

            if carta["rarity"] == rareza:
                cantidad += 1

    print(rareza, ":", cantidad)

print("==========================================")


ventana.title("Gundam Card Explorer")
ventana.geometry("1400x900")
ventana.configure(bg="#151922")


# Frame para el buscador
frame_busqueda = tk.Frame(
    ventana,
    bg="#151922"
)
frame_busqueda.pack(pady=15)

tipos = ["UNIT", "PILOT", "COMMAND", "BASE", "RESOURCE"]

menu_tipo = ttk.Combobox(
    frame_busqueda,
    values=tipos,
    state="readonly",
    width=12,
    font=("Arial", 14)
)

label_contador = tk.Label(
    frame_busqueda,
    text="",
    font=("Arial", 14, "bold"),
    bg="#0b0f16",
    fg="white"
)

label_contador.pack(side="left", padx=20)

menu_tipo.set("UNIT")
menu_tipo.pack(side="left", padx=5)
menu_tipo.bind("<<ComboboxSelected>>", cambiar_tipo)

entrada = tk.Entry(
    frame_busqueda,
    font=("Arial", 14, "bold"),
    width=12,
    bg="#303747",
    fg="white",
    insertbackground="white",
    relief="sunken",
    bd=3
)

entrada.pack(side="left", padx=5)

entrada.bind("<Left>", lambda event: "break")
entrada.bind("<Right>", lambda event: "break")

boton = tk.Button(
    frame_busqueda,
    text="BUSCAR",
    command=buscar,
    font=("Arial", 12, "bold"),
    bg="#303747",
    fg="white",
    activebackground="#4a556b",
    activeforeground="white",
    relief="raised",
    bd=3,
    padx=12,
    pady=6
)
boton.pack(side="left", padx=5)

boton_sobre = tk.Button(
    frame_busqueda,
    text="🎁 ABRIR SOBRE",
    command=lambda: abrir_sobre(
        ventana,
        cartas_por_tipo
    ),
    font=("Arial", 12, "bold"),
    bg="#303747",
    fg="white",
    relief="raised",
    bd=3,
    padx=12,
    pady=6
)

boton_sobre.pack(
    side="left",
    padx=5
)

boton_coleccion = tk.Button(
    frame_busqueda,
    text="📖 MI COLECCIÓN",
    command=lambda: abrir_coleccion(ventana),
    font=("Arial", 12, "bold"),
    bg="#303747",
    fg="white",
    activebackground="#4a556b",
    activeforeground="white",
    relief="raised",
    bd=3,
    padx=12,
    pady=6
)

boton_coleccion.pack(
    side="left",
    padx=5
)

# boton_anterior = tk.Button(
#     frame_busqueda,
#     text="◀ ATRÁS",
#     command=anterior,
#     font=("Arial", 12, "bold"),
#     bg="#303747",
#     fg="white",
#     activebackground="#4a556b",
#     activeforeground="white",
#     relief="raised",
#     bd=3,
#     padx=12,
#     pady=6
# )
# boton_anterior.pack(side="left", padx=5)

# boton_siguiente = tk.Button(
#     frame_busqueda,
#     text="SIGUIENTE ▶",
#     command=siguiente,
#     font=("Arial", 12, "bold"),
#     bg="#303747",
#     fg="white",
#     activebackground="#4a556b",
#     activeforeground="white",
#     relief="raised",
#     bd=3,
#     padx=12,
#     pady=6
# )
# boton_siguiente.pack(side="left", padx=5)

# Frame que contiene imagen y datos
frame_contenido = tk.Frame(
    ventana,
    bg="#151922"
)
frame_contenido.pack(pady=10)

# Frame de la imagen
frame_navegacion = tk.Frame(
    frame_contenido,
    bg="#151922"
)

frame_navegacion.pack(
    side="left",
    padx=30
)

boton_anterior = tk.Button(
    frame_navegacion,
    text="◀",
    command=anterior,
    font=("Arial", 28, "bold"),
    bg="#303747",
    fg="white",
    width=2,
    height=3
)

boton_anterior.pack(
    side="left",
    padx=15
)

frame_imagen = tk.Frame(
    frame_navegacion,
    bg="#151922",
    width=500,
    height=700
)

frame_imagen.pack(side="left")

frame_imagen.pack_propagate(False)

imagen_carta = tk.Label(
    frame_imagen,
    bg="#151922"
)

imagen_carta.place(
    x=0,
    y=0
)

boton_siguiente = tk.Button(
    frame_navegacion,
    text="▶",
    command=siguiente,
    font=("Arial", 28, "bold"),
    bg="#303747",
    fg="white",
    width=2,
    height=3
)

boton_siguiente.pack(
    side="left",
    padx=15
)

# Frame de los datos
frame_borde = tk.Frame(
    frame_contenido,
    bg="#ff8c00",
    padx=3,
    pady=3
)

frame_borde.pack(
    side="left",
    padx=30
)

frame_datos = tk.Frame(
    frame_borde,
    bg="#0b0f16",
    padx=20,
    pady=20
)

frame_datos.pack()

label_codigo = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16, "bold"),
    bg="#0b0f16",
    fg="white"
)
label_codigo.pack(anchor="w", pady=5)

label_nombre = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 24, "bold"),
    bg="#0b0f16",
    fg="white"
)

label_nombre.pack(anchor="w", pady=10)

label_tipo = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    bg="#0b0f16",
    fg="white"
)
label_tipo.pack(anchor="w", pady=3)

label_color = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    bg="#0b0f16",
    fg="white"
)
label_color.pack(anchor="w", pady=3)

label_rareza = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    bg="#0b0f16",
    fg="white"
)
label_rareza.pack(anchor="w", pady=3)
frame_stats = tk.Frame(
    frame_datos,
    bg="#0b0f16"
)

frame_stats.pack(
    anchor="w",
    pady=10
)

label_level = tk.Label(
    frame_stats,
    text="",
    font=("Arial", 16, "bold"),
    bg="#303747",
    fg="gold",
    width=10,
    height=2,
    relief="ridge",
    bd=3
)

label_level.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

label_cost = tk.Label(
    frame_stats,
    text="",
    font=("Arial", 16, "bold"),
    bg="#303747",
    fg="orange",
    width=10,
    height=2,
    relief="ridge",
    bd=3
)

label_cost.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

label_ap = tk.Label(
    frame_stats,
    text="",
    font=("Arial", 16, "bold"),
    bg="#303747",
    fg="red",
    width=10,
    height=2,
    relief="ridge",
    bd=3
)

label_ap.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

label_hp = tk.Label(
    frame_stats,
    text="",
    font=("Arial", 16, "bold"),
    bg="#303747",
    fg="lime",
    width=10,
    height=2,
    relief="ridge",
    bd=3
)

label_hp.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

label_effect = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    justify="left",
    wraplength=350,
    bg="#0b0f16",
    fg="white"
)

label_effect.pack(anchor="w", pady=15)

entrada.insert(0, "GD01-001")
buscar("GD01-001")
actualizar_botones()
ventana.focus_set()

reproducir_musica()

ventana.bind(
    "<Left>",
    lambda event: (
        efecto_boton(boton_anterior),
        anterior()
    )
)

ventana.bind(
    "<Right>",
    lambda event: (
        efecto_boton(boton_siguiente),
        siguiente()
    )
)

ventana.bind("<Return>", lambda event: buscar())
ventana.mainloop()