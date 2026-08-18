import pygame
import os
import sys


pygame.mixer.init()


def obtener_ruta_musica():

    if getattr(sys, "frozen", False):
        carpeta_base = sys._MEIPASS
    else:
        carpeta_base = os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.join(
        carpeta_base,
        "sonidos",
        "musica.mp3"
    )


def reproducir_musica():

    ruta = obtener_ruta_musica()

    pygame.mixer.music.load(ruta)
    pygame.mixer.music.play(-1)
    volumen(0.2)


def detener_musica():

    pygame.mixer.music.stop()


def volumen(valor):

    pygame.mixer.music.set_volume(valor)