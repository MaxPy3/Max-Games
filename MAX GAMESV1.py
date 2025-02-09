import pygame
import sys
import random
import time

# Inizializzazione
pygame.init()

# Configurazioni globali
MENU_WIDTH, MENU_HEIGHT = 1280, 720
TETRIS_WIDTH, TETRIS_HEIGHT = 400, 800
PACMAN_WIDTH, PACMAN_HEIGHT = 600, 600
FPS = 60
CELL_SIZE = 30

# Colori
COLORS = {
    "background": (10, 10, 30),
    "neon_blue": (0, 200, 255),
    "neon_pink": (255, 0, 127),
    "text": (255, 255, 255),  # Bianco
    "grid": (50, 50, 80),
    "piece": (200, 200, 200),
    "code_bg": (20, 20, 50),
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "pink": (255, 184, 255),
    "cyan": (0, 255, 255),
    "orange": (255, 184, 82),
    "hack_bg": (30, 30, 60),
    "hack_text": (0, 255, 0)
}

# Setup finestre
menu_screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pygame.display.set_caption("MAX GAMES")
clock = pygame.time.Clock()

# Font
try:
    title_font = pygame.font.Font("Retro Gaming.ttf", 100)
    menu_font = pygame.font.Font("Retro Gaming.ttf", 40)
    code_font = pygame.font.Font("Retro Gaming.ttf", 25)
    hack_font = pygame.font.Font("Retro Gaming.ttf", 30)
except:
    title_font = pygame.font.SysFont("arialblack", 80)
    menu_font = pygame.font.SysFont("consolas", 40)
    code_font = pygame.font.SysFont("consolas", 25)
    hack_font = pygame.font.SysFont("consolas", 30)

# Variabili globali
input_code = ""
show_credit = False
credit_timer = 0
show_hack_menu = False
hacks = {
    "immortality": False,
    "infinite_lives": False,
    "super_speed": False
}

