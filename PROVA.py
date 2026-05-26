import pygame
import sys

# =========================
# INIZIALIZZAZIONE
# =========================
pygame.init()

LARGHEZZA = 800
ALTEZZA = 600

schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Gioco Completo")

clock = pygame.time.Clock()

# Colori
NERO = (15, 15, 15)
BIANCO = (255, 255, 255)
VERDE = (50, 205, 50)
ROSSO = (220, 20, 60)
GRIGIO = (80, 80, 80)
GIALLO = (255, 255, 0)
BLU = (0, 0, 255)

# Font
font = pygame.font.SysFont("Arial", 25)
font_grande = pygame.font.SysFont("Arial", 45)

# =========================
# STATO DEL GIOCO
# =========================
fase = "SPINTA"

# =========================
# GIOCO 1 - SPINTA
# =========================
altezza_personaggi = 100
larghezza_personaggi = 60
linea_terra = ALTEZZA - 150

punto_contatto_x = LARGHEZZA // 2

forza_spinta_giocatore = 12
forza_spinta_bot = 0.4

stato_spinta = "IN_CORSO"

# =========================
# GIOCO 2 - FRECCIA
# =========================
x = 50
velocita = 3

zona_verde = pygame.Rect(200, 75, 100, 50)
zona_gialla = pygame.Rect(400, 75, 100, 50)
zona_rossa = pygame.Rect(600, 75, 100, 50)

# =========================
# LOOP PRINCIPALE
# =========================
running = True

while running:

    # ================= EVENTI =================
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            running = False

        # -----------------------------------
        # EVENTI GIOCO SPINTA
        # -----------------------------------
        if fase == "SPINTA":

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE and stato_spinta == "IN_CORSO":

                    punto_contatto_x += forza_spinta_giocatore

                    if punto_contatto_x >= LARGHEZZA - larghezza_personaggi:
                        punto_contatto_x = LARGHEZZA - larghezza_personaggi
                        stato_spinta = "GIOCATORE_VINCE"

        # -----------------------------------
        # EVENTI GIOCO FRECCIA
        # -----------------------------------
        elif fase == "FRECCIA":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if zona_verde.collidepoint(x, 100):
                    velocita += 1

                elif zona_rossa.collidepoint(x, 100):
                    velocita -= 1

                    if velocita < 1:
                        velocita = 1

    # =====================================================
    # GIOCO 1 - SPINTA
    # =====================================================
    if fase == "SPINTA":

        # Logica bot
        if stato_spinta == "IN_CORSO":

            punto_contatto_x -= forza_spinta_bot

            if punto_contatto_x <= larghezza_personaggi:
                punto_contatto_x = larghezza_personaggi
                stato_spinta = "BOT_VINCE"

        # Posizioni
        giocatore_x = punto_contatto_x - larghezza_personaggi
        bot_x = punto_contatto_x

        # Disegno
        schermo.fill(NERO)

        pygame.draw.line(
            schermo,
            GRIGIO,
            (0, linea_terra + altezza_personaggi),
            (LARGHEZZA, linea_terra + altezza_personaggi),
            5
        )

        pygame.draw.rect(
            schermo,
            VERDE,
            (giocatore_x, linea_terra, larghezza_personaggi, altezza_personaggi)
        )

        pygame.draw.rect(
            schermo,
            ROSSO,
            (bot_x, linea_terra, larghezza_personaggi, altezza_personaggi)
        )

        testo = font.render(
            "Premi SPAZIO per spingere il bot!",
            True,
            BIANCO
        )

        schermo.blit(testo, (220, 50))

        # Vittoria
        if stato_spinta == "GIOCATORE_VINCE":

            vittoria = font_grande.render(
                "HAI VINTO! Parte il gioco della freccia...",
                True,
                VERDE
            )

            schermo.blit(vittoria, (40, 200))

            pygame.display.flip()
            pygame.time.delay(2500)

            # PASSA AL GIOCO 2
            fase = "FRECCIA"

        # Sconfitta
        elif stato_spinta == "BOT_VINCE":

            sconfitta = font_grande.render(
                "SCONFITTA!",
                True,
                ROSSO
            )

            schermo.blit(sconfitta, (280, 220))

    # =====================================================
    # GIOCO 2 - FRECCIA
    # =====================================================
    elif fase == "FRECCIA":

        # Movimento freccia
        x += velocita

        if x > 800:
            x = 50

        # Disegno
        schermo.fill(BIANCO)

        pygame.draw.line(
            schermo,
            NERO,
            (50, 100),
            (750, 100),
            5
        )

        pygame.draw.rect(schermo, VERDE, zona_verde)
        pygame.draw.rect(schermo, GIALLO, zona_gialla)
        pygame.draw.rect(schermo, ROSSO, zona_rossa)

        # Freccia
        pygame.draw.polygon(
            schermo,
            BLU,
            [
                (x, 100),
                (x - 20, 90),
                (x - 20, 110)
            ]
        )

        info = font.render(
            "Click nelle zone colorate!",
            True,
            NERO
        )

        schermo.blit(info, (250, 20))

    # =====================================================
    # AGGIORNAMENTO SCHERMO
    # =====================================================
    pygame.display.flip()
    clock.tick(60)

# =========================
# CHIUSURA
# =========================
pygame.quit()
sys.exit()
