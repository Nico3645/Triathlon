import pygame
import sys
import random
import os  # Necessario per verificare se il file di salvataggio esiste già

# Inizializza Pygame
pygame.init()

# Dimensioni finestra
LARGHEZZA = 800
ALTEZZA = 600
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Scontro di Spinte")

# Colori base della prima versione
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
VERDE = (0, 200, 0)
ROSSO = (200, 0, 0)
GRIGIO = (100, 100, 100)

# Font di default di Pygame
font_grande = pygame.font.Font(None, 60)
font_medio = pygame.font.Font(None, 40)
font_piccolo = pygame.font.Font(None, 30)

# Variabili di gioco originali
clock = pygame.time.Clock()
# Nuovi stati aggiunti: "PUNTEGGI" per la schermata dei record
stato = "MENU"  

punto_centrale = LARGHEZZA // 2
pos_x = punto_centrale
linea_terra = 450
dim_pg = 80

forza_giocatore = 15
forza_bot = 12

attesa_bot = 0
attesa_min = 10
attesa_max = 20

# --- NUOVE VARIABILI E GESTIONE FILE PER I PUNTEGGI ---
difficolta_corrente = "FACILE"
moltiplicatore = 1
frame_partita = 0
max_pos_x = punto_centrale
punteggio_ottenuto = 0

# Dizionario per i record in memoria
punteggi_record = {"FACILE": 0, "MEDIO": 0, "PAZZO": 0}
FILE_SALVATAGGIO = "classifica.txt"

def carica_punteggi():
    """Legge i record dal file di testo se esiste."""
    if os.path.exists(FILE_SALVATAGGIO):
        try:
            with open(FILE_SALVATAGGIO, "r") as f:
                for linea in f:
                    # Rimuove spazi e divide per il carattere ':'
                    parti = linea.strip().split(":")
                    if len(parti) == 2:
                        diff, punti = parti[0], parti[1]
                        if diff in punteggi_record:
                            punteggi_record[diff] = int(punti)
        except Exception:
            pass # Se il file è corrotto o vuoto, tiene i record a 0

def salva_punteggi():
    """Scrive i record attuali nel file di testo."""
    try:
        with open(FILE_SALVATAGGIO, "w") as f:
            for diff, punti in punteggi_record.items():
                f.write(f"{diff}:{punti}\n")
    except Exception:
        pass

# Carica i punteggi salvati all'avvio del gioco
carica_punteggi()

