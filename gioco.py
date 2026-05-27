import pygame
import sys
import random

# 1. Inizializzazione di Pygame
pygame.init()

# Costanti per lo schermo
LARGHEZZA = 800
ALTEZZA = 600
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Scontro di Spinte: Giocatore vs IA")

# --- COLORI MIGLIORATI ---
SFONDO_SCURO = (24, 26, 36)    # Blu notte scuro ultra-veloce (risolve lo schermo nero)
BIANCO = (240, 240, 245)       # Bianco pulito per i testi
VERDE = (46, 204, 113)         # Verde Smeraldo per il Giocatore
ROSSO = (231, 76, 60)          # Rosso Corallo per il Bot
GRIGIO_TERRA = (52, 73, 94)    # Grigio Bluastro per la linea di terra
GRIGIO_OMBRA = (40, 55, 72)    # Colore di contrasto per il terreno

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

# Bilanciamento forze (Giocatore ha una spinta leggermente superiore per bilanciare l'IA)
forza_giocatore = 13       

stato_gioco = "IN_CORSO"   

# --- VARIABILI DELL'INTELLIGENZA ARTIFICIALE (BOT BILANCIATO SENZA STANCHEZZA) ---
forza_spinta_bot = 11      # Forza di ogni singola spinta del bot
timer_decisione_bot = 0    # Frame di attesa tra un click e l'altro del bot

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
                    # Reset della partita
                    punto_contatto_x = LARGHEZZA // 2
                    stato_gioco = "IN_CORSO"
                    timer_decisione_bot = 0

    # 3. Logica del Gioco (Aggiornamenti)
    if stato_gioco == "IN_CORSO":
        
        # Il bot riduce il suo tempo di attesa ad ogni frame
        if timer_decisione_bot > 0:
            timer_decisione_bot -= 1
        
        # Quando il timer scade, il bot esegue la sua mossa
        if timer_decisione_bot == 0:
            pericolo = punto_contatto_x / LARGHEZZA
            
            # Il ritmo del bot si adatta a quanto è vicino a perdere, senza esagerare
            if pericolo > 0.75:
                attesa_minima = 6   # Più reattivo quando sta per perdere
                attesa_massima = 11
            elif pericolo > 0.50:
                attesa_minima = 9   
                attesa_massima = 15
            else:
                attesa_minima = 15  # Più rilassato all'inizio
                attesa_massima = 25
            
            # Il bot applica la spinta verso sinistra
            punto_contatto_x -= forza_spinta_bot
            
            # Genera il prossimo tempo di attesa casuale
            timer_decisione_bot = random.randint(attesa_minima, attesa_massima)

        # Verifica Condizioni di Vittoria/Sconfitta
        if punto_contatto_x >= LARGHEZZA:
            stato_gioco = "GIOCATORE_VINCE"
        elif punto_contatto_x <= 0:
            stato_gioco = "BOT_VINCE"

    # Calcolo delle posizioni dei personaggi
    giocatore_x = punto_contatto_x - larghezza_personaggi
    bot_x = punto_contatto_x

    # 4. Rendering Grafico (Disegno)
    
    # Sfondo istantaneo
    schermo.fill(SFONDO_SCURO)
    
    # Crea la pedana del terreno sotto i personaggi
    pygame.draw.rect(schermo, GRIGIO_OMBRA, (0, linea_terra, LARGHEZZA, ALTEZZA - linea_terra))
    pygame.draw.line(schermo, GRIGIO_TERRA, (0, linea_terra), (LARGHEZZA, linea_terra), 6)
    
    # Disegna i Personaggi con bordi smussati (Giocatore Verde, Bot Rosso)
    pygame.draw.rect(schermo, VERDE, (giocatore_x, linea_terra, larghezza_personaggi, altezza_personaggi), border_radius=8)
    pygame.draw.rect(schermo, ROSSO, (bot_x, linea_terra, larghezza_personaggi, altezza_personaggi), border_radius=8)
    
    # Testo di istruzioni in alto con ombra
    testo_info_ombra = font.render("Premi SPAZIO ripetutamente per battere il Bot!", True, (0, 0, 0))
    testo_info = font.render("Premi SPAZIO ripetutamente per battere il Bot!", True, BIANCO)
    pos_x_testo = LARGHEZZA // 2 - testo_info.get_width() // 2
    schermo.blit(testo_info_ombra, (pos_x_testo + 2, 42)) 
    schermo.blit(testo_info, (pos_x_testo, 40))

    # --- SCHERMATA DI FINE PARTITA ---
    if stato_gioco == "GIOCATORE_VINCE":
        pygame.draw.rect(schermo, (15, 15, 20), (40, 180, 720, 160), border_radius=12)
        pygame.draw.rect(schermo, VERDE, (40, 180, 720, 160), width=3, border_radius=12)
        
        testo_fine = font_vittoria.render("VITTORIA! Hai sconfitto il Bot!", True, VERDE)
        schermo.blit(testo_fine, (LARGHEZZA // 2 - testo_fine.get_width() // 2, 210))
        
        testo_reset = font.render("Premi SPAZIO per un altro round", True, BIANCO)
        schermo.blit(testo_reset, (LARGHEZZA // 2 - testo_reset.get_width() // 2, 280))
        
    elif stato_gioco == "BOT_VINCE":
        pygame.draw.rect(schermo, (15, 15, 20), (40, 180, 720, 160), border_radius=12)
        pygame.draw.rect(schermo, ROSSO, (40, 180, 720, 160), width=3, border_radius=12)
        
        testo_fine = font_vittoria.render("SCONFITTA! Il Bot ha vinto.", True, ROSSO)
        schermo.blit(testo_fine, (LARGHEZZA // 2 - testo_fine.get_width() // 2, 210))
        
        testo_reset = font.render("Premi SPAZIO per riprovare", True, BIANCO)
        schermo.blit(testo_reset, (LARGHEZZA // 2 - testo_reset.get_width() // 2, 280))

    # Aggiorna lo schermo ed esegui il rendering
    pygame.display.flip()
    
    # Fissa il framerate a 60 FPS
    orologio.tick(60)