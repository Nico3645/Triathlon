import pygame

pygame.init()

# finestra
screen = pygame.display.set_mode((800, 200))
pygame.display.set_caption("Gioco Freccia")

clock = pygame.time.Clock()

# freccia
x = 50
velocita = 3

# colori
bianco = (255, 255, 255)
verde = (0, 255, 0)
giallo = (255, 255, 0)
rosso = (255, 0, 0)
blu = (0, 0, 255)

# zone
zona_verde = pygame.Rect(200, 75, 100, 50)
zona_gialla = pygame.Rect(400, 75, 100, 50)
zona_rossa = pygame.Rect(600, 75, 100, 50)

running = True

while running:

    # eventi
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # click del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:

            # se la freccia è nella zona verde
            if zona_verde.collidepoint(x, 100):
                velocita += 1

            # se è nella zona rossa
            elif zona_rossa.collidepoint(x, 100):
                velocita -= 1

                if velocita < 1:
                    velocita = 1

            # zona gialla = niente

    # movimento freccia
    x += velocita

    # se esce dallo schermo ricompare a sinistra
    if x > 800:
        x = 50

    # sfondo
    screen.fill(bianco)

    # percorso
    pygame.draw.line(screen, (0, 0, 0), (50, 100), (750, 100), 5)

    # zone colorate
    pygame.draw.rect(screen, verde, zona_verde)
    pygame.draw.rect(screen, giallo, zona_gialla)
    pygame.draw.rect(screen, rosso, zona_rossa)

    # freccia
    pygame.draw.polygon(screen, blu, [
        (x, 100),
        (x - 20, 90),
        (x - 20, 110)
    ])

    pygame.display.update()
    clock.tick(60)

pygame.quit()
