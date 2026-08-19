import pygame
import random
import math
import os

from PIL import Image

from cache import cache, precargar

RUTA_FUENTE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fuentes",
    "Neo Gen.ttf"
)

RUTA_FUENTE_BOLD = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fuentes",
    "Neo Gen Bold.ttf"
)


def ejecutar_animacion(cartas):

    pygame.init()



    RUTA_DISPARO = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "sonidos",
        "disparo.wav"
    )

    RUTA_EXPLOSION = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "sonidos",
        "explosion.wav"
    )

    sonido_disparo = pygame.mixer.Sound(
        RUTA_DISPARO
    )

    sonido_explosion = pygame.mixer.Sound(
        RUTA_EXPLOSION
    )

    fuente_ui = pygame.font.Font(
        RUTA_FUENTE,
        32
    )

    fuente_ui_bold = pygame.font.Font(
        RUTA_FUENTE_BOLD,
        32
    )

    ANCHO = 1000
    ALTO = 700

    pantalla = pygame.display.set_mode(
        (ANCHO, ALTO)
    )

    # =====================================================
    # SPRITESHEET DEL GUNDAM
    # =====================================================

    ruta_sprite = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "sprites",
        "spritesheet.png"
    )

    spritesheet = pygame.image.load(
        ruta_sprite
    ).convert_alpha()

    frames_gundam = []

    frames_gundam.append(
        spritesheet.subsurface(
            pygame.Rect(0, 0, 512, 360)
        )
    )

    frames_gundam.append(
        spritesheet.subsurface(
            pygame.Rect(512, 0, 512, 360)
        )
    )

    frames_gundam.append(
        spritesheet.subsurface(
            pygame.Rect(1024, 0, 512, 360)
        )
    )

    frames_gundam.append(
        spritesheet.subsurface(
            pygame.Rect(0, 440, 512, 300)
        )
    )

    frames_gundam.append(
        spritesheet.subsurface(
            pygame.Rect(512, 440, 512, 300)
        )
    )

    pygame.display.set_caption(
        "Gundam Pack Opening"
    )

    reloj = pygame.time.Clock()

    # =====================================================
    # COLORES
    # =====================================================

    FONDO = (15, 20, 30)
    BLANCO = (255, 255, 255)
    AMARILLO = (255, 210, 50)
    ROJO = (220, 50, 50)

    # =====================================================
    # ESTADOS
    # =====================================================

    APUNTANDO = 0
    DISPARANDO = 1
    IMPACTO = 2
    EXPLOSION = 3
    CARTA_PEQUENA = 4
    CARTA_GRANDE = 5
    RETIRAR_CARTA = 6
    RESULTADOS = 7

    estado = APUNTANDO
    tiempo_estado = 0

    # =====================================================
    # CARTAS
    # =====================================================

    indice_carta = 0

    carta_actual = None
    numero_carta = None
    rareza = None
    imagen_carta = None

    imagenes_resultado = []

    nivel_explosion = 1

    # =====================================================
    # POSICIONES
    # =====================================================

    gundam_x = 180
    gundam_y = 420

    caja_x = 700
    caja_y = 400

    proyectil_x = 300
    proyectil_y = 390

    particulas = []

    # =====================================================
    # FUENTES
    # =====================================================

    fuente_titulo = pygame.font.Font(
        RUTA_FUENTE_BOLD,
        32
    )

    # =====================================================
    # PREPARAR CARTA REAL
    # =====================================================

    def preparar_carta():

        nonlocal carta_actual
        nonlocal numero_carta
        nonlocal rareza
        nonlocal imagen_carta
        nonlocal nivel_explosion

        carta_actual = cartas[indice_carta]

        numero_carta = carta_actual["card_number"]

        rareza = carta_actual["rarity"]

        # ---------------------------------------------
        # NIVEL DE EXPLOSIÓN SEGÚN RAREZA
        # ---------------------------------------------

        if rareza in ("UR", "SEC"):

            nivel_explosion = 3

        elif rareza == "SR":

            nivel_explosion = 2

        else:

            nivel_explosion = 1

        # ---------------------------------------------
        # IMAGEN REAL DESDE CACHE
        # ---------------------------------------------

        if numero_carta not in cache:

            precargar(numero_carta)

        imagen_pil = cache[
            numero_carta
        ]["imagen"].copy()

        imagen_pil.thumbnail(
            (
                300,
                420
            ),
            Image.Resampling.LANCZOS
        )

        imagen_carta = pygame.image.fromstring(
            imagen_pil.tobytes(),
            imagen_pil.size,
            imagen_pil.mode
        )

    # =====================================================
    # PREPARAR LAS 5 CARTAS PARA RESULTADOS
    # =====================================================

    def preparar_resultados():

        nonlocal imagenes_resultado

        imagenes_resultado = []

        for carta in cartas:

            numero = carta["card_number"]

            if numero not in cache:

                precargar(numero)

            imagen_pil = cache[
                numero
            ]["imagen"].copy()

            imagen_pil.thumbnail(
                (
                    170,
                    240
                ),
                Image.Resampling.LANCZOS
            )

            imagen = pygame.image.fromstring(
                imagen_pil.tobytes(),
                imagen_pil.size,
                imagen_pil.mode
            )

            imagenes_resultado.append(
                imagen
            )

    # =====================================================
    # EXPLOSIÓN
    # =====================================================

    def crear_explosion():

        particulas.clear()

        if nivel_explosion == 1:

            cantidad = 50
            velocidad_maxima = 5

        elif nivel_explosion == 2:

            cantidad = 100
            velocidad_maxima = 7

        else:

            cantidad = 180
            velocidad_maxima = 11

        for _ in range(cantidad):

            angulo = random.uniform(
                0,
                math.pi * 2
            )

            velocidad = random.uniform(
                2,
                velocidad_maxima
            )

            particulas.append({

                "x": caja_x,

                "y": caja_y,

                "vx":
                    math.cos(angulo)
                    * velocidad,

                "vy":
                    math.sin(angulo)
                    * velocidad,

                "vida":
                    random.randint(
                        30,
                        70
                    ),

                "radio":
                    random.randint(
                        2,
                        7
                    )
            })

    # =====================================================
    # GUNDAM SPRITE
    # =====================================================

    def dibujar_gundam():

        if estado == APUNTANDO:

            frame = frames_gundam[1]

        elif estado == DISPARANDO:

            frame = frames_gundam[2]

        elif estado == IMPACTO:

            frame = frames_gundam[3]

        else:

            frame = frames_gundam[0]

        sprite = pygame.transform.scale(
            frame,
            (300, 300)
        )

        pantalla.blit(
            sprite,
            (
                gundam_x - 150,
                gundam_y - 150
            )
        )

    # =====================================================
    # CAJA
    # =====================================================

    def dibujar_caja():

        offset_x = 0

        if estado == IMPACTO:

            offset_x = random.randint(
                -8,
                8
            )

        x = caja_x + offset_x
        y = caja_y

        pygame.draw.rect(
            pantalla,
            (150, 100, 45),
            (
                x - 60,
                y - 60,
                120,
                120
            )
        )

        pygame.draw.rect(
            pantalla,
            (190, 135, 65),
            (
                x - 50,
                y - 50,
                100,
                100
            ),
            5
        )

        pygame.draw.line(
            pantalla,
            (110, 70, 30),
            (
                x - 50,
                y - 50
            ),
            (
                x + 50,
                y + 50
            ),
            8
        )

        pygame.draw.line(
            pantalla,
            (110, 70, 30),
            (
                x + 50,
                y - 50
            ),
            (
                x - 50,
                y + 50
            ),
            8
        )

    # =====================================================
    # PROYECTIL
    # =====================================================

    def dibujar_proyectil():

        pygame.draw.circle(
            pantalla,
            AMARILLO,
            (
                int(proyectil_x),
                int(proyectil_y)
            ),
            10
        )

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (
                int(proyectil_x),
                int(proyectil_y)
            ),
            5
        )

    # =====================================================
    # EXPLOSIÓN
    # =====================================================

    def dibujar_explosion():

        for particula in particulas:

            pygame.draw.circle(
                pantalla,
                random.choice(
                    [
                        AMARILLO,
                        (255, 120, 30),
                        ROJO,
                        BLANCO
                    ]
                ),
                (
                    int(particula["x"]),
                    int(particula["y"])
                ),
                particula["radio"]
            )

    # =====================================================
    # CARTA REAL GRANDE
    # =====================================================

    def dibujar_carta():

        if imagen_carta is None:
            return

        if estado == CARTA_PEQUENA:

            escala = min(
                0.15 +
                (tiempo_estado / 15) * 0.15,
                0.30
            )

        elif estado == CARTA_GRANDE:

            escala = min(
                0.30 +
                (tiempo_estado / 20) * 0.70,
                1.0
            )

        else:

            escala = max(
                1.0 -
                (tiempo_estado / 25),
                0
            )

        ancho = int(
            imagen_carta.get_width()
            * escala
        )

        alto = int(
            imagen_carta.get_height()
            * escala
        )

        if ancho <= 0 or alto <= 0:
            return

        carta_escalada = pygame.transform.scale(
            imagen_carta,
            (
                ancho,
                alto
            )
        )

        rect = carta_escalada.get_rect(
            center=(
                ANCHO // 2,
                ALTO // 2
            )
        )

        pantalla.blit(
            carta_escalada,
            rect
        )

    # =====================================================
    # RESULTADOS FINALES: LAS 5 CARTAS
    # =====================================================

    def dibujar_resultados():

        titulo = fuente_titulo.render(
            "RESULTADOS",
            True,
            BLANCO
        )

        titulo_rect = titulo.get_rect(
            center=(
                ANCHO // 2,
                45
            )
        )

        pantalla.blit(
            titulo,
            titulo_rect
        )

        # ---------------------------------------------
        # CARTAS
        # ---------------------------------------------

        cantidad = len(
            imagenes_resultado
        )

        ancho_carta = 170
        espacio = 15

        ancho_total = (
            cantidad * ancho_carta
            +
            (cantidad - 1) * espacio
        )

        inicio_x = (
            ANCHO - ancho_total
        ) // 2

        y = 120

        for i, imagen in enumerate(
            imagenes_resultado
        ):

            x = (
                inicio_x
                +
                i * (
                    ancho_carta
                    +
                    espacio
                )
            )

            # -----------------------------------------
            # APARICIÓN
            # -----------------------------------------

            if i == 0:

                escala = min(
                    tiempo_estado / 15,
                    1
                )

            else:

                tiempo_entrada = (
                    tiempo_estado
                    -
                    i * 12
                )

                escala = min(
                    max(
                        tiempo_entrada / 15,
                        0
                    ),
                    1
                )

            if escala <= 0:
                continue

            ancho = int(
                imagen.get_width()
                * escala
            )

            alto = int(
                imagen.get_height()
                * escala
            )

            carta_escalada = pygame.transform.scale(
                imagen,
                (
                    ancho,
                    alto
                )
            )

            rect = carta_escalada.get_rect(
                center=(
                    x + ancho_carta // 2,
                    y + 230
                )
            )

            pantalla.blit(
                carta_escalada,
                rect
            )

        # ---------------------------------------------
        # TEXTO
        # ---------------------------------------------

        if tiempo_estado >= 75:

            texto = fuente_ui.render(
                "ESPACIO → CONTINUAR",
                True,
                BLANCO
            )

            texto_rect = texto.get_rect(
                center=(
                    ANCHO // 2,
                    ALTO - 35
                )
            )

            pantalla.blit(
                texto,
                texto_rect
            )

    # =====================================================
    # PRIMERA CARTA
    # =====================================================

    preparar_carta()

    # =====================================================
    # LOOP PRINCIPAL
    # =====================================================

    ejecutando = True

    while ejecutando:

        reloj.tick(60)

        # =================================================
        # EVENTOS
        # =================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                ejecutando = False

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    ejecutando = False

                elif (
                    evento.key == pygame.K_SPACE
                    and estado == RESULTADOS
                ):

                    ejecutando = False

        tiempo_estado += 1

        # =================================================
        # ESTADOS
        # =================================================

        if estado == APUNTANDO:

            if tiempo_estado >= 40:
                sonido_disparo.play()

                estado = DISPARANDO
                tiempo_estado = 0

        elif estado == DISPARANDO:

            proyectil_x += 15

            if proyectil_x >= caja_x:

                estado = IMPACTO
                tiempo_estado = 0

        elif estado == IMPACTO:

            if tiempo_estado >= 20:
                crear_explosion()

                sonido_explosion.play()

                estado = EXPLOSION
                tiempo_estado = 0

        elif estado == EXPLOSION:

            for particula in particulas:

                particula["x"] += particula["vx"]
                particula["y"] += particula["vy"]

                particula["vy"] += 0.15

                particula["vida"] -= 1

            particulas[:] = [
                p
                for p in particulas
                if p["vida"] > 0
            ]

            if tiempo_estado >= 70:

                estado = CARTA_PEQUENA
                tiempo_estado = 0

        elif estado == CARTA_PEQUENA:

            if tiempo_estado >= 15:

                estado = CARTA_GRANDE
                tiempo_estado = 0

        elif estado == CARTA_GRANDE:

            if tiempo_estado >= 100:

                estado = RETIRAR_CARTA
                tiempo_estado = 0

        elif estado == RETIRAR_CARTA:

            if tiempo_estado >= 25:

                indice_carta += 1

                # -----------------------------------------
                # ¿TERMINARON LAS 5 CARTAS?
                # -----------------------------------------

                if indice_carta >= len(cartas):

                    preparar_resultados()

                    estado = RESULTADOS
                    tiempo_estado = 0

                else:

                    proyectil_x = 300
                    proyectil_y = 390

                    particulas.clear()

                    preparar_carta()

                    estado = APUNTANDO
                    tiempo_estado = 0

        # =================================================
        # DIBUJAR
        # =================================================

        pantalla.fill(
            FONDO
        )

        # =================================================
        # REJILLA
        # =================================================

        for x in range(
            0,
            ANCHO,
            100
        ):

            pygame.draw.line(
                pantalla,
                (25, 32, 45),
                (
                    x,
                    0
                ),
                (
                    x,
                    ALTO
                )
            )

        for y in range(
            0,
            ALTO,
            100
        ):

            pygame.draw.line(
                pantalla,
                (25, 32, 45),
                (
                    0,
                    y
                ),
                (
                    ANCHO,
                    y
                )
            )

        # =================================================
        # ESCENA
        # =================================================

        if estado in (
            APUNTANDO,
            DISPARANDO,
            IMPACTO
        ):

            dibujar_gundam()
            dibujar_caja()

            if estado == DISPARANDO:

                dibujar_proyectil()

        elif estado == EXPLOSION:

            dibujar_gundam()
            dibujar_explosion()

        elif estado in (
            CARTA_PEQUENA,
            CARTA_GRANDE,
            RETIRAR_CARTA
        ):

            dibujar_gundam()
            dibujar_carta()

        elif estado == RESULTADOS:

            dibujar_resultados()

        pygame.display.flip()

    pygame.quit()