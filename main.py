import math
import time
import pygame

# Pygame init
pygame.init()
screen_w = 720
screen_h = 720
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 20)
running = True


# Game variables
DEAD_CELL = 0
ALIVE_CELL = 1
board_size = 50
board = [[DEAD_CELL for _ in range(board_size)] for _ in range(board_size)]
tile_size = math.floor(math.sqrt((screen_w * screen_h) / math.pow(board_size, 2)))
print(tile_size)
walked_over = [[0 for _ in range(board_size)] for _ in range(board_size)]
generation = 0

species = {
    # Still Lifes (static patterns)
    "block": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "beehive": [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)],
    "loaf": [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (3, 2), (2, 3)],
    
    # Oscillators (patterns that repeat)
    "blinker": [(1, 0), (1, 1), (1, 2)], # Period 2
    "toad": [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)], # Period 2
    "beacon": [(0,0), (1,0), (0,1), (3,2), (2,3), (3,3)], # Period 2

    # Spaceships (patterns that move)
    "glider": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    
    "square": [(1, 1), (1, 2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)], 
}


def draw_species(board, species_name, x, y):
    for sx, sy in species[species_name]:
        # Check for species spawned outside of board
        if sx + x >= board_size or sy + y >= board_size: 
            return
        board[y + sy][x + sx] = ALIVE_CELL


def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            color = "black" if cell else "white"
            tile_x = (tile_size) * x
            tile_y = (tile_size) * y
            tile = pygame.Rect(tile_x, tile_y, tile_size, tile_size)
            pygame.draw.rect(screen, color, tile)


def draw_game():
    global board
    # Draw the board first...maybe wait 3 seconds?
    draw_board(board)
    board = next_generation(board)


def draw_scene(name="default"):
    if name == "default":
        draw_species(board, "glider", 2, 2)
        draw_species(board, "blinker", 15, 5)
        draw_species(board, "toad", 25, 8)
        draw_species(board, "beacon", 35, 12)
        draw_species(board, "loaf", 10, 20)
        draw_species(board, "beehive", 25, 30)
        draw_species(board, "block", 40, 40)



def next_generation(current_board):
    global generation
    generation += 1
    new_board = [[cell for cell in row] for row in current_board]

    for y, row in enumerate(current_board):
        for x, cell in enumerate(row):
            alive = cell
            neighbors = get_neighbors(current_board, x, y)
            
            # Rules

            # 1. If live cell has < 2 live neighbors: dead
            if alive and neighbors < 2:
                new_board[y][x] = DEAD_CELL

            # 2. If live cell has 2 or 3 live neighbors: continue


            # 3. If live cell has > 3 live neighbors: dead
            if alive and neighbors > 3:
                new_board[y][x] = DEAD_CELL

            # 4. If dead cell has = 3 live neighbors: alive
            if not alive and neighbors == 3: 
                new_board[y][x] = ALIVE_CELL

    return new_board


def get_neighbors(board, x, y) -> int:
    '''Returns live neighbors of pos x, y'''
    alive_count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # Skip self
            if dx == 0 and dy == 0: 
                continue
            nx = (x + dx) % board_size
            ny = (y + dy) % board_size
            neighbor = board[ny][nx]
            if neighbor:
                alive_count += 1
    return alive_count


def game_loop():
    global running
    global board

    draw_scene()

    paused = False
    while running:
        # Check if the game is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            paused = not paused


        # Set color
        screen.fill("white")

        # Render game
        if not paused:
            draw_game()
        else:
            draw_board(board)


        # Render debug info
        debug_text = font.render('Paused' if paused else 'Paused', False, (0, 0, 0))
        gen_text = font.render('Generation ' + str(generation), False, (0, 0, 0))
        screen.blit(debug_text, (10,10))
        screen.blit(gen_text, (100,10))

        # Update screen
        pygame.display.flip()
            
        clock.tick(20) # limit fps to 60


if __name__ == "__main__":
    game_loop()
    pygame.quit()