# Animazione iniziale
def show_start_animation():
    start_time = time.time()
    progress = 0
    
    while progress < 100:
        menu_screen.fill(COLORS["background"])
        
        title = title_font.render("MAX GAMES", True, COLORS["neon_blue"])
        menu_screen.blit(title, (MENU_WIDTH//2 - title.get_width()//2, MENU_HEIGHT//2 - 100))
        pygame.draw.rect(menu_screen, COLORS["grid"], (MENU_WIDTH//2-150, MENU_HEIGHT//2+50, 300, 20))
        pygame.draw.rect(menu_screen, COLORS["neon_pink"], (MENU_WIDTH//2-145, MENU_HEIGHT//2+55, 2.9*progress, 10))
        
        pygame.display.update()
        progress = min(100, (time.time() - start_time) * 40)
        clock.tick(60)

# Schermata di game over per Snake
def game_over_screen(score):
    while True:
        menu_screen.fill(COLORS["background"])
        
        title = title_font.render("GAME OVER", True, COLORS["neon_pink"])
        menu_screen.blit(title, (MENU_WIDTH//2 - title.get_width()//2, 200))
        
        score_text = menu_font.render(f"Score: {score}", True, COLORS["text"])
        menu_screen.blit(score_text, (MENU_WIDTH//2 - score_text.get_width()//2, 350))
        
        info_text = menu_font.render("Press ESC to return", True, COLORS["text"])
        menu_screen.blit(info_text, (MENU_WIDTH//2 - info_text.get_width()//2, 500))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

# Barra del codice e scritta crediti
def draw_code_input():
    # Barra codice in alto a sinistra
    pygame.draw.rect(menu_screen, COLORS["code_bg"], (10, 10, 200, 40))
    code_text = code_font.render(f"CODE: {input_code}", True, COLORS["text"])
    menu_screen.blit(code_text, (15, 15))
    
    # Scritta crediti in basso al centro
    if show_credit:
        credit_text = title_font.render("Game By Massimiliano", True, COLORS["text"])
        text_rect = credit_text.get_rect(center=(MENU_WIDTH//2, MENU_HEIGHT - 50))
        menu_screen.blit(credit_text, text_rect)

# Menu delle hack
def draw_hack_menu():
    pygame.draw.rect(menu_screen, COLORS["hack_bg"], (MENU_WIDTH//2 - 200, MENU_HEIGHT//2 - 150, 400, 300))
    title = hack_font.render("HACK MENU", True, COLORS["hack_text"])
    menu_screen.blit(title, (MENU_WIDTH//2 - title.get_width()//2, MENU_HEIGHT//2 - 120))
    
    hacks_list = [
        f"1. Immortality: {'ON' if hacks['immortality'] else 'OFF'}",
        f"2. Infinite Lives: {'ON' if hacks['infinite_lives'] else 'OFF'}",
        f"3. Super Speed: {'ON' if hacks['super_speed'] else 'OFF'}"
    ]
    
    for i, hack in enumerate(hacks_list):
        text = hack_font.render(hack, True, COLORS["hack_text"])
        menu_screen.blit(text, (MENU_WIDTH//2 - 180, MENU_HEIGHT//2 - 80 + i * 40))
    
    info_text = hack_font.render("Press ESC to close", True, COLORS["hack_text"])
    menu_screen.blit(info_text, (MENU_WIDTH//2 - info_text.get_width()//2, MENU_HEIGHT//2 + 100))

# Menu principale
def main_menu():
    global input_code, show_credit, credit_timer, show_hack_menu
    
    buttons = [
        {"text": "TETRIS", "pos": (MENU_WIDTH//2-100, 300), "action": start_tetris},
        {"text": "SNAKE", "pos": (MENU_WIDTH//2-100, 400), "action": start_snake},
        {"text": "PAC-MAN", "pos": (MENU_WIDTH//2-100, 500), "action": start_pacman},
        {"text": "EXIT", "pos": (MENU_WIDTH//2-100, 600), "action": "exit"}
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        menu_screen.fill(COLORS["background"])
        
        # Titolo principale
        title = title_font.render("MAX GAMES", True, COLORS["neon_blue"])
        menu_screen.blit(title, (MENU_WIDTH//2 - title.get_width()//2, 50))
        
        # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, 
                               pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                               pygame.K_8, pygame.K_9]:
                    input_code += event.unicode
                    if len(input_code) > 4:
                        input_code = input_code[-4:]
                    if input_code == "0905":
                        show_credit = True
                        credit_timer = pygame.time.get_ticks()
                        input_code = ""
                    if input_code == "9452":
                        show_hack_menu = True
                        input_code = ""
                
                if event.key == pygame.K_ESCAPE:
                    input_code = ""
                    show_hack_menu = False
                
                if show_hack_menu:
                    if event.key == pygame.K_1:
                        hacks["immortality"] = not hacks["immortality"]
                    if event.key == pygame.K_2:
                        hacks["infinite_lives"] = not hacks["infinite_lives"]
                    if event.key == pygame.K_3:
                        hacks["super_speed"] = not hacks["super_speed"]
        
        # Disegno pulsanti
        for btn in buttons:
            text = menu_font.render(btn["text"], True, COLORS["text"])
            rect = pygame.Rect(btn["pos"][0], btn["pos"][1], 200, 50)
            
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(menu_screen, COLORS["neon_pink"], rect, border_radius=15)
                if pygame.mouse.get_pressed()[0]:
                    if btn["action"] == "exit":
                        pygame.quit()
                        sys.exit()
                    else:
                        btn["action"]()
            pygame.draw.rect(menu_screen, COLORS["neon_blue"], rect, 3, border_radius=15)
            menu_screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))
        
        # Elementi codice e crediti
        draw_code_input()
        
        # Menu delle hack
        if show_hack_menu:
            draw_hack_menu()
        
        # Timer crediti
        if show_credit and pygame.time.get_ticks() - credit_timer > 3000:
            show_credit = False
        
        pygame.display.update()
        clock.tick(FPS)

# TETRIS
def start_tetris():
    tetris_screen = pygame.display.set_mode((TETRIS_WIDTH, TETRIS_HEIGHT))
    pygame.display.set_caption("MAX GAMES - Tetris")
    
    COLS, ROWS = 10, 20
    GRID_WIDTH = COLS * CELL_SIZE
    GRID_HEIGHT = ROWS * CELL_SIZE
    GRID_OFFSET_X = (TETRIS_WIDTH - GRID_WIDTH) // 2
    
    board = [[0]*COLS for _ in range(ROWS)]
    shapes = [
        [[1,1,1,1]], [[1,1],[1,1]], [[1,1,1],[0,1,0]],
        [[1,1,1],[1,0,0]], [[1,1,1],[0,0,1]], 
        [[1,1,0],[0,1,1]], [[0,1,1],[1,1,0]]
    ]
    current_piece = random.choice(shapes)
    piece_color = COLORS["neon_blue"]
    piece_pos = [COLS//2 - len(current_piece[0])//2, 0]
    last_move = pygame.time.get_ticks()
    move_delay = 200

    def draw_grid():
        for x in range(COLS + 1):
            start_pos = (GRID_OFFSET_X + x * CELL_SIZE, 0)
            end_pos = (GRID_OFFSET_X + x * CELL_SIZE, GRID_HEIGHT)
            pygame.draw.line(tetris_screen, COLORS["grid"], start_pos, end_pos)
        
        for y in range(ROWS + 1):
            start_pos = (GRID_OFFSET_X, y * CELL_SIZE)
            end_pos = (GRID_OFFSET_X + GRID_WIDTH, y * CELL_SIZE)
            pygame.draw.line(tetris_screen, COLORS["grid"], start_pos, end_pos)

    def check_collision():
        for y, row in enumerate(current_piece):
            for x, cell in enumerate(row):
                if cell:
                    if (piece_pos[0]+x < 0 or piece_pos[0]+x >= COLS or
                        piece_pos[1]+y >= ROWS or board[piece_pos[1]+y][piece_pos[0]+x]):
                        return True
        return False

    while True:
        current_time = pygame.time.get_ticks()
        tetris_screen.fill(COLORS["background"])
        
        # Gestione input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    return
                if event.key == pygame.K_RETURN:
                    while not check_collision():
                        piece_pos[1] += 1
                    piece_pos[1] -= 1
                    for y, row in enumerate(current_piece):
                        for x, cell in enumerate(row):
                            if cell:
                                board[piece_pos[1]+y][piece_pos[0]+x] = piece_color
                    current_piece = random.choice(shapes)
                    piece_pos = [COLS//2 - len(current_piece[0])//2, 0]
                    if check_collision():
                        pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                        return

        # Movimento orizzontale
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and current_time - last_move > move_delay:
            piece_pos[0] -= 1
            if check_collision():
                piece_pos[0] += 1
            last_move = current_time
        if keys[pygame.K_RIGHT] and current_time - last_move > move_delay:
            piece_pos[0] += 1
            if check_collision():
                piece_pos[0] -= 1
            last_move = current_time

        # Caduta automatica
        if current_time - last_move > 1000:
            piece_pos[1] += 1
            if check_collision():
                piece_pos[1] -= 1
                for y, row in enumerate(current_piece):
                    for x, cell in enumerate(row):
                        if cell:
                            board[piece_pos[1]+y][piece_pos[0]+x] = piece_color
                current_piece = random.choice(shapes)
                piece_pos = [COLS//2 - len(current_piece[0])//2, 0]
                if check_collision():
                    pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    return
            last_move = current_time

        # Disegno elementi
        for y in range(ROWS):
            for x in range(COLS):
                if board[y][x]:
                    pygame.draw.rect(tetris_screen, board[y][x],
                                   (GRID_OFFSET_X + x*CELL_SIZE + 1, y*CELL_SIZE + 1, CELL_SIZE-2, CELL_SIZE-2))
        
        for y, row in enumerate(current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(tetris_screen, piece_color,
                                   (GRID_OFFSET_X + (piece_pos[0]+x)*CELL_SIZE + 1,
                                    (piece_pos[1]+y)*CELL_SIZE + 1,
                                    CELL_SIZE-2, CELL_SIZE-2))
        
        draw_grid()
        pygame.display.update()
        clock.tick(FPS)

# SNAKE
def start_snake():
    cell_size = 25
    snake = [(10, 10)]
    direction = (1, 0)
    food = (random.randint(0, (MENU_WIDTH//cell_size)-1), random.randint(0, (MENU_HEIGHT//cell_size)-1))
    score = 0

    while True:
        menu_screen.fill(COLORS["background"])
        
        # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_UP and direction != (0,1):
                    direction = (0,-1)
                if event.key == pygame.K_DOWN and direction != (0,-1):
                    direction = (0,1)
                if event.key == pygame.K_LEFT and direction != (1,0):
                    direction = (-1,0)
                if event.key == pygame.K_RIGHT and direction != (-1,0):
                    direction = (1,0)
        
        # Movimento e collisioni
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (head[0] < 0 or head[0] >= MENU_WIDTH//cell_size or
            head[1] < 0 or head[1] >= MENU_HEIGHT//cell_size or
            head in snake) and not hacks["immortality"]:
            game_over_screen(score)
            return
        
        snake.insert(0, head)
        if head == food:
            score += 1
            food = (random.randint(0, (MENU_WIDTH//cell_size)-1), random.randint(0, (MENU_HEIGHT//cell_size)-1))
        else:
            snake.pop()

        # Disegno
        for i, segment in enumerate(snake):
            color = COLORS["neon_pink"] if i ==0 else COLORS["neon_blue"]
            pygame.draw.rect(menu_screen, color,
                           (segment[0]*cell_size, segment[1]*cell_size, cell_size-2, cell_size-2))
        pygame.draw.rect(menu_screen, (255,0,0),
                       (food[0]*cell_size, food[1]*cell_size, cell_size, cell_size))
        
        pygame.display.update()
        clock.tick(10)

# PAC-MAN
def start_pacman():
    pacman_screen = pygame.display.set_mode((PACMAN_WIDTH, PACMAN_HEIGHT))
    pygame.display.set_caption("MAX GAMES - Pac-Man")
    
    # Configurazioni Pac-Man
    pacman_size = 20
    pacman_pos = [PACMAN_WIDTH//2, PACMAN_HEIGHT//2]
    pacman_speed = 5
    direction = [0, 0]
    
    # Fantasmi
    ghosts = [
        {"pos": [100, 100], "color": COLORS["red"], "speed": 3},
        {"pos": [500, 100], "color": COLORS["pink"], "speed": 2},
        {"pos": [100, 500], "color": COLORS["cyan"], "speed": 4},
        {"pos": [500, 500], "color": COLORS["orange"], "speed": 3}
    ]
    
    while True:
        pacman_screen.fill(COLORS["background"])
        
        # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    return
                if event.key == pygame.K_UP:
                    direction = [0, -pacman_speed]
                if event.key == pygame.K_DOWN:
                    direction = [0, pacman_speed]
                if event.key == pygame.K_LEFT:
                    direction = [-pacman_speed, 0]
                if event.key == pygame.K_RIGHT:
                    direction = [pacman_speed, 0]
        
        # Movimento Pac-Man
        pacman_pos[0] += direction[0]
        pacman_pos[1] += direction[1]
        
        # Controllo bordi
        if pacman_pos[0] < 0:
            pacman_pos[0] = PACMAN_WIDTH
        if pacman_pos[0] > PACMAN_WIDTH:
            pacman_pos[0] = 0
        if pacman_pos[1] < 0:
            pacman_pos[1] = PACMAN_HEIGHT
        if pacman_pos[1] > PACMAN_HEIGHT:
            pacman_pos[1] = 0
        
        # Disegno Pac-Man
        pygame.draw.circle(pacman_screen, COLORS["yellow"], pacman_pos, pacman_size)
        
        # Disegno fantasmi
        for ghost in ghosts:
            pygame.draw.circle(pacman_screen, ghost["color"], ghost["pos"], pacman_size)
            # Movimento fantasmi
            ghost["pos"][0] += ghost["speed"]
            if ghost["pos"][0] < 0 or ghost["pos"][0] > PACMAN_WIDTH:
                ghost["speed"] *= -1
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    show_start_animation()
    main_menu()