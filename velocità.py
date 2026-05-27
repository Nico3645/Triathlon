import pygame
import random

# -------------------------
# CONFIG
# -------------------------
WIDTH, HEIGHT = 1000, 500
FPS = 60

TRACK_Y = 160
TRACK_HEIGHT = 120

FINISH_X = 900

BAR_X = 200
BAR_Y = 350
BAR_WIDTH = 600
BAR_HEIGHT = 30

COUNTDOWN_TIME = 5

# -------------------------
# COLORI
# -------------------------
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)

GREEN = (50, 220, 50)
YELLOW = (240, 220, 50)
RED = (220, 60, 60)
BLUE = (70, 120, 255)

# -------------------------
# INIT
# -------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Race")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# -------------------------
# FUNZIONE RESET GARA
# -------------------------
def reset_race():

    players = []

    colors = [GREEN, BLUE, RED, YELLOW]

    for i in range(4):
        players.append({
            "x": 50,
            "y": TRACK_Y + 15 + i * 25,
            "speed": 0,
            "color": colors[i],
            "finished": False,
            "place": None
        })

    return players

players = reset_race()

# -------------------------
# ZONE BARRA
# -------------------------
green_zone = pygame.Rect(BAR_X + 260, BAR_Y, 80, BAR_HEIGHT)

yellow_zone_left = pygame.Rect(BAR_X + 170, BAR_Y, 90, BAR_HEIGHT)
yellow_zone_right = pygame.Rect(BAR_X + 340, BAR_Y, 90, BAR_HEIGHT)

# -------------------------
# FRECCIA
# -------------------------
arrow_x = BAR_X
arrow_speed = 6
arrow_direction = 1

# -------------------------
# STATO GIOCO
# -------------------------
game_started = False
game_over = False

countdown_start = pygame.time.get_ticks()

finish_order = []

player_position_text = ""

# -------------------------
# LOOP
# -------------------------
running = True

while running:

    clock.tick(FPS)

    screen.fill(WHITE)

    # -------------------------
    # EVENTI
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_started and not game_over:

                arrow_rect = pygame.Rect(
                    arrow_x - 5,
                    BAR_Y - 5,
                    10,
                    BAR_HEIGHT + 10
                )

                # BOOST
                if green_zone.colliderect(arrow_rect):
                    players[0]["speed"] = 4.5

                # VELOCITA NORMALE
                elif (
                    yellow_zone_left.colliderect(arrow_rect)
                    or yellow_zone_right.colliderect(arrow_rect)
                ):
                    players[0]["speed"] = 2.5

                # ERRORE
                else:
                    players[0]["speed"] = 0

        # RICOMINCIA
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_over:

                players = reset_race()

                finish_order = []

                game_over = False
                game_started = False

                player_position_text = ""

                countdown_start = pygame.time.get_ticks()

    # -------------------------
    # COUNTDOWN
    # -------------------------
    if not game_started:

        elapsed = (pygame.time.get_ticks() - countdown_start) / 1000
        remaining = COUNTDOWN_TIME - int(elapsed)

        text = big_font.render(str(max(0, remaining)), True, BLACK)
        screen.blit(text, (WIDTH // 2 - 20, 50))

        if elapsed >= COUNTDOWN_TIME:
            game_started = True

    # -------------------------
    # GIOCO
    # -------------------------
    if game_started and not game_over:

        # Movimento freccia
        arrow_x += arrow_speed * arrow_direction

        if arrow_x >= BAR_X + BAR_WIDTH:
            arrow_x = BAR_X + BAR_WIDTH
            arrow_direction = -1

        if arrow_x <= BAR_X:
            arrow_x = BAR_X
            arrow_direction = 1

        # -------------------------
        # CPU
        # -------------------------
        for i in range(1, 4):

            if not players[i]["finished"]:

                speed = 1.6

                r = random.random()

                # Boost casuale
                if r < 0.004:
                    speed = 3.5

                # Piccola pausa
                elif r < 0.008:
                    speed = 0.3

                players[i]["x"] += speed

        # -------------------------
        # GIOCATORE
        # -------------------------
        if not players[0]["finished"]:
            players[0]["x"] += players[0]["speed"]

        # -------------------------
        # ARRIVI
        # -------------------------
        for i, p in enumerate(players):

            if not p["finished"] and p["x"] >= FINISH_X - 20:

                p["finished"] = True

                finish_order.append(i)

                p["place"] = len(finish_order)

                # Posizione giocatore
                if i == 0:

                    pos = p["place"]

                    if pos == 1:
                        player_position_text = "SEI ARRIVATO 1°!"
                    elif pos == 2:
                        player_position_text = "SEI ARRIVATO 2°!"
                    elif pos == 3:
                        player_position_text = "SEI ARRIVATO 3°!"
                    else:
                        player_position_text = "SEI ARRIVATO 4°!"

        # Tutti arrivati
        if len(finish_order) == 4:
            game_over = True

    # -------------------------
    # DISEGNO PISTA
    # -------------------------
    pygame.draw.rect(
        screen,
        GRAY,
        (40, TRACK_Y, 900, TRACK_HEIGHT)
    )

    # Traguardo
    pygame.draw.line(
        screen,
        BLACK,
        (FINISH_X, TRACK_Y),
        (FINISH_X, TRACK_Y + TRACK_HEIGHT),
        5
    )

    # -------------------------
    # QUADRATINI
    # -------------------------
    for p in players:

        pygame.draw.rect(
            screen,
            p["color"],
            (p["x"], p["y"], 20, 20)
        )

    # -------------------------
    # BARRA
    # -------------------------
    pygame.draw.rect(
        screen,
        RED,
        (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT)
    )

    pygame.draw.rect(screen, YELLOW, yellow_zone_left)
    pygame.draw.rect(screen, YELLOW, yellow_zone_right)

    pygame.draw.rect(screen, GREEN, green_zone)

    # Freccia
    pygame.draw.polygon(
        screen,
        BLACK,
        [
            (arrow_x, BAR_Y - 15),
            (arrow_x - 10, BAR_Y),
            (arrow_x + 10, BAR_Y)
        ]
    )

    # -------------------------
    # TESTI
    # -------------------------
    info = font.render(
        "Clicca quando la freccia è nel VERDE!",
        True,
        BLACK
    )

    screen.blit(info, (250, 400))

    # Posizione giocatore
    if player_position_text != "":

        pos_text = big_font.render(
            player_position_text,
            True,
            GREEN
        )

        screen.blit(pos_text, (250, 70))

    # -------------------------
    # FINE GARA
    # -------------------------
    if game_over:

        end_text = font.render(
            "Premi SPAZIO per fare un'altra gara",
            True,
            BLACK
        )

        screen.blit(end_text, (250, 120))

    pygame.display.flip()

pygame.quit()
