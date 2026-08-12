import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import threading

from api import obtener_carta
from cartas import (
    cartas_por_tipo,
    cargar_cartas_tipo,
    cambiar_tipo as cambiar_tipo_carta,
    siguiente as siguiente_carta,
    anterior as anterior_carta,
    obtener_indice_actual
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

            imagen_tk = ImageTk.PhotoImage(imagen)


        else:

            print("Consultando API:", numero)

            carta = obtener_carta(numero)

            imagen = descargar_imagen(carta["image_url"])

            cache[numero] = {

                "carta": carta,

                "imagen": imagen

            }

            imagen_tk = ImageTk.PhotoImage(imagen)
        resultado.config(
            text=f"""
Nombre: {carta["name"]}
Número: {carta["card_number"]}
Color: {carta["color"]}
Tipo: {carta["card_type"]}
Coste: {carta["cost"]}
AP: {carta["ap"]}
HP: {carta["hp"]}

Efecto:
{carta["effect"]}
""",
            wraplength=400
        )

        imagen_carta.config(image=imagen_tk)
        imagen_carta.image = imagen_tk

        indice_actual = obtener_indice_actual()

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
        resultado.config(
            text="No se encontró la carta o la respuesta no es válida."
        )

def siguiente():
    carta = siguiente_carta()

    entrada.delete(0, tk.END)
    entrada.insert(0, carta["card_number"])

    buscar(carta["card_number"])

def anterior():
    carta = anterior_carta()

    entrada.delete(0, tk.END)
    entrada.insert(0, carta["card_number"])

    buscar(carta["card_number"])

ventana = tk.Tk()

carta = obtener_carta("GD01-002")


cargar_cartas_tipo("UNIT")
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
ventana.geometry("900x600")


# Frame para el buscador
frame_busqueda = tk.Frame(ventana)
frame_busqueda.pack(pady=15)

tipos = ["UNIT", "PILOT", "COMMAND", "BASE", "RESOURCE"]

menu_tipo = ttk.Combobox(
    frame_busqueda,
    values=tipos,
    state="readonly",
    width=12
)

menu_tipo.set("UNIT")
menu_tipo.pack(side="left", padx=5)
menu_tipo.bind("<<ComboboxSelected>>", cambiar_tipo)

entrada = tk.Entry(frame_busqueda)
entrada.pack(side="left")

boton = tk.Button(frame_busqueda, text="Buscar", command=buscar)
boton.pack(side="left", padx=5)

boton_anterior = tk.Button(
    frame_busqueda,
    text="← Atrás",
    command=anterior
)
boton_anterior.pack(side="left", padx=5)

boton_siguiente = tk.Button(
    frame_busqueda,
    text="Siguiente →",
    command=siguiente
)
boton_siguiente.pack(side="left", padx=5)

# Frame que contiene imagen y datos
frame_contenido = tk.Frame(ventana)
frame_contenido.pack()


# Frame de la imagen
frame_imagen = tk.Frame(frame_contenido)
frame_imagen.pack(side="left", padx=20)

imagen_carta = tk.Label(frame_imagen)
imagen_carta.pack()


# Frame de los datos
frame_datos = tk.Frame(frame_contenido)
frame_datos.pack(side="left", padx=20)

resultado = tk.Label(
    frame_datos,
    text="",
    justify="left",
    anchor="nw",
    wraplength=400
)
resultado.pack()

entrada.insert(0, "GD01-001")
buscar("GD01-001")

ventana.mainloop()