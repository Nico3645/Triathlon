import pygame
import sys
import random
import os
import json
import time

# -------------------------
# INIZIALIZZAZIONE & SCHERMO PC
# -------------------------
pygame.init()

info_schermo = pygame.display.Info()
WIDTH = info_schermo.current_w
HEIGHT = info_schermo.current_h

# Il gioco gira a schermo intero adattandosi al tuo PC
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("The Pygame Triathlon Edition")

FPS = 60
clock = pygame.time.Clock()

# -------------------------
# PALETTE COLORI (Unificata Dark Mode)
# -------------------------
NERO = (15, 15, 15)
BIANCO = (255, 255, 255)
GRIGIO_SCURO = (35, 35, 35)
GRIGIO_LUCE = (100, 100, 100)

VERDE = (0, 200, 0)
GIALLO = (230, 200, 0)
ROSSO = (220, 60, 60)
BLU = (70, 120, 255)
ARANCIO = (200, 100, 0)

# Font proporzionati alla risoluzione
font_piccolo = pygame.font.Font(None, int(HEIGHT * 0.035))
font_medio = pygame.font.Font(None, int(HEIGHT * 0.045))
font_grande = pygame.font.Font(None, int(HEIGHT * 0.09))

# FILE DI SALVATAGGIO UNIFICATO
FILE_SALVATAGGIO = "classifica_triathlon.txt"

# Struttura dei record per il Triathlon
record_triathlon = {
    "FORZA": {"FACILE": 0, "MEDIO": 0, "PAZZO": 0},
    "VELOCITA": {"FACILE": 0, "MEDIO": 0, "PAZZO": 0},
    "QUIZ": 0
}

def carica_punteggi():
    global record_triathlon
    if os.path.exists(FILE_SALVATAGGIO):
        try:
            with open(FILE_SALVATAGGIO, "r") as f:
                record_triathlon = json.load(f)
        except Exception:
            pass

def salva_punteggi():
    try:
        with open(FILE_SALVATAGGIO, "w") as f:
            json.dump(record_triathlon, f, indent=4)
    except Exception:
        pass

carica_punteggi()

# -------------------------
# DOMANDE DEL QUIZ
# -------------------------
questions = [
    {"question": "Quanto fa 12 x 8?", "options": ["84", "96", "92", "88"], "answer": "96"},
    {"question": "Quanto fa 144 ÷ 12?", "options": ["10", "11", "12", "14"], "answer": "12"},
    {"question": "Quanto fa 15²?", "options": ["215", "225", "235", "245"], "answer": "225"},
    {"question": "Quanto fa 7 x 9 + 3?", "options": ["66", "63", "60", "69"], "answer": "66"},
    {"question": "Quanto fa 81 ÷ 9?", "options": ["7", "8", "9", "10"], "answer": "9"},
    {"question": "Quanto fa 25 x 4?", "options": ["90", "95", "100", "105"], "answer": "100"},
    {"question": "Quanto fa 18 + 27?", "options": ["45", "44", "43", "46"], "answer": "45"},
    {"question": "Quanto fa 9²?", "options": ["72", "81", "91", "99"], "answer": "81"},
    {"question": "Quanto fa 56 ÷ 7?", "options": ["6", "7", "8", "9"], "answer": "8"},
    {"question": "Quanto fa 14 x 6?", "options": ["72", "84", "86", "88"], "answer": "84"},
    {"question": "Quante ossa ha il corpo umano adulto?", "options": ["206", "180", "250", "300"], "answer": "206"},
    {"question": "Qual è il muscolo principale della respirazione?", "options": ["Diaframma", "Bicipite", "Tricipite", "Quadricipite"], "answer": "Diaframma"},
    {"question": "Quale organo pompa il sangue?", "options": ["Polmone", "Cuore", "Fegato", "Rene"], "answer": "Cuore"},
    {"question": "Qual è l'osso più lungo del corpo?", "options": ["Femore", "Tibia", "Omero", "Radio"], "answer": "Femore"},
    {"question": "Quale parte del cervello controlla l'equilibrio?", "options": ["Cervelletto", "Talamo", "Ipotalamo", "Midollo"], "answer": "Cervelletto"},
    {"question": "Quale sangue trasporta ossigeno?", "options": ["Arterioso", "Venoso", "Capillare", "Linfa"], "answer": "Arterioso"},
    {"question": "Quanti polmoni ha il corpo umano?", "options": ["1", "2", "3", "4"], "answer": "2"},
    {"question": "Quale organo produce la bile?", "options": ["Cuore", "Fegato", "Pancreas", "Milza"], "answer": "Fegato"}
]

