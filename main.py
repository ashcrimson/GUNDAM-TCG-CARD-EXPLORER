import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading

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
            text=f'Level: {carta["level"]}'
        )

        label_cost.config(
            text=f'Cost: {carta["cost"]}'
        )

        label_ap.config(
            text=f'AP: {carta["ap"]}'
        )

        label_hp.config(
            text=f'HP: {carta["hp"]}'
        )

        label_effect.config(
            text=f'Efecto:\n{carta["effect"]}'
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

        label_contador.config(
            text=f'Carta {indice_actual + 1} / {total_cartas}'
        )

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

def siguiente():
    print("Tecla derecha")

    carta = siguiente_carta()

    entrada.delete(0, tk.END)
    entrada.insert(0, carta["card_number"])

    buscar(carta["card_number"])



def anterior():
    carta = anterior_carta()

    entrada.delete(0, tk.END)
    entrada.insert(0, carta["card_number"])

    buscar(carta["card_number"])

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


ventana.title("Gundam Card Explorer")
ventana.geometry("1200x900")
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
    bg="#151922",
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

boton_anterior = tk.Button(
    frame_busqueda,
    text="◀ ATRÁS",
    command=anterior,
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
boton_anterior.pack(side="left", padx=5)

boton_siguiente = tk.Button(
    frame_busqueda,
    text="SIGUIENTE ▶",
    command=siguiente,
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
boton_siguiente.pack(side="left", padx=5)

# Frame que contiene imagen y datos
frame_contenido = tk.Frame(
    ventana,
    bg="#151922"
)
frame_contenido.pack(pady=10)

# Frame de la imagen
frame_imagen = tk.Frame(
    frame_contenido,
    bg="#151922"
)
frame_imagen.pack(side="left", padx=30)

imagen_carta = tk.Label(frame_imagen)
imagen_carta.pack()

# Frame de los datos
frame_datos = tk.Frame(
    frame_contenido,
    bg="#151922"
)
frame_datos.pack(side="left", padx=30)

label_codigo = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16, "bold"),
    bg="#151922",
    fg="white"
)
label_codigo.pack(anchor="w", pady=5)

label_nombre = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 22, "bold"),
    bg="#151922",
    fg="white"
)

label_nombre.pack(anchor="w", pady=10)

label_tipo = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    bg="#151922",
    fg="white"
)
label_tipo.pack(anchor="w", pady=3)

label_color = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    bg="#151922",
    fg="white"
)
label_color.pack(anchor="w", pady=3)

label_rareza = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    bg="#151922",
    fg="white"
)
label_rareza.pack(anchor="w", pady=3)

label_level = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 18, "bold"),
    bg="#151922",
    fg="white"
)
label_level.pack(anchor="w", pady=3)

label_cost = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 18, "bold"),
    bg="#151922",
    fg="white"
)
label_cost.pack(anchor="w", pady=3)

label_ap = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 18, "bold"),
    bg="#151922",
    fg="white"
)
label_ap.pack(anchor="w", pady=3)

label_hp = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 18, "bold"),
    bg="#151922",
    fg="white"
)
label_hp.pack(anchor="w", pady=3)

label_effect = tk.Label(
    frame_datos,
    text="",
    font=("Arial", 16),
    justify="left",
    wraplength=350,
    bg="#151922",
    fg="white"
)

label_effect.pack(anchor="w", pady=15)

entrada.insert(0, "GD01-001")
buscar("GD01-001")
ventana.focus_set()

ventana.bind("<Left>", lambda event: anterior())
ventana.bind("<Right>", lambda event: siguiente())
ventana.bind("<Return>", lambda event: buscar())
ventana.mainloop()