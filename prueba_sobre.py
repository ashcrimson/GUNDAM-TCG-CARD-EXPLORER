import pygame
import random
import math
import os

pygame.init()

# =========================================================
# CONFIGURACIÓN
# =========================================================

ANCHO = 1000
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Gundam Pack Opening - Prueba")

reloj = pygame.time.Clock()

# =========================================================
# SPRITESHEET
# =========================================================

ruta_sprite = os.path.join(
    os.path.dirname(__file__),
    "sprites",
    "spritesheet.png"
)

spritesheet = pygame.image.load(
    ruta_sprite
).convert_alpha()

print("Tamaño del spritesheet:", spritesheet.get_size())

# =========================================================
# FRAMES DEL GUNDAM
# =========================================================

frames_gundam = []

# Gundam 1
frames_gundam.append(
    spritesheet.subsurface(
        pygame.Rect(0, 0, 512, 360)
    )
)

# Gundam 2
frames_gundam.append(
    spritesheet.subsurface(
        pygame.Rect(512, 0, 512, 360)
    )
)

# Gundam 3
frames_gundam.append(
    spritesheet.subsurface(
        pygame.Rect(1024, 0, 512, 360)
    )
)

# Gundam 4
frames_gundam.append(
    spritesheet.subsurface(
        pygame.Rect(0, 440, 512, 300)
    )
)

# Gundam 5
frames_gundam.append(
    spritesheet.subsurface(
        pygame.Rect(512, 440, 512, 300)
    )
)
# Colores
FONDO = (15, 20, 30)
BLANCO = (255, 255, 255)
ROJO = (220, 50, 50)
AMARILLO = (255, 210, 50)
GRIS = (100, 110, 125)
GRIS_OSCURO = (45, 50, 60)

# =========================================================
# ESTADOS DE LA ANIMACIÓN
# =========================================================

ESPERANDO = 0
APUNTANDO = 1
DISPARANDO = 2
IMPACTO = 3
EXPLOSION = 4
CARTA = 5

estado = ESPERANDO

tiempo_estado = 0

# =========================================================
# POSICIONES
# =========================================================

gundam_x = 180
gundam_y = 420

caja_x = 700
caja_y = 400

proyectil_x = 300
proyectil_y = 390

# =========================================================
# PARTÍCULAS
# =========================================================

particulas = []


def crear_explosion():

    global particulas

    particulas = []

    for _ in range(80):

        angulo = random.uniform(
            0,
            math.pi * 2
        )

        velocidad = random.uniform(
            2,
            8
        )

        particulas.append({

            "x": caja_x,
            "y": caja_y,

            "vx": math.cos(angulo) * velocidad,
            "vy": math.sin(angulo) * velocidad,

            "vida": random.randint(
                30,
                70
            ),

            "radio": random.randint(
                2,
                7
            )
        })


# =========================================================
# DIBUJAR GUNDAM
# =========================================================
def dibujar_gundam():

    if estado == ESPERANDO:

        frame = frames_gundam[0]

    elif estado == APUNTANDO:

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
# =========================================================
# DIBUJAR CAJA
# =========================================================

def dibujar_caja():

    global caja_x

    # Sacudida durante el impacto

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

    # Cruz de la caja

    pygame.draw.line(
        pantalla,
        (110, 70, 30),
        (x - 50, y - 50),
        (x + 50, y + 50),
        8
    )

    pygame.draw.line(
        pantalla,
        (110, 70, 30),
        (x + 50, y - 50),
        (x - 50, y + 50),
        8
    )


# =========================================================
# DIBUJAR PROYECTIL
# =========================================================

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


# =========================================================
# DIBUJAR EXPLOSIÓN
# =========================================================

def dibujar_explosion():

    for particula in particulas:

        pygame.draw.circle(
            pantalla,
            random.choice([
                AMARILLO,
                (255, 120, 30),
                ROJO,
                BLANCO
            ]),
            (
                int(particula["x"]),
                int(particula["y"])
            ),
            particula["radio"]
        )


# =========================================================
# DIBUJAR CARTA
# =========================================================