# Loop principale
while True:
    schermo.fill(NERO) 
    
    # 1. GESTIONE EVENTI (Invariata + click tasto punteggi)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            
            if stato == "MENU":
                if 250 <= x_mouse <= 550:
                    if 200 <= y_mouse <= 250:
                        attesa_min, attesa_max = 15, 25 # FACILE
                        difficolta_corrente = "FACILE"
                        moltiplicatore = 1
                        stato = "GIOCO"
                        pos_x = punto_centrale
                        frame_partita = 0
                        max_pos_x = punto_centrale
                    elif 300 <= y_mouse <= 350:
                        attesa_min, attesa_max = 8, 14  # MEDIO
                        difficolta_corrente = "MEDIO"
                        moltiplicatore = 2
                        stato = "GIOCO"
                        pos_x = punto_centrale
                        frame_partita = 0
                        max_pos_x = punto_centrale
                    elif 400 <= y_mouse <= 450:
                        attesa_min, attesa_max = 2, 8   # PAZZO
                        difficolta_corrente = "PAZZO"
                        moltiplicatore = 3
                        stato = "GIOCO"
                        pos_x = punto_centrale
                        frame_partita = 0
                        max_pos_x = punto_centrale
                    # Click sul nuovo pulsante VEDI PUNTEGGI
                    elif 250 <= y_mouse <= 550:  
                        if 490 <= y_mouse <= 540:
                            stato = "PUNTEGGI"
                            
            elif stato == "PUNTEGGI":
                # Bottone per tornare al menu principale dalla schermata punteggi
                if 250 <= x_mouse <= 550 and 460 <= y_mouse <= 510:
                    stato = "MENU"
                    
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if stato == "GIOCO":
                    pos_x += forza_giocatore 
                elif stato in ["FINE_VITTORIA", "FINE_SCONFITTA"]:
                    stato = "MENU" 

    # 2. LOGICA DEL GIOCO (Invariata + calcolo punteggio a fine partita)
    if stato == "GIOCO":
        frame_partita += 1
        if pos_x > max_pos_x:
            max_pos_x = pos_x

        if attesa_bot > 0:
            attesa_bot -= 1
        else:
            pos_x -= forza_bot 
            attesa_bot = random.randint(attesa_min, attesa_max)
            
        # Controllo condizioni di fine partita e calcolo punteggi
        if pos_x >= LARGHEZZA:
            # Vittoria: più sei veloce, più punti accumuli
            punteggio_ottenuto = int(max(100, 1500 - frame_partita) * moltiplicatore)
            if punteggio_ottenuto > punteggi_record[difficolta_corrente]:
                punteggi_record[difficolta_corrente] = punteggio_ottenuto
                salva_punteggi() # Scrive subito il nuovo record sul file di testo
            stato = "FINE_VITTORIA"
            
        elif pos_x <= 0:
            # Sconfitta: punteggio parziale basato sulla spinta massima raggiunta
            punteggio_ottenuto = int((max_pos_x / LARGHEZZA) * 300 * moltiplicatore)
            if punteggio_ottenuto > punteggi_record[difficolta_corrente]:
                punteggi_record[difficolta_corrente] = punteggio_ottenuto
                salva_punteggi() # Scrive subito il nuovo record sul file di testo
            stato = "FINE_SCONFITTA"

    # 3. DISEGNO SULLO SCHERMO
    if stato == "MENU":
        titolo = font_grande.render("SCONTRO DI SPINTE", True, BIANCO)
        schermo.blit(titolo, (180, 80))
        
        # Pulsanti Difficoltà Originali
        pygame.draw.rect(schermo, VERDE, (250, 200, 300, 50))
        txt_facile = font_medio.render("FACILE", True, NERO)
        schermo.blit(txt_facile, (350, 215))
        
        pygame.draw.rect(schermo, (200, 100, 0), (250, 300, 300, 50))
        txt_medio = font_medio.render("MEDIO", True, NERO)
        schermo.blit(txt_medio, (350, 315))
        
        pygame.draw.rect(schermo, ROSSO, (250, 400, 300, 50))
        txt_pazzo = font_medio.render("PAZZO", True, NERO)
        schermo.blit(txt_pazzo, (350, 415))
        
        # NUOVO PULSANTE: VEDI PUNTEGGI
        pygame.draw.rect(schermo, GRIGIO, (250, 490, 300, 50))
        txt_punteggi = font_medio.render("VEDI PUNTEGGI", True, BIANCO)
        schermo.blit(txt_punteggi, (300, 505))

    elif stato == "PUNTEGGI":
        titolo_punteggi = font_grande.render("MIGLIORI RECORD", True, BIANCO)
        schermo.blit(titolo_punteggi, (220, 80))
        
        # Mostra i record letti dal file / aggiornati in partita
        rec_f = font_medio.render(f"FACILE: {punteggi_record['FACILE']} PT", True, VERDE)
        schermo.blit(rec_f, (280, 200))
        
        rec_m = font_medio.render(f"MEDIO: {punteggi_record['MEDIO']} PT", True, (200, 100, 0))
        schermo.blit(rec_m, (280, 270))
        
        rec_p = font_medio.render(f"PAZZO: {punteggi_record['PAZZO']} PT", True, ROSSO)
        schermo.blit(rec_p, (280, 340))
        
        # Pulsante Torna al Menu
        pygame.draw.rect(schermo, GRIGIO, (250, 460, 300, 50))
        txt_indietro = font_medio.render("TORNA AL MENU", True, BIANCO)
        schermo.blit(txt_indietro, (295, 475))

    elif stato == "GIOCO":
        pygame.draw.line(schermo, GRIGIO, (0, linea_terra), (LARGHEZZA, linea_terra), 5)
        pygame.draw.rect(schermo, VERDE, (pos_x - dim_pg, linea_terra - dim_pg, dim_pg, dim_pg))
        pygame.draw.rect(schermo, ROSSO, (pos_x, linea_terra - dim_pg, dim_pg, dim_pg))
        
        istruzioni = font_piccolo.render("Premi SPAZIO velocemente!", True, BIANCO)
        schermo.blit(istruzioni, (250, 50))

    elif stato == "FINE_VITTORIA":
        msg = font_grande.render("HAI VINTO!", True, VERDE)
        schermo.blit(msg, (280, 180))
        txt_punti = font_medio.render(f"Punteggio: {punteggio_ottenuto} punti", True, BIANCO)
        schermo.blit(txt_punti, (260, 260))
        msg2 = font_piccolo.render("Premi SPAZIO per il Menu", True, BIANCO)
        schermo.blit(msg2, (260, 360))
        
    elif stato == "FINE_SCONFITTA":
        msg = font_grande.render("HAI PERSO!", True, ROSSO)
        schermo.blit(msg, (280, 180))
        txt_punti = font_medio.render(f"Punti di consolazione: {punteggio_ottenuto}", True, BIANCO)
        schermo.blit(txt_punti, (210, 260))
        msg2 = font_piccolo.render("Premi SPAZIO per il Menu", True, BIANCO)
        schermo.blit(msg2, (260, 360))

    pygame.display.flip()
    clock.tick(60)