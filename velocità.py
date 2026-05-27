import pygame
import random
import sys

# -------------------------
# INIT & RISOLUZIONE SCHERMO PC
# -------------------------
pygame.init()

# Rileva automaticamente le dimensioni reali dello schermo del computer
info_schermo = pygame.display.Info()
WIDTH = info_schermo.current_w
HEIGHT = info_schermo.current_h

# Imposta il gioco alla risoluzione massima dello schermo
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Mini Race - 1v1 Enhanced Edition")

FPS = 60
clock = pygame.time.Clock()

# -------------------------
# CONFIGURAZIONE TRACCIATO ADATTIVO
# -------------------------
TRACK_Y = HEIGHT // 3
TRACK_HEIGHT = 120      # Allargata la pista (altezza aumentata da 80 a 120)
FINISH_X = WIDTH - 100  # Il traguardo si adatta alla fine dello schermo del PC

# Posizionamento centrato della barra dei click
BAR_WIDTH = 600
BAR_HEIGHT = 30
BAR_X = (WIDTH - BAR_WIDTH) // 2
BAR_Y = HEIGHT - 180

COUNTDOWN_TIME = 3

# -------------------------
# COLORI
# -------------------------
NERO = (15, 15, 15)
BIANCO = (255, 255, 255)
GRIGIO_SCURO = (40, 40, 40)
GRIGIO_LUCE = (100, 100, 100)

VERDE = (0, 200, 0)
GIALLO = (230, 200, 0)
ROSSO = (200, 0, 0)

# Font proporzionati alla risoluzione dello schermo
font = pygame.font.Font(None, int(HEIGHT * 0.045))
big_font = pygame.font.Font(None, int(HEIGHT * 0.09))

# -------------------------
# FUNZIONE RESET GARA
# -------------------------
def reset_race():
    players = []
    
    # Velocità iniziale di partenza uguale per tutti e due
    velocita_iniziale = 1.0  

    # 1. Giocatore (Cubo Verde)
    players.append({
        "x": 50,
        "y": TRACK_Y + 20,       # Posizionamento distanziato nella nuova pista allargata
        "speed": velocita_iniziale,
        "color": VERDE,
        "finished": False,
        "place": None
    })

    # 2. Avversario Bot (Cubo Rosso)
    players.append({
        "x": 50,
        "y": TRACK_Y + 70,       # Posizionamento distanziato nella nuova pista allargata
        "speed": velocita_iniziale,
        "color": ROSSO,
        "finished": False,
        "place": None,
        "prob_verde": 0.75,
        "prob_giallo": 0.80
    })
    return players

players = reset_race()

# -------------------------
# ZONE BARRA (Verde più piccola della gialla)
# -------------------------
green_zone = pygame.Rect(BAR_X + 280, BAR_Y, 40, BAR_HEIGHT)

yellow_zone_left = pygame.Rect(BAR_X + 170, BAR_Y, 110, BAR_HEIGHT)
yellow_zone_right = pygame.Rect(BAR_X + 320, BAR_Y, 110, BAR_HEIGHT)

# -------------------------
# FRECCIA
# -------------------------
arrow_x = BAR_X
arrow_speed = 6.5  
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
# LOOP PRINCIPALE
# -------------------------
running = True

