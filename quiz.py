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
big_font = pygame.font.SysFont("arial", 42)

# =========================
# COLORI
# =========================

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
BLUE = (40, 90, 255)
GREEN = (40, 180, 80)
RED = (220, 60, 60)
GRAY = (210, 210, 210)

# =========================
# DOMANDE
# =========================

questions = [

    # ================= MATEMATICA =================

    {
        "question": "Quanto fa 12 x 8?",
        "options": ["84", "96", "92", "88"],
        "answer": "96"
    },

    {
        "question": "Quanto fa 144 ÷ 12?",
        "options": ["10", "11", "12", "14"],
        "answer": "12"
    },

    {
        "question": "Quanto fa 15²?",
        "options": ["215", "225", "235", "245"],
        "answer": "225"
    },

    {
        "question": "Quanto fa 7 x 9 + 3?",
        "options": ["66", "63", "60", "69"],
        "answer": "66"
    },

    {
        "question": "Quanto fa 81 ÷ 9?",
        "options": ["7", "8", "9", "10"],
        "answer": "9"
    },

    {
        "question": "Quanto fa 25 x 4?",
        "options": ["90", "95", "100", "105"],
        "answer": "100"
    },

    {
        "question": "Quanto fa 18 + 27?",
        "options": ["45", "44", "43", "46"],
        "answer": "45"
    },

    {
        "question": "Quanto fa 9²?",
        "options": ["72", "81", "91", "99"],
        "answer": "81"
    },

    {
        "question": "Quanto fa 56 ÷ 7?",
        "options": ["6", "7", "8", "9"],
        "answer": "8"
    },

    {
        "question": "Quanto fa 14 x 6?",
        "options": ["72", "84", "86", "88"],
        "answer": "84"
    },

    {
        "question": "Quanto fa 99 - 47?",
        "options": ["51", "52", "53", "54"],
        "answer": "52"
    },

    {
        "question": "Quanto fa 13 x 13?",
        "options": ["169", "156", "173", "182"],
        "answer": "169"
    },

    {
        "question": "Quanto fa 5³?",
        "options": ["100", "110", "125", "150"],
        "answer": "125"
    },

    {
        "question": "Quanto fa 64 ÷ 8?",
        "options": ["6", "7", "8", "9"],
        "answer": "8"
    },

    {
        "question": "Quanto fa 17 + 29?",
        "options": ["44", "45", "46", "47"],
        "answer": "46"
    },

    {
        "question": "Quanto fa 20% di 200?",
        "options": ["20", "30", "40", "50"],
        "answer": "40"
    },

    {
        "question": "Quanto fa 11 x 11?",
        "options": ["111", "121", "131", "141"],
        "answer": "121"
    },

    {
        "question": "Quanto fa 150 - 78?",
        "options": ["70", "71", "72", "73"],
        "answer": "72"
    },

    {
        "question": "Quanto fa 3² + 4²?",
        "options": ["25", "20", "18", "30"],
        "answer": "25"
    },

    {
        "question": "Quanto fa 8 x 7 - 10?",
        "options": ["46", "48", "50", "52"],
        "answer": "46"
    },

    # ================= ANATOMIA =================

    {
        "question": "Quante ossa ha il corpo umano adulto?",
        "options": ["206", "180", "250", "300"],
        "answer": "206"
    },

    {
        "question": "Qual è il muscolo principale della respirazione?",
        "options": ["Diaframma", "Bicipite", "Tricipite", "Quadricipite"],
        "answer": "Diaframma"
    },

    {
        "question": "Quale organo pompa il sangue?",
        "options": ["Polmone", "Cuore", "Fegato", "Rene"],
        "answer": "Cuore"
    },

    {
        "question": "Qual è l'osso più lungo del corpo?",
        "options": ["Femore", "Tibia", "Omero", "Radio"],
        "answer": "Femore"
    },

    {
        "question": "Quale parte del cervello controlla l'equilibrio?",
        "options": ["Cervelletto", "Talamo", "Ipotalamo", "Midollo"],
        "answer": "Cervelletto"
    },

    {
        "question": "Quale sangue trasporta ossigeno?",
        "options": ["Arterioso", "Venoso", "Capillare", "Linfa"],
        "answer": "Arterioso"
    },

    {
        "question": "Dove si trova l'ulna?",
        "options": ["Braccio", "Gamba", "Torace", "Testa"],
        "answer": "Braccio"
    },

    {
        "question": "Quanti polmoni ha il corpo umano?",
        "options": ["1", "2", "3", "4"],
        "answer": "2"
    },

    {
        "question": "Quale organo produce la bile?",
        "options": ["Cuore", "Fegato", "Pancreas", "Milza"],
        "answer": "Fegato"
    },

    {
        "question": "Quante camere ha il cuore umano?",
        "options": ["2", "3", "4", "5"],
        "answer": "4"
    },

    {
        "question": "Quale organo filtra il sangue?",
        "options": ["Polmone", "Rene", "Cuore", "Milza"],
        "answer": "Rene"
    },

    {
        "question": "Qual è il più grande organo del corpo?",
        "options": ["Fegato", "Pelle", "Cervello", "Polmone"],
        "answer": "Pelle"
    },

    {
        "question": "Dove si trova il femore?",
        "options": ["Braccio", "Torace", "Gamba", "Testa"],
        "answer": "Gamba"
    },

    {
        "question": "Quale organo controlla il corpo umano?",
        "options": ["Cuore", "Fegato", "Cervello", "Polmone"],
        "answer": "Cervello"
    },

    {
        "question": "Quanti denti ha normalmente un adulto?",
        "options": ["28", "30", "32", "36"],
        "answer": "32"
    },

    {
        "question": "Come si chiamano le cellule del cervello?",
        "options": ["Globuli", "Neuroni", "Tessuti", "Muscoli"],
        "answer": "Neuroni"
    },

    {
        "question": "Quale organo aiuta la digestione?",
        "options": ["Stomaco", "Cuore", "Polmone", "Milza"],
        "answer": "Stomaco"
    },

    {
        "question": "Dove si trovano le costole?",
        "options": ["Torace", "Braccio", "Gamba", "Testa"],
        "answer": "Torace"
    },

    {
        "question": "Quale parte del corpo contiene la rotula?",
        "options": ["Braccio", "Ginocchio", "Collo", "Spalla"],
        "answer": "Ginocchio"
    },

    {
        "question": "Qual è il gruppo sanguigno universale donatore?",
        "options": ["A", "B", "AB", "0"],
        "answer": "0"
    }

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
# FUNZIONI GRAFICHE
# =========================

def draw_text(text, font_used, color, x, y):

    render = font_used.render(text, True, color)

    screen.blit(render, (x, y))


# =========================
# MENU REPLAY
# =========================

def wait_for_restart():

    while True:

        screen.fill(WHITE)

        draw_text("Vuoi ripetere il quiz?", big_font, BLACK, 260, 220)

        yes_rect = pygame.Rect(250, 380, 180, 70)
        no_rect = pygame.Rect(560, 380, 180, 70)

        pygame.draw.rect(screen, GREEN, yes_rect)
        pygame.draw.rect(screen, RED, no_rect)

        draw_text("SI", font, WHITE, 320, 400)
        draw_text("NO", font, WHITE, 630, 400)

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

            screen.fill(WHITE)

            draw_text(
                f"Domanda {current_question + 1}/{MAX_QUESTIONS}",
                font,
                BLACK,
                30,
                20
            )

            draw_text(
                f"Tempo rimasto: {remaining}s",
                font,
                RED,
                720,
                20
            )

            draw_text(q["question"], font, BLUE, 50, 100)

            option_rects.clear()

            for i, option in enumerate(q["options"]):

                rect = pygame.Rect(120, 200 + i * 90, 760, 60)

                pygame.draw.rect(screen, GRAY, rect)

                draw_text(option, font, BLACK, rect.x + 20, rect.y + 15)

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
    # FINE GIOCO
    # =========================

    total_time = int(time.time() - start_time)

    best_record = load_record()

    new_record = False

    if best_record is None or total_time < best_record:

        save_record(total_time)

        best_record = total_time

        new_record = True

    while True:

        screen.fill(WHITE)

        draw_text("QUIZ TERMINATO!", big_font, BLUE, 300, 90)

        draw_text(
            f"Punteggio: {score}/{MAX_QUESTIONS}",
            font,
            BLACK,
            360,
            220
        )

        draw_text(
            f"Tempo usato: {total_time} secondi",
            font,
            BLACK,
            300,
            280
        )

        draw_text(
            f"Record migliore: {best_record} secondi",
            font,
            GREEN,
            250,
            340
        )

        if new_record:

            draw_text(
                "NUOVO RECORD!",
                big_font,
                RED,
                300,
                430
            )

        pygame.display.flip()

        pygame.time.delay(3000)

        break


# =========================
# LOOP PRINCIPALE
# =========================

while True:

    game()

    replay = wait_for_restart()

    if not replay:
        break

pygame.quit()
