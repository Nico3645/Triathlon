import pygame
import sys

# 1. Inizializzazione di Pygame
pygame.init()

# Costanti per lo schermo
LARGHEZZA = 800
ALTEZZA = 600
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Scontro di Spinte: Giocatore vs Bot")

# Colori (RGB)
NERO = (15, 15, 15)
BIANCO = (255, 255, 255)
VERDE = (50, 205, 50)
ROSSO = (220, 20, 60)
GRIGIO = (80, 80, 80)

# Orologio per gli FPS
orologio = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 25)
font_vittoria = pygame.font.SysFont("Arial", 45)

# --- VARIABILI DEI PERSONAGGI ---
altezza_personaggi = 100
larghezza_personaggi = 60
linea_terra = ALTEZZA - 150 # Altezza a cui si trovano i personaggi

# Posizione X del punto di contatto (inizialmente al centro dello schermo)
punto_contatto_x = LARGHEZZA // 2

# Bilanciamento forze
forza_spinta_giocatore = 12  # Pixel guadagnati a ogni pressione di SPAZIO
forza_spinta_bot = 0.4       # Spinta costante del bot per frame

stato_gioco = "IN_CORSO"

# --- LOOP PRINCIPALE ---
running = True
while running:
    
    # 2. Gestione degli Eventi
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and stato_gioco == "IN_CORSO":
                # Il giocatore spinge il punto di contatto verso destra
                punto_contatto_x += forza_spinta_giocatore
                
                # Controllo vittoria Giocatore (se il bot viene spinto fuori dallo schermo a destra)
                if punto_contatto_x >= LARGHEZZA - larghezza_personaggi:
                    punto_contatto_x = LARGHEZZA - larghezza_personaggi
                    stato_gioco = "GIOCATORE_VINCE"

    # 3. Logica di Gioco (Mossa del Bot)
    if stato_gioco == "IN_CORSO":
        # Il bot spinge costantemente il punto di contatto verso sinistra
        punto_contatto_x -= forza_spinta_bot
        
        # Controllo vittoria Bot (se il giocatore viene spinto fuori dallo schermo a sinistra)
        if punto_contatto_x <= larghezza_personaggi:
            punto_contatto_x = larghezza_personaggi
            stato_gioco = "BOT_VINCE"

    # 4. Calcolo posizioni dei personaggi in base al punto di contatto
    # Il giocatore è a sinistra del punto di contatto
    giocatore_x = punto_contatto_x - larghezza_personaggi
    # Il bot è a destra del punto di contatto
    bot_x = punto_contatto_x

    # 5. Rendering (Disegno)
    schermo.fill(NERO)
    
    # Disegna il terreno (una linea grigia spessa)
    pygame.draw.line(schermo, GRIGIO, (0, linea_terra + altezza_personaggi), (LARGHEZZA, linea_terra + altezza_personaggi), 5)
    
    # Disegna il Giocatore (Rettangolo Verde)
    pygame.draw.rect(schermo, VERDE, (giocatore_x, linea_terra, larghezza_personaggi, altezza_personaggi))
    # Disegna il Bot (Rettangolo Rosso)
    pygame.draw.rect(schermo, ROSSO, (bot_x, linea_terra, larghezza_personaggi, altezza_personaggi))
    
    # Mostra le istruzioni in alto
    testo_info = font.render("Premi SPAZIO ripetutamente per spingere il Bot fuori dallo schermo!", True, BIANCO)
    schermo.blit(testo_info, (60, 50))

    # --- SCHERMATA DI FINE PARTITA ---
    if stato_gioco == "GIOCATORE_VINCE":
        testo_fine = font_vittoria.render("VITTORIA! Hai scaraventato fuori il Bot!", True, VERDE)
        schermo.blit(testo_fine, (50, 200))
        testo_reset = font.render("Premi SPAZIO per un altro round", True, BIANCO)
        schermo.blit(testo_reset, (260, 280))
        
    elif stato_gioco == "BOT_VINCE":
        testo_fine = font_vittoria.render("SCONFITTA! Il Bot ti ha buttato fuori!", True, ROSSO)
        schermo.blit(testo_fine, (70, 200))
        testo_reset = font.render("Premi SPAZIO per riprovare", True, BIANCO)
        schermo.blit(testo_reset, (260, 280))

    # Gestione del reset
    if stato_gioco != "IN_CORSO":
        tasti = pygame.key.get_pressed()
        if tasti[pygame.K_SPACE]:
            punto_contatto_x = LARGHEZZA // 2
            stato_gioco = "IN_CORSO"

    pygame.display.flip()
    orologio.tick(60)

pygame.quit()
sys.exit()