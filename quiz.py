import pygame
import random
import json
import os
import time

# =========================
# CONFIGURAZIONE
# =========================
WIDTH, HEIGHT = 1000, 650
FPS = 60

MAX_QUESTIONS = 9
TIME_LIMIT = 90  # 1 minuto e mezzo

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mega Quiz - Anatomia e Matematica")

clock = pygame.time.Clock()

# =========================
# FONT
# =========================
font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 46, bold=True)

# =========================
# PALETTE COLORI (Stile Gioco di Corse - Dark Mode)
# =========================
NERO = (15, 15, 15)
BIANCO = (255, 255, 255)
GRIGIO_SCURO = (35, 35, 35)
GRIGIO_LUCE = (60, 60, 60)

VERDE = (0, 200, 0)
GIALLO = (230, 200, 0)
ROSSO = (220, 60, 60)
BLU = (70, 120, 255)

# =========================
# DOMANDE
# =========================
questions = [
    # ================= MATEMATICA =================
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
    {"question": "Quanto fa 99 - 47?", "options": ["51", "52", "53", "54"], "answer": "52"},
    {"question": "Quanto fa 13 x 13?", "options": ["169", "156", "173", "182"], "answer": "169"},
    {"question": "Quanto fa 5³?", "options": ["100", "110", "125", "150"], "answer": "125"},
    {"question": "Quanto fa 64 ÷ 8?", "options": ["6", "7", "8", "9"], "answer": "8"},
    {"question": "Quanto fa 17 + 29?", "options": ["44", "45", "46", "47"], "answer": "46"},
    {"question": "Quanto fa 20% di 200?", "options": ["20", "30", "40", "50"], "answer": "40"},
    {"question": "Quanto fa 11 x 11?", "options": ["111", "121", "131", "141"], "answer": "121"},
    {"question": "Quanto fa 150 - 78?", "options": ["70", "71", "72", "73"], "answer": "72"},
    {"question": "Quanto fa 3² + 4²?", "options": ["25", "20", "18", "30"], "answer": "25"},
    {"question": "Quanto fa 8 x 7 - 10?", "options": ["46", "48", "50", "52"], "answer": "46"},
    # ================= ANATOMIA =================
    {"question": "Quante ossa ha il corpo umano adulto?", "options": ["206", "180", "250", "300"], "answer": "206"},
    {"question": "Qual è il muscolo principale della respirazione?", "options": ["Diaframma", "Bicipite", "Tricipite", "Quadricipite"], "answer": "Diaframma"},
    {"question": "Quale organo pompa il sangue?", "options": ["Polmone", "Cuore", "Fegato", "Rene"], "answer": "Cuore"},
    {"question": "Qual è l'osso più lungo del corpo?", "options": ["Femore", "Tibia", "Omero", "Radio"], "answer": "Femore"},
    {"question": "Quale parte del cervello controlla l'equilibrio?", "options": ["Cervelletto", "Talamo", "Ipotalamo", "Midollo"], "answer": "Cervelletto"},
    {"question": "Quale sangue trasporta ossigeno?", "options": ["Arterioso", "Venoso", "Capillare", "Linfa"], "answer": "Arterioso"},
    {"question": "Dove si trova l'ulna?", "options": ["Braccio", "Gamba", "Torace", "Testa"], "answer": "Braccio"},
    {"question": "Quanti polmoni ha il corpo umano?", "options": ["1", "2", "3", "4"], "answer": "2"},
    {"question": "Quale organo produce la bile?", "options": ["Cuore", "Fegato", "Pancreas", "Milza"], "answer": "Fegato"},
    {"question": "Quante camere ha il cuore umano?", "options": ["2", "3", "4", "5"], "answer": "4"},
    {"question": "Quale organo filtra il sangue?", "options": ["Polmone", "Rene", "Cuore", "Milza"], "answer": "Rene"},
    {"question": "Qual è il più grande organo del corpo?", "options": ["Fegato", "Pelle", "Cervello", "Polmone"], "answer": "Pelle"},
    {"question": "Dove si trova il femore?", "options": ["Braccio", "Torace", "Gamba", "Testa"], "answer": "Gamba"},
    {"question": "Quale organo controlla il corpo umano?", "options": ["Cuore", "Fegato", "Cervello", "Polmone"], "answer": "Cervello"},
    {"question": "Quanti denti ha normalmente un adulto?", "options": ["28", "30", "32", "36"], "answer": "32"},
    {"question": "Come si chiamano le cellule del cervello?", "options": ["Globuli", "Neuroni", "Tessuti", "Muscoli"], "answer": "Neuroni"},
    {"question": "Quale organo aiuta la digestione?", "options": ["Stomaco", "Cuore", "Polmone", "Milza"], "answer": "Stomaco"},
    {"question": "Dove si trovano le costole?", "options": ["Torace", "Braccio", "Gamba", "Testa"], "answer": "Torace"},
    {"question": "Quale parte del corpo contiene la rotula?", "options": ["Braccio", "Ginocchio", "Collo", "Spalla"], "answer": "Ginocchio"},
    {"question": "Qual è il gruppo sanguigno universale donatore?", "options": ["A", "B", "AB", "0"], "answer": "0"}
]

# =========================
# RECORD
# =========================
RECORD_FILE = "record.json"