def dibujar_carta():

    # Animación de entrada

    progreso = min(
        tiempo_estado / 60,
        1
    )

    # Ease-out

    progreso = 1 - (1 - progreso) ** 3

    ancho = int(
        180 * progreso
    )

    alto = int(
        260 * progreso
    )

    if ancho <= 0:
        return

    x = ANCHO // 2
    y = ALTO // 2

    # Sombra

    pygame.draw.rect(
        pantalla,
        (0, 0, 0),
        (
            x - ancho // 2 + 10,
            y - alto // 2 + 10,
            ancho,
            alto
        ),
        border_radius=8
    )

    # Carta

    pygame.draw.rect(
        pantalla,
        (235, 235, 240),
        (
            x - ancho // 2,
            y - alto // 2,
            ancho,
            alto
        ),
        border_radius=8
    )

    # Marco

    pygame.draw.rect(
        pantalla,
        (50, 80, 180),
        (
            x - ancho // 2,
            y - alto // 2,
            ancho,
            alto
        ),
        6,
        border_radius=8
    )

    # Imagen falsa

    if ancho > 50:

        pygame.draw.rect(
            pantalla,
            (35, 40, 55),
            (
                x - ancho // 2 + 15,
                y - alto // 2 + 25,
                ancho - 30,
                int(alto * 0.55)
            )
        )

        # Silueta Gundam

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (
                x,
                y - 30
            ),
            20
        )

        pygame.draw.rect(
            pantalla,
            (180, 180, 185),
            (
                x - 25,
                y - 5,
                50,
                65
            )
        )

    # Texto

    if ancho > 120:

        fuente = pygame.font.Font(
            None,
            24
        )

        texto = fuente.render(
            "RX-78-2",
            True,
            (20, 25, 35)
        )

        pantalla.blit(
            texto,
            (
                x - texto.get_width() // 2,
                y + alto // 2 - 45
            )
        )


# =========================================================
# LOOP PRINCIPAL
# =========================================================

ejecutando = True

while ejecutando:

    dt = reloj.tick(60)

    # -----------------------------------------------------
    # EVENTOS
    # -----------------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                ejecutando = False

            if evento.key == pygame.K_SPACE:

                if estado in (ESPERANDO, CARTA):
                    estado = APUNTANDO
                    tiempo_estado = 0
                    proyectil_x = 300

    # -----------------------------------------------------
    # TIEMPO
    # -----------------------------------------------------

    tiempo_estado += 1

    # -----------------------------------------------------
    # MÁQUINA DE ESTADOS
    # -----------------------------------------------------

    if estado == ESPERANDO:

        pass

    elif estado == APUNTANDO:

        if tiempo_estado >= 40:

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

            estado = EXPLOSION
            tiempo_estado = 0

    elif estado == EXPLOSION:

        for particula in particulas:

            particula["x"] += particula["vx"]
            particula["y"] += particula["vy"]

            particula["vy"] += 0.15

            particula["vida"] -= 1

        particulas[:] = [

            p for p in particulas
            if p["vida"] > 0
        ]

        if tiempo_estado >= 70:

            estado = CARTA
            tiempo_estado = 0

    elif estado == CARTA:

        pass

    # -----------------------------------------------------
    # DIBUJAR
    # -----------------------------------------------------

    pantalla.fill(
        FONDO
    )

    # Líneas del "hangar"

    for x in range(
        0,
        ANCHO,
        100
    ):

        pygame.draw.line(
            pantalla,
            (25, 32, 45),
            (x, 0),
            (x, ALTO),
            1
        )

    for y in range(
        0,
        ALTO,
        100
    ):

        pygame.draw.line(
            pantalla,
            (25, 32, 45),
            (0, y),
            (ANCHO, y),
            1
        )

    # -----------------------------------------------------
    # ELEMENTOS
    # -----------------------------------------------------

    if estado != CARTA:

        dibujar_gundam()

        if estado in (
            ESPERANDO,
            APUNTANDO,
            IMPACTO
        ):

            dibujar_caja()

        if estado == DISPARANDO:

            dibujar_caja()
            dibujar_proyectil()

        if estado == EXPLOSION:

            dibujar_explosion()

    else:

        dibujar_carta()

    # -----------------------------------------------------
    # TEXTO DE AYUDA
    # -----------------------------------------------------

    fuente = pygame.font.Font(
        None,
        28
    )

    if estado == ESPERANDO:

        texto = fuente.render(
            "PULSA ESPACIO PARA ABRIR EL SOBRE",
            True,
            BLANCO
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                40
            )
        )

    pygame.display.flip()


pygame.quit()