while running:
    clock.tick(FPS)
    screen.fill(NERO)

    # -------------------------
    # GESTIONE EVENTI
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # ESC per uscire dal gioco
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()

            # TASTO SPAZIO PER RESET
            if event.key == pygame.K_SPACE and game_over:
                players = reset_race()
                finish_order = []
                game_over = False
                game_started = False  
                player_position_text = ""
                countdown_start = pygame.time.get_ticks()

        # CLICK MOUSE GIOCATORE
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_started and not game_over:
                arrow_rect = pygame.Rect(arrow_x - 5, BAR_Y - 5, 10, BAR_HEIGHT + 10)

                # BOOST VERDE GIOCATORE (Rimane 3.2)
                if green_zone.colliderect(arrow_rect):
                    players[0]["speed"] = 3.2  
                # VELOCITÀ GIALLA GIOCATORE (Rimane 1.8)
                elif yellow_zone_left.colliderect(arrow_rect) or yellow_zone_right.colliderect(arrow_rect):
                    players[0]["speed"] = 1.8
                # ERRORE ROSSO
                else:
                    players[0]["speed"] = 0.3  

    # -------------------------
    # GESTIONE COUNTDOWN
    # -------------------------
    if not game_started:
        elapsed = (pygame.time.get_ticks() - countdown_start) / 1000
        remaining = COUNTDOWN_TIME - int(elapsed)

        if remaining > 0:
            txt_countdown = str(remaining)
        else:
            txt_countdown = "VIA!"
            
        text = big_font.render(txt_countdown, True, BIANCO)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, TRACK_Y - 80))

        if elapsed >= COUNTDOWN_TIME:
            game_started = True

    # -------------------------
    # LOGICA DI GIOCO
    # -------------------------
    if game_started and not game_over:
        # Movimento freccia indicatore
        arrow_x += arrow_speed * arrow_direction

        if arrow_x >= BAR_X + BAR_WIDTH:
            arrow_x = BAR_X + BAR_WIDTH
            arrow_direction = -1
        if arrow_x <= BAR_X:
            arrow_x = BAR_X
            arrow_direction = 1

        # Trova la testa della corsa
        posizione_leader = max(p["x"] for p in players)

        # Rettangolo della freccia per il calcolo della posizione rispetto alle zone
        arrow_rect = pygame.Rect(arrow_x - 5, BAR_Y - 5, 10, BAR_HEIGHT + 10)

        # LOGICA BOT ROSSO (Velocità potenziata rispetto al giocatore)
        if not players[1]["finished"]:
            
            # Calcoliamo il distacco per la rimonta intelligente
            distacco = posizione_leader - players[1]["x"]
            
            # Bonus riflessi se il bot è dietro (può aggiungere fino a +20% di chance)
            bonus_riflessi = 0.0
            if distacco > 50:
                bonus_riflessi = min(0.20, distacco * 0.001)

            r = random.random()

            # 1. SE LA FRECCIA È SUL VERDE: il bot ottiene un super aumento di velocità (4.2 invece di 3.2)
            if green_zone.colliderect(arrow_rect):
                if r < (players[1]["prob_verde"] + bonus_riflessi):
                    players[1]["speed"] = 4.2  

            # 2. SE LA FRECCIA È SUL GIALLO: il bot ottiene un aumento maggiore (2.3 invece di 1.8)
            elif yellow_zone_left.colliderect(arrow_rect) or yellow_zone_right.colliderect(arrow_rect):
                if r < (players[1]["prob_giallo"] + bonus_riflessi):
                    players[1]["speed"] = 2.3  

            # Aggiornamento movimento continuo del bot rosso
            players[1]["x"] += players[1]["speed"]

        # LOGICA GIOCATORE
        if not players[0]["finished"]:
            players[0]["x"] += players[0]["speed"]

        # GESTIONE ARRIVI TRAGUARDO
        for i, p in enumerate(players):
            if not p["finished"] and p["x"] >= FINISH_X - 20:
                p["finished"] = True
                finish_order.append(i)
                p["place"] = len(finish_order)

                if i == 0:
                    pos = p["place"]
                    if pos == 1:
                        player_position_text = "SEI ARRIVATO 1°! HAI VINTO!"
                    else:
                        player_position_text = "SEI ARRIVATO 2°! HAI PERSO!"

        if len(finish_order) == 2:  
            game_over = True

    # -------------------------
    # RENDERING GRAFICO
    # -------------------------
    
    # Nuova pista allargata
    pygame.draw.rect(screen, GRIGIO_SCURO, (40, TRACK_Y, FINISH_X - 20, TRACK_HEIGHT))

    # Linea del Traguardo
    pygame.draw.line(screen, BIANCO, (FINISH_X, TRACK_Y), (FINISH_X, TRACK_Y + TRACK_HEIGHT), 6)

    # Disegno Quadratini Personaggi (Verde e Rosso)
    for p in players:
        pygame.draw.rect(screen, p["color"], (p["x"], p["y"], 24, 24))  

    # Disegno della Barra dei click
    pygame.draw.rect(screen, ROSSO, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT))
    pygame.draw.rect(screen, GIALLO, yellow_zone_left)
    pygame.draw.rect(screen, GIALLO, yellow_zone_right)
    pygame.draw.rect(screen, VERDE, green_zone)

    # Freccia invertita (Punta verso il basso)
    pygame.draw.polygon(
        screen,
        BIANCO,
        [
            (arrow_x, BAR_Y),        
            (arrow_x - 10, BAR_Y - 15), 
            (arrow_x + 10, BAR_Y - 15)  
        ]
    )

    # Scritte informative di gioco
    info = font.render("Sfida 1v1! Clicca quando la freccia è nel VERDE! (ESC per uscire)", True, BIANCO)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, BAR_Y + 50))

    if player_position_text != "":
        colore_testo = VERDE if "1°" in player_position_text else BIANCO
        pos_text = big_font.render(player_position_text, True, colore_testo)
        screen.blit(pos_text, (WIDTH // 2 - pos_text.get_width() // 2, 60))

    if game_over:
        end_text = font.render("Premi SPAZIO per fare un'altra gara", True, GRIGIO_LUCE)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, 130))

    pygame.display.flip()

pygame.quit()