def load_record():
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r") as f:
            data = json.load(f)
            return data.get("best_time", None)
    return None

def save_record(seconds):
    with open(RECORD_FILE, "w") as f:
        json.dump({"best_time": seconds}, f)

# =========================
# FUNZIONI GRAFICHE CENTRATE
# =========================
def draw_text(text, font_used, color, x, y):
    render = font_used.render(text, True, color)
    screen.blit(render, (x, y))

def draw_text_centered(text, font_used, color, y):
    render = font_used.render(text, True, color)
    x = WIDTH // 2 - render.get_width() // 2
    screen.blit(render, (x, y))

# =========================
# MENU REPLAY (Stile Moderno)
# =========================
def wait_for_restart():
    while True:
        screen.fill(NERO)

        draw_text_centered("Vuoi ripetere il quiz?", big_font, BIANCO, 200)

        yes_rect = pygame.Rect(WIDTH // 2 - 210, 360, 180, 60)
        no_rect = pygame.Rect(WIDTH // 2 + 30, 360, 180, 60)

        # Rilevamento mouse per effetto Hover pulsanti SI/NO
        mouse_pos = pygame.mouse.get_pos()
        
        color_yes = VERDE if yes_rect.collidepoint(mouse_pos) else GRIGIO_SCURO
        color_no = ROSSO if no_rect.collidepoint(mouse_pos) else GRIGIO_SCURO

        pygame.draw.rect(screen, color_yes, yes_rect)
        pygame.draw.rect(screen, color_no, no_rect)
        pygame.draw.rect(screen, BIANCO, yes_rect, 2)
        pygame.draw.rect(screen, BIANCO, no_rect, 2)

        # Testi pulsanti centrati nei propri box
        txt_yes = font.render("SI", True, BIANCO)
        txt_no = font.render("NO", True, BIANCO)
        screen.blit(txt_yes, (yes_rect.x + (yes_rect.width // 2 - txt_yes.get_width() // 2), yes_rect.y + 15))
        screen.blit(txt_no, (no_rect.x + (no_rect.width // 2 - txt_no.get_width() // 2), no_rect.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    return True
                if no_rect.collidepoint(event.pos):
                    return False

# =========================
# GIOCO
# =========================
def game():
    selected_questions = random.sample(questions, MAX_QUESTIONS)
    score = 0
    current_question = 0
    start_time = time.time()

    while current_question < MAX_QUESTIONS:
        elapsed = int(time.time() - start_time)
        remaining = TIME_LIMIT - elapsed

        if remaining <= 0:
            break

        q = selected_questions[current_question]
        option_rects = []
        running = True

        while running:
            elapsed = int(time.time() - start_time)
            remaining = TIME_LIMIT - elapsed

            if remaining <= 0:
                running = False
                break

            screen.fill(NERO)

            # Header info
            draw_text(f"Domanda {current_question + 1}/{MAX_QUESTIONS}", font, GRIGIO_LUCE, 40, 25)
            
            # Cambia il colore del tempo in rosso fisso se mancano meno di 15 secondi
            timer_color = ROSSO if remaining <= 15 else GIALLO
            draw_text(f"Tempo rimasto: {remaining}s", font, timer_color, 750, 25)

            # Domanda Centrata
            draw_text_centered(q["question"], font, BLU, 110)

            option_rects.clear()
            mouse_pos = pygame.mouse.get_pos()

            # Disegno opzioni di risposta con Hovering luminoso
            for i, option in enumerate(q["options"]):
                rect = pygame.Rect(120, 200 + i * 90, 760, 60)

                # Se il mouse è sopra, la risorsa si colora di Grigio Chiaro e bordo Blu
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, GRIGIO_LUCE, rect)
                    pygame.draw.rect(screen, BLU, rect, 3)
                else:
                    pygame.draw.rect(screen, GRIGIO_SCURO, rect)
                    pygame.draw.rect(screen, BIANCO, rect, 1)

                draw_text(option, font, BIANCO, rect.x + 25, rect.y + 14)
                option_rects.append((rect, option))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, option in option_rects:
                        if rect.collidepoint(event.pos):
                            if option == q["answer"]:
                                score += 1
                            current_question += 1
                            running = False

            clock.tick(FPS)

    # =========================
    # FINE GIOCO & STATISTICHE
    # =========================
    total_time = int(time.time() - start_time)
    best_record = load_record()
    new_record = False

    if best_record is None or total_time < best_record:
        save_record(total_time)
        best_record = total_time
        new_record = True

    # Schermata risultati stile Dark
    screen.fill(NERO)
    draw_text_centered("QUIZ TERMINATO!", big_font, BLU, 80)
    
    draw_text_centered(f"Punteggio Totale: {score}/{MAX_QUESTIONS}", font, BIANCO, 220)
    draw_text_centered(f"Tempo impiegato: {total_time} secondi", font, BIANCO, 280)
    draw_text_centered(f"Record assoluto: {best_record} secondi", font, VERDE, 340)

    if new_record:
        draw_text_centered("NUOVO RECORD!", big_font, ROSSO, 450)

    pygame.display.flip()
    pygame.time.delay(3500)

# =========================
# LOOP PRINCIPALE
# =========================
while True:
    game()
    replay = wait_for_restart()
    if not replay:
        break

pygame.quit()