# -------------------------
# FUNZIONI DI SUPPORTO GRAFICO
# -------------------------
def draw_text_centered(text, font_used, color, y):
    render = font_used.render(text, True, color)
    x = WIDTH // 2 - render.get_width() // 2
    screen.blit(render, (x, y))

def draw_text(text, font_used, color, x, y):
    render = font_used.render(text, True, color)
    screen.blit(render, (x, y))

# Schermata Selezione Difficoltà (Per Prova 1 e Prova 2)
def seleziona_difficolta(nome_prova):
    while True:
        screen.fill(NERO)
        draw_text_centered(f"SELEZIONA DIFFICOLTÀ - {nome_prova}", font_grande, BLU, HEIGHT // 6)
        
        btn_w, btn_h = 400, 60
        btn_x = WIDTH // 2 - btn_w // 2
        
        rect_f = pygame.Rect(btn_x, HEIGHT // 2 - 100, btn_w, btn_h)
        rect_m = pygame.Rect(btn_x, HEIGHT // 2, btn_w, btn_h)
        rect_p = pygame.Rect(btn_x, HEIGHT // 2 + 100, btn_w, btn_h)
        
        m_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, VERDE if rect_f.collidepoint(m_pos) else GRIGIO_SCURO, rect_f)
        pygame.draw.rect(screen, ARANCIO if rect_m.collidepoint(m_pos) else GRIGIO_SCURO, rect_m)
        pygame.draw.rect(screen, ROSSO if rect_p.collidepoint(m_pos) else GRIGIO_SCURO, rect_p)
        
        for r in [rect_f, rect_m, rect_p]:
            pygame.draw.rect(screen, BIANCO, r, 2)
            
        txt_f = font_medio.render("FACILE", True, BIANCO)
        txt_m = font_medio.render("MEDIO", True, BIANCO)
        txt_p = font_medio.render("PAZZO", True, BIANCO)
        
        screen.blit(txt_f, (rect_f.x + (btn_w // 2 - txt_f.get_width() // 2), rect_f.y + 15))
        screen.blit(txt_m, (rect_m.x + (btn_w // 2 - txt_m.get_width() // 2), rect_m.y + 15))
        screen.blit(txt_p, (rect_p.x + (btn_w // 2 - txt_p.get_width() // 2), rect_p.y + 15))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_f.collidepoint(event.pos): return "FACILE"
                if rect_m.collidepoint(event.pos): return "MEDIO"
                if rect_p.collidepoint(event.pos): return "PAZZO"

# Schermata Risultati Intermedia
def mostra_risultati_intermedi(titolo, punti, record_attuale, testo_bottone):
    while True:
        screen.fill(NERO)
        draw_text_centered(titolo, font_grande, GIALLO, HEIGHT // 5)
        draw_text_centered(f"Punteggio ottenuto in questa prova: {punti} PT", font_medio, BIANCO, HEIGHT // 2 - 40)
        draw_text_centered(f"Record Attuale: {record_attuale} PT", font_medio, VERDE, HEIGHT // 2 + 20)
        
        btn_w, btn_h = 450, 60
        rect_btn = pygame.Rect(WIDTH // 2 - btn_w // 2, HEIGHT - 200, btn_w, btn_h)
        
        m_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, BLU if rect_btn.collidepoint(m_pos) else GRIGIO_SCURO, rect_btn)
        pygame.draw.rect(screen, BIANCO, rect_btn, 2)
        
        txt_btn = font_medio.render(testo_bottone, True, BIANCO)
        screen.blit(txt_btn, (rect_btn.x + (btn_w // 2 - txt_btn.get_width() // 2), rect_btn.y + 15))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_btn.collidepoint(event.pos):
                    return

# -------------------------
# PROVA 1: GIOCO DELLA FORZA (gioco.py)
# -------------------------
def esegui_prova_forza(difficolta):
    if difficolta == "FACILE":
        attesa_min, attesa_max, moltiplicatore = 15, 25, 1
    elif difficolta == "MEDIO":
        attesa_min, attesa_max, moltiplicatore = 8, 14, 2
    else:
        attesa_min, attesa_max, moltiplicatore = 2, 8, 3

    punto_centrale = WIDTH // 2
    pos_x = punto_centrale
    linea_terra = HEIGHT // 2 + 100
    dim_pg = 80
    forza_giocatore = 15
    forza_bot = 12
    attesa_bot = 0
    frame_partita = 0
    max_pos_x = punto_centrale
    punteggio = 0
    
    running = True
    while running:
        screen.fill(NERO)
        frame_partita += 1
        if pos_x > max_pos_x: max_pos_x = pos_x
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pos_x += forza_giocatore
                
        if attesa_bot > 0:
            attesa_bot -= 1
        else:
            pos_x -= forza_bot
            attesa_bot = random.randint(attesa_min, attesa_max)
            
        # Controllo Fine Gioco
        if pos_x >= WIDTH:
            punteggio = int(max(100, 1500 - frame_partita) * moltiplicatore)
            running = False
        elif pos_x <= 0:
            punteggio = int((max_pos_x / WIDTH) * 300 * moltiplicatore)
            running = False
            
        # Grafica Prova 1
        draw_text_centered("PROVA 1: SCONTRO DI FORZA", font_medio, BLU, 50)
        draw_text_centered("Premi SPAZIO velocemente per spingere!", font_piccolo, BIANCO, 110)
        pygame.draw.line(screen, GRIGIO_LUCE, (0, linea_terra), (WIDTH, linea_terra), 5)
        pygame.draw.rect(screen, VERDE, (pos_x - dim_pg, linea_terra - dim_pg, dim_pg, dim_pg))
        pygame.draw.rect(screen, ROSSO, (pos_x, linea_terra - dim_pg, dim_pg, dim_pg))
        
        pygame.display.flip()
        clock.tick(FPS)
        
    if punteggio > record_triathlon["FORZA"][difficolta]:
        record_triathlon["FORZA"][difficolta] = punteggio
        salva_punteggi()
    return punteggio

# -------------------------
# PROVA 2: GIOCO DELLA VELOCITÀ (velocità.py)
# -------------------------
def esegui_prova_velocita(difficolta):
    # Adattamento difficoltà personalizzato per la velocità della freccia e i riflessi del Bot
    if difficolta == "FACILE":
        arrow_speed = 5.0
        prob_v, prob_g = 0.65, 0.70
        moltiplicatore = 1
    elif difficolta == "MEDIO":
        arrow_speed = 7.5
        prob_v, prob_g = 0.78, 0.83
        moltiplicatore = 2
    else:
        arrow_speed = 11.0
        prob_v, prob_g = 0.88, 0.92
        moltiplicatore = 3

    TRACK_Y = HEIGHT // 3
    TRACK_HEIGHT = 120
    FINISH_X = WIDTH - 100
    BAR_WIDTH, BAR_HEIGHT = 600, 30
    BAR_X = (WIDTH - BAR_WIDTH) // 2
    BAR_Y = HEIGHT - 180
    
    players = [
        {"x": 50, "y": TRACK_Y + 20, "speed": 1.0, "color": VERDE, "finished": False, "place": None},
        {"x": 50, "y": TRACK_Y + 70, "speed": 1.0, "color": ROSSO, "finished": False, "place": None, "prob_verde": prob_v, "prob_giallo": prob_g}
    ]
    
    green_zone = pygame.Rect(BAR_X + 280, BAR_Y, 40, BAR_HEIGHT)
    yellow_zone_left = pygame.Rect(BAR_X + 170, BAR_Y, 110, BAR_HEIGHT)
    yellow_zone_right = pygame.Rect(BAR_X + 320, BAR_Y, 110, BAR_HEIGHT)
    
    arrow_x = BAR_X
    arrow_direction = 1
    game_started = False
    game_over = False
    countdown_start = pygame.time.get_ticks()
    finish_order = []
    frame_cronometro = 0

    while not game_over:
        screen.fill(NERO)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game_started and not game_over:
                arrow_rect = pygame.Rect(arrow_x - 5, BAR_Y - 5, 10, BAR_HEIGHT + 10)
                if green_zone.colliderect(arrow_rect): players[0]["speed"] = 3.2
                elif yellow_zone_left.colliderect(arrow_rect) or yellow_zone_right.colliderect(arrow_rect): players[0]["speed"] = 1.8
                else: players[0]["speed"] = 0.3

        if not game_started:
            elapsed = (pygame.time.get_ticks() - countdown_start) / 1000
            remaining = 3 - int(elapsed)
            txt = str(remaining) if remaining > 0 else "VIA!"
            draw_text_centered(txt, font_grande, BIANCO, TRACK_Y - 80)
            if elapsed >= 3: game_started = True
        else:
            frame_cronometro += 1
            arrow_x += arrow_speed * arrow_direction
            if arrow_x >= BAR_X + BAR_WIDTH: arrow_x, arrow_direction = BAR_X + BAR_WIDTH, -1
            if arrow_x <= BAR_X: arrow_x, arrow_direction = BAR_X, 1
            
            # Logica Bot Rosso
            pos_leader = max(p["x"] for p in players)
            arrow_rect = pygame.Rect(arrow_x - 5, BAR_Y - 5, 10, BAR_HEIGHT + 10)
            if not players[1]["finished"]:
                distacco = pos_leader - players[1]["x"]
                bonus = min(0.20, distacco * 0.001) if distacco > 50 else 0.0
                r = random.random()
                if green_zone.colliderect(arrow_rect) and r < (players[1]["prob_verde"] + bonus): players[1]["speed"] = 4.2
                elif (yellow_zone_left.colliderect(arrow_rect) or yellow_zone_right.colliderect(arrow_rect)) and r < (players[1]["prob_giallo"] + bonus): players[1]["speed"] = 2.3
                players[1]["x"] += players[1]["speed"]
                
            # Logica Giocatore
            if not players[0]["finished"]: players[0]["x"] += players[0]["speed"]
            
            # Arrivi
            for i, p in enumerate(players):
                if not p["finished"] and p["x"] >= FINISH_X - 20:
                    p["finished"] = True
                    finish_order.append(i)
                    p["place"] = len(finish_order)
            if len(finish_order) == 2: game_over = True

        # Rendering Visivo
        pygame.draw.rect(screen, GRIGIO_SCURO, (40, TRACK_Y, FINISH_X - 20, TRACK_HEIGHT))
        pygame.draw.line(screen, BIANCO, (FINISH_X, TRACK_Y), (FINISH_X, TRACK_Y + TRACK_HEIGHT), 6)
        for p in players: pygame.draw.rect(screen, p["color"], (p["x"], p["y"], 24, 24))
        pygame.draw.rect(screen, ROSSO, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, GIALLO, yellow_zone_left); pygame.draw.rect(screen, GIALLO, yellow_zone_right)
        pygame.draw.rect(screen, VERDE, green_zone)
        pygame.draw.polygon(screen, BIANCO, [(arrow_x, BAR_Y), (arrow_x - 10, BAR_Y - 15), (arrow_x + 10, BAR_Y - 15)])
        draw_text_centered("PROVA 2: GARA DI VELOCITÀ - Clicca sulla zona VERDE!", font_medio, BIANCO, BAR_Y + 50)
        pygame.display.flip()
        clock.tick(FPS)

    # Calcolo punteggio finale in base alle performance
    if players[0]["place"] == 1:
        punteggio = int(max(200, 2000 - frame_cronometro) * moltiplicatore)
    else:
        punteggio = int(max(50, 500 - frame_cronometro) * moltiplicatore)

    if punteggio > record_triathlon["VELOCITA"][difficolta]:
        record_triathlon["VELOCITA"][difficolta] = punteggio
        salva_punteggi()
    return punteggio

# -------------------------
# PROVA 3: MEGA QUIZ (quiz.py)
# -------------------------
def esegui_prova_quiz():
    MAX_QUESTIONS = 9
    TIME_LIMIT = 90
    selected_questions = random.sample(questions, MAX_QUESTIONS)
    score = 0
    current_question = 0
    start_time = time.time()

    while current_question < MAX_QUESTIONS:
        elapsed = int(time.time() - start_time)
        remaining = TIME_LIMIT - elapsed
        if remaining <= 0: break
        
        q = selected_questions[current_question]
        option_rects = []
        running = True

        while running:
            elapsed = int(time.time() - start_time)
            remaining = TIME_LIMIT - elapsed
            if remaining <= 0: running = False; break

            screen.fill(NERO)
            draw_text(f"Domanda {current_question + 1}/{MAX_QUESTIONS}", font_medio, GRIGIO_LUCE, 40, 25)
            timer_color = ROSSO if remaining <= 15 else GIALLO
            draw_text(f"Tempo: {remaining}s", font_medio, timer_color, WIDTH - 200, 25)
            draw_text_centered(q["question"], font_medio, BLU, HEIGHT // 5)

            option_rects.clear()
            m_pos = pygame.mouse.get_pos()

            for i, option in enumerate(q["options"]):
                rect = pygame.Rect(WIDTH // 2 - 380, HEIGHT // 3 + i * 85, 760, 55)
                if rect.collidepoint(m_pos):
                    pygame.draw.rect(screen, GRIGIO_LUCE, rect)
                    pygame.draw.rect(screen, BLU, rect, 3)
                else:
                    pygame.draw.rect(screen, GRIGIO_SCURO, rect)
                    pygame.draw.rect(screen, BIANCO, rect, 1)
                draw_text(option, font_medio, BIANCO, rect.x + 25, rect.y + 12)
                option_rects.append((rect, option))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, option in option_rects:
                        if rect.collidepoint(event.pos):
                            if option == q["answer"]: score += 1
                            current_question += 1
                            running = False
            clock.tick(FPS)

    total_time = int(time.time() - start_time)
    # Calcolo Punteggio Dinamico del Quiz: più risposte corrette e minor tempo = più punti!
    tempo_bonus = max(0, TIME_LIMIT - total_time)
    punteggio_finale = (score * 200) + (tempo_bonus * 10)

    if punteggio_finale > record_triathlon["QUIZ"]:
        record_triathlon["QUIZ"] = punteggio_finale
        salva_punteggi()
    return score, total_time, punteggio_finale

# -------------------------
# VISUALIZZAZIONE SCHERMATA PUNTEGGI RECORD
# -------------------------
def mostra_schermata_classifiche():
    while True:
        screen.fill(NERO)
        draw_text_centered("MIGLIORI RECORD TRIATHLON", font_grande, GIALLO, 50)
        
        # Colonne e Righe organizzate pulite
        y_offset = HEIGHT // 4 + 20
        draw_text("PROVA 1 (FORZA):", font_medio, BLU, WIDTH // 4, y_offset)
        draw_text(f"Facile: {record_triathlon['FORZA']['FACILE']} PT | Medio: {record_triathlon['FORZA']['MEDIO']} PT | Pazzo: {record_triathlon['FORZA']['PAZZO']} PT", font_piccolo, BIANCO, WIDTH // 4, y_offset + 40)
        
        draw_text("PROVA 2 (VELOCITÀ):", font_medio, BLU, WIDTH // 4, y_offset + 120)
        draw_text(f"Facile: {record_triathlon['VELOCITA']['FACILE']} PT | Medio: {record_triathlon['VELOCITA']['MEDIO']} PT | Pazzo: {record_triathlon['VELOCITA']['PAZZO']} PT", font_piccolo, BIANCO, WIDTH // 4, y_offset + 160)
        
        draw_text("PROVA 3 (MEGA QUIZ):", font_medio, BLU, WIDTH // 4, y_offset + 240)
        draw_text(f"Record Assoluto: {record_triathlon['QUIZ']} PT", font_piccolo, VERDE, WIDTH // 4, y_offset + 280)
        
        btn_w, btn_h = 300, 50
        rect_back = pygame.Rect(WIDTH // 2 - btn_w // 2, HEIGHT - 150, btn_w, btn_h)
        m_pos = pygame.mouse.get_pos()
        
        pygame.draw.rect(screen, ROSSO if rect_back.collidepoint(m_pos) else GRIGIO_SCURO, rect_back)
        pygame.draw.rect(screen, BIANCO, rect_back, 2)
        txt_back = font_medio.render("TORNA AL MENU", True, BIANCO)
        screen.blit(txt_back, (rect_back.x + (btn_w // 2 - txt_back.get_width() // 2), rect_back.y + 12))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_back.collidepoint(event.pos): return

# -------------------------
# STREAM PRINCIPALE DEL MENU
# -------------------------
def menu_principale():
    while True:
        screen.fill(NERO)
        draw_text_centered("THE PYGAME TRIATHLON", font_grande, BIANCO, HEIGHT // 4)
        
        btn_w, btn_h = 450, 60
        btn_x = WIDTH // 2 - btn_w // 2
        
        rect_start = pygame.Rect(btn_x, HEIGHT // 2, btn_w, btn_h)
        rect_scores = pygame.Rect(btn_x, HEIGHT // 2 + 90, btn_w, btn_h)
        rect_exit = pygame.Rect(btn_x, HEIGHT // 2 + 180, btn_w, btn_h)
        
        m_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, VERDE if rect_start.collidepoint(m_pos) else GRIGIO_SCURO, rect_start)
        pygame.draw.rect(screen, BLU if rect_scores.collidepoint(m_pos) else GRIGIO_SCURO, rect_scores)
        pygame.draw.rect(screen, ROSSO if rect_exit.collidepoint(m_pos) else GRIGIO_SCURO, rect_exit)
        
        for r in [rect_start, rect_scores, rect_exit]:
            pygame.draw.rect(screen, BIANCO, r, 2)
            
        txt_start = font_medio.render("INIZIA IL TRIATHLON", True, BIANCO)
        txt_scores = font_medio.render("VEDI PUNTEGGI", True, BIANCO)
        txt_exit = font_medio.render("ESCI DAL GIOCO", True, BIANCO)
        
        screen.blit(txt_start, (rect_start.x + (btn_w // 2 - txt_start.get_width() // 2), rect_start.y + 15))
        screen.blit(txt_scores, (rect_scores.x + (btn_w // 2 - txt_scores.get_width() // 2), rect_scores.y + 15))
        screen.blit(txt_exit, (rect_exit.x + (btn_w // 2 - txt_exit.get_width() // 2), rect_exit.y + 15))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_start.collidepoint(event.pos):
                    esegui_flusso_triathlon()
                if rect_scores.collidepoint(event.pos):
                    mostra_schermata_classifiche()
                if rect_exit.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

# -------------------------
# FLUSSO SEQUENZIALE DELLE PROVE
# -------------------------
def esegui_flusso_triathlon():
    # --- PROVA 1 ---
    diff_forza = seleziona_difficolta("PROVA 1: FORZA")
    punti_forza = esegui_prova_forza(diff_forza)
    mostra_risultati_intermedi("PROVA 1 COMPLETATA!", punti_forza, record_triathlon["FORZA"][diff_forza], "PROSEGUI ALLA PROVA 2 (VELOCITÀ)")
    
    # --- PROVA 2 ---
    diff_vel = seleziona_difficolta("PROVA 2: VELOCITÀ")
    punti_vel = esegui_prova_velocita(diff_vel)
    mostra_risultati_intermedi("PROVA 2 COMPLETATA!", punti_vel, record_triathlon["VELOCITA"][diff_vel], "PROSEGUI ALL'ULTIMA PROVA (MEGA QUIZ)")
    
    # --- PROVA 3 ---
    risposte_esatte, tempo, punti_quiz = esegui_prova_quiz()
    
    # Schermata Finale Completa del Triathlon
    while True:
        screen.fill(NERO)
        draw_text_centered("TRIATHLON CONCLUSO!", font_grande, VERDE, 60)
        
        y_res = HEIGHT // 3
        draw_text_centered(f"1° Prova (Forza - {diff_forza}): {punti_forza} PT", font_medio, BIANCO, y_res)
        draw_text_centered(f"2° Prova (Velocità - {diff_vel}): {punti_vel} PT", font_medio, BIANCO, y_res + 50)
        draw_text_centered(f"3° Prova (Quiz - Risposte {risposte_esatte}/9 in {tempo}s): {punti_quiz} PT", font_medio, BIANCO, y_res + 100)
        
        punteggio_totale_triathlon = punti_forza + punti_vel + punti_quiz
        draw_text_centered(f"PUNTEGGIO TOTALE TRIATHLON: {punteggio_totale_triathlon} PT", font_medio, GIALLO, y_res + 200)
        
        btn_w, btn_h = 400, 60
        rect_back_menu = pygame.Rect(WIDTH // 2 - btn_w // 2, HEIGHT - 180, btn_w, btn_h)
        m_pos = pygame.mouse.get_pos()
        
        pygame.draw.rect(screen, BLU if rect_back_menu.collidepoint(m_pos) else GRIGIO_SCURO, rect_back_menu)
        pygame.draw.rect(screen, BIANCO, rect_back_menu, 2)
        txt_menu = font_medio.render("TORNA AL MENU PRINCIPALE", True, BIANCO)
        screen.blit(txt_menu, (rect_back_menu.x + (btn_w // 2 - txt_menu.get_width() // 2), rect_back_menu.y + 15))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_back_menu.collidepoint(event.pos):
                    return

# Avvio del Gioco
if __name__ == "__main__":
    menu_principale()