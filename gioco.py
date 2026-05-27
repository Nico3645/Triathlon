import pygame
import sys
import random

# Inizializza Pygame (fondamentale)
pygame.init()

# Dimensioni finestra
LARGHEZZA = 800
ALTEZZA = 600
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Scontro di Spinte")

# Colori base sicuri
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
VERDE = (0, 200, 0)
ROSSO = (200, 0, 0)
GRIGIO = (100, 100, 100)

# Font di default di Pygame (il 'None' assicura che funzioni su tutti i PC)
font_grande = pygame.font.Font(None, 60)
font_medio = pygame.font.Font(None, 40)
font_piccolo = pygame.font.Font(None, 30)

# Variabili di gioco
clock = pygame.time.Clock()
stato = "MENU"  # Può essere "MENU", "GIOCO", "FINE_VITTORIA", "FINE_SCONFITTA"

# Posizione e dimensioni
punto_centrale = LARGHEZZA // 2
pos_x = punto_centrale
linea_terra = 450
dim_pg = 80

# Forze
forza_giocatore = 15
forza_bot = 12

# Difficoltà (ritmo del bot)
attesa_bot = 0
attesa_min = 10
attesa_max = 20

# Loop principale
while True:
    schermo.fill(NERO) # Sfondo sempre nero per sicurezza
    
    # 1. GESTIONE EVENTI (Tasti e Mouse)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Click del mouse nel menu
        if evento.type == pygame.MOUSEBUTTONDOWN and stato == "MENU":
            x_mouse, y_mouse = pygame.mouse.get_pos()
            
            # Controlla quale difficoltà è stata cliccata
            if 250 <= x_mouse <= 550:
                if 200 <= y_mouse <= 250:
                    attesa_min, attesa_max = 15, 25 # FACILE
                    stato = "GIOCO"
                    pos_x = punto_centrale
                elif 300 <= y_mouse <= 350:
                    attesa_min, attesa_max = 8, 14  # MEDIO
                    stato = "GIOCO"
                    pos_x = punto_centrale
                elif 400 <= y_mouse <= 450:
                    attesa_min, attesa_max = 2, 7   # PAZZO
                    stato = "GIOCO"
                    pos_x = punto_centrale
                    
        # Pressione barra spaziatrice
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if stato == "GIOCO":
                    pos_x += forza_giocatore # Spingi a destra
                elif stato == "FINE_VITTORIA" or stato == "FINE_SCONFITTA":
                    stato = "MENU" # Torna al menu

    # 2. LOGICA DEL GIOCO
    if stato == "GIOCO":
        # Il bot agisce a intervalli
        if attesa_bot > 0:
            attesa_bot -= 1
        else:
            pos_x -= forza_bot # Il bot spinge a sinistra
            attesa_bot = random.randint(attesa_min, attesa_max)
            
        # Controlla chi ha vinto
        if pos_x >= LARGHEZZA:
            stato = "FINE_VITTORIA"
        elif pos_x <= 0:
            stato = "FINE_SCONFITTA"

    # 3. DISEGNO SULLO SCHERMO
    if stato == "MENU":
        titolo = font_grande.render("SCONTRO DI SPINTE", True, BIANCO)
        schermo.blit(titolo, (180, 80))
        
        # Pulsanti
        pygame.draw.rect(schermo, VERDE, (250, 200, 300, 50))
        txt_facile = font_medio.render("FACILE", True, NERO)
        schermo.blit(txt_facile, (350, 215))
        
        pygame.draw.rect(schermo, (200, 100, 0), (250, 300, 300, 50))
        txt_medio = font_medio.render("MEDIO", True, NERO)
        schermo.blit(txt_medio, (350, 315))
        
        pygame.draw.rect(schermo, ROSSO, (250, 400, 300, 50))
        txt_pazzo = font_medio.render("PAZZO", True, NERO)
        schermo.blit(txt_pazzo, (350, 415))

    elif stato == "GIOCO":
        # Linea del suolo
        pygame.draw.line(schermo, GRIGIO, (0, linea_terra), (LARGHEZZA, linea_terra), 5)
        
        # Personaggi
        pygame.draw.rect(schermo, VERDE, (pos_x - dim_pg, linea_terra - dim_pg, dim_pg, dim_pg))
        pygame.draw.rect(schermo, ROSSO, (pos_x, linea_terra - dim_pg, dim_pg, dim_pg))
        
        istruzioni = font_piccolo.render("Premi SPAZIO velocemente!", True, BIANCO)
        schermo.blit(istruzioni, (250, 50))

    elif stato == "FINE_VITTORIA":
        msg = font_grande.render("HAI VINTO!", True, VERDE)
        schermo.blit(msg, (280, 200))
        msg2 = font_piccolo.render("Premi SPAZIO per il Menu", True, BIANCO)
        schermo.blit(msg2, (260, 300))
        
    elif stato == "FINE_SCONFITTA":
        msg = font_grande.render("HAI PERSO!", True, ROSSO)
        schermo.blit(msg, (280, 200))
        msg2 = font_piccolo.render("Premi SPAZIO per il Menu", True, BIANCO)
        schermo.blit(msg2, (260, 300))

    pygame.display.flip()
    clock.tick(60)