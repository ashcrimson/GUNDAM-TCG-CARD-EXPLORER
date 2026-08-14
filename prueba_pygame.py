import pygame

pygame.init()

ventana = pygame.display.set_mode((700, 900))
pygame.display.set_caption("Prueba Gacha")

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

    ventana.fill((21, 25, 34))

    pygame.display.flip()

pygame.quit()