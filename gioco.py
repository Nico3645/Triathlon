import pygame
import sys

# 1. Inizializzazione di Pygame
pygame.init()

# Costanti per lo schermo
LARGHEZZA = 800
ALTEZZA = 600
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Scontro di Spinte: Giocatore vs Bot")

# --- COLORI MIGLIORATI ---
BIANCO = (240, 240, 245)      # Bianco ghiaccio pulito per i testi
VERDE = (46, 204, 113)        # Verde Smeraldo brillante per il Giocatore
ROSSO = (231, 76, 60)         # Rosso Corallo acceso per il Bot
GRIGIO = (52, 73, 94)         # Grigio Bluastro elegante per la linea di terra

# Orologio per gli FPS
orologio = pygame.time.Clock()

# Font di sistema standard
font = pygame.font.SysFont("Arial", 24, bold=True)
font_vittoria = pygame.font.SysFont("Arial", 42, bold=True)

# --- VARIABILI DEI PERSONAGGI ---
altezza_personaggi = 100
larghezza_personaggi = 60
linea_terra = ALTEZZA - 150 

# Posizione X del punto di contatto
punto_contatto_x = LARGHEZZA // 2

# Bilanciamento forze
forza_giocatore = 12       
forza_bot_base = 0.30      
forza_bot = forza_bot_base

stato_gioco = "IN_CORSO"   

# --- OTTIMIZZAZIONE DELLO SFONDO SFUMATO ---
# Creiamo una superficie separata per lo sfondo e la disegnamo UNA SOLA VOLTA all'avvio
superficie_sfondo = pygame.Surface((LARGHEZZA, ALTEZZA))
for y in range(ALTEZZA):
    frazione = y / ALTEZZA
    r = int(15 * (1 - frazione) + 30 * frazione)
    g = int(15 * (1 - frazione) + 30 * frazione)
    b = int(25 * (1 - frazione) + 50 * frazione)
    pygame.draw.line(superficie_sfondo, (r, g, b), (0, y), (LARGHEZZA, y))

# --- LOOP PRINCIPALE DEL GIOCO ---
mentre_corre = True
while mentre_corre:
    
    # 2. Gestione degli Eventi
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            mentre_corre = False
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if stato_gioco == "IN_CORSO":
                    punto_contatto_x += forza_giocatore
                else:
                    punto_contatto_x = LARGHEZZA // 2
                    forza_bot = forza_bot_base
                    stato_gioco = "IN_CORSO"

    # 3. Logica del Gioco (Aggiornamenti)
    if stato_gioco == "IN_CORSO":
        punto_contatto_x -= forza_bot
        forza_bot += 0.0007
        
        if punto_contatto_x >= LARGHEZZA:
            stato_gioco = "GIOCATORE_VINCE"
        elif punto_contatto_x <= 0:
            stato_gioco = "BOT_VINCE"

    # Calcolo delle posizioni dei personaggi
    giocatore_x = punto_contatto_x - larghezza_personaggi
    bot_x = punto_contatto_x

    # 4. Rendering Grafico (Disegno)
    
    # Disegna lo sfondo sfumato pre-calcolato (velocissimo, corregge lo schermo nero)
    schermo.blit(superficie_sfondo, (0, 0))
    
    # Disegna la linea di terra
    pygame.draw.line(schermo, GRIGIO, (0, linea_terra), (LARGHEZZA, linea_terra), 6)
    
    # Disegna i Personaggi con bordi smussati
    pygame.draw.rect(schermo, VERDE, (giocatore_x, linea_terra, larghezza_personaggi, altezza_personaggi), border_radius=8)
    pygame.draw.rect(schermo, ROSSO, (bot_x, linea_terra, larghezza_personaggi, altezza_personaggi), border_radius=8)
    
    # Testo di istruzioni in alto con ombra
    testo_info_ombra = font.render("Premi SPAZIO ripetutamente per spingere il Bot fuori dallo schermo!", True, (0, 0, 0))
    testo_info = font.render("Premi SPAZIO ripetutamente per spingere il Bot fuori dallo schermo!", True, BIANCO)
    
    pos_x_testo = LARGHEZZA // 2 - testo_info.get_width() // 2
    schermo.blit(testo_info_ombra, (pos_x_testo + 2, 52)) 
    schermo.blit(testo_info, (pos_x_testo, 50))

    # --- SCHERMATA DI FINE PARTITA ---
    if stato_gioco == "GIOCATORE_VINCE":
        pygame.draw.rect(schermo, (15, 15, 20), (40, 180, 720, 160), border_radius=12)
        pygame.draw.rect(schermo, VERDE, (40, 180, 720, 160), width=3, border_radius=12)
        
        testo_fine = font_vittoria.render("VITTORIA! Hai scaraventato fuori il Bot!", True, VERDE)
        schermo.blit(testo_fine, (LARGHEZZA // 2 - testo_fine.get_width() // 2, 210))
        
        testo_reset = font.render("Premi SPAZIO per un altro round", True, BIANCO)
        schermo.blit(testo_reset, (LARGHEZZA // 2 - testo_reset.get_width() // 2, 280))
        
    elif stato_gioco == "BOT_VINCE":
        pygame.draw.rect(schermo, (15, 15, 20), (40, 180, 720, 160), border_radius=12)
        pygame.draw.rect(schermo, ROSSO, (40, 180, 720, 160), width=3, border_radius=12)
        
        testo_fine = font_vittoria.render("SCONFITTA! Il Bot ti ha buttato fuori!", True, ROSSO)
        schermo.blit(testo_fine, (LARGHEZZA // 2 - testo_fine.get_width() // 2, 210))
        
        testo_reset = font.render("Premi SPAZIO per riprovare", True, BIANCO)
        schermo.blit(testo_reset, (LARGHEZZA // 2 - testo_reset.get_width() // 2, 280))

    # Aggiorna lo schermo intero
    pygame.display.flip()
    
    # Regola la velocità del gioco a 60 FPS
    orologio.tick(60)