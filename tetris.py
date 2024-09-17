import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30  # Size of the grid block
PLAY_WIDTH = 10 * BLOCK_SIZE  # 10 blocks wide
PLAY_HEIGHT = 20 * BLOCK_SIZE  # 20 blocks high

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

# Define colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0),    # Red
]

# Define the shapes
SHAPES = [
    [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '...O.',
      '.....']],
    [['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '.O...',
      '.....']],
    [['.....',
      '...O.',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..OO.',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '.O...',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....']],
    [['.....',
      '.O...',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..OO.',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '...O.',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....']],
    [['.....',
      '..O..',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '.OOOO',
      '.....',
      '.....'],
     ['..O..',
      '..O..',
      '..O..',
      '..O..',
      '.....']]
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    shape = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == BLACK] for y in range(20)]
    accepted_positions = [x for sub in accepted_positions for x in sub]

    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('Calibri', size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, (WIDTH / 2 - label.get_width() / 2, HEIGHT / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (PLAY_WIDTH, y * BLOCK_SIZE))
        for x in range(len(grid[y])):
            pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, PLAY_HEIGHT))

def clear_rows(grid, locked):
    cleared = 0
    for y in range(len(grid)-1, -1, -1):
        row = grid[y]
        if BLACK not in row:
            cleared += 1
            del_row = y
            for x in range(len(row)):
                try:
                    del locked[(x, y)]
                except:
                    continue

    if cleared > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < del_row:
                new_key = (x, y + cleared)
                locked[new_key] = locked.pop(key)
    return cleared

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Calibri', 24)
    label = font.render('Next Shape:', True, (255, 255, 255))

    start_x = PLAY_WIDTH + 10
    start_y = 60
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                pygame.draw.rect(surface, shape.color, (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (start_x, 30))

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0

    font = pygame.font.SysFont('Calibri', 24)
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # Increase speed every 60 seconds
        if level_time / 1000 > 60:
            level_time = 0
            if fall_speed > 0.1:
                fall_speed -= 0.005

        # Piece falls
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        # Add piece to the grid
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color

        # Piece hit the ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(screen, grid, score)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        # Check if game is over
        if check_lost(locked_positions):
            draw_text_middle("GAME OVER", 40, (255, 255, 255), screen)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)
    # Tetris Title
    font = pygame.font.SysFont('Calibri', 60)
    label = font.render('Tetris', True, (255, 255, 255))
    surface.blit(label, (WIDTH / 2 - label.get_width() / 2, 30))

    # Current Score
    font = pygame.font.SysFont('Calibri', 24)
    label = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(label, (PLAY_WIDTH + 10, 200))

    # Draw grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Grid lines
    draw_grid(surface, grid)

def main_menu():
    run = True
    while run:
        screen.fill(BLACK)
        draw_text_middle('Press Any Key To Play', 30, (255, 255, 255), screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main_menu()
