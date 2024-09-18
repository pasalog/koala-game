import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(self.screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece.color,
                                     ((piece.x + x + offset_x) * BLOCK_SIZE,
                                      (piece.y + y + offset_y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)

    def draw_next_piece(self):
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece.color,
                                     ((GRID_WIDTH + 1 + x) * BLOCK_SIZE,
                                      (1 + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)

    def check_collision(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (piece.x + x + offset_x < 0 or
                        piece.x + x + offset_x >= GRID_WIDTH or
                        piece.y + y + offset_y >= GRID_HEIGHT or
                        self.grid[piece.y + y + offset_y][piece.x + x + offset_x] != BLACK):
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color

    def remove_full_rows(self):
        full_rows = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        self.score += len(full_rows) ** 2 * 100

    def game_over(self):
        return any(cell != BLACK for cell in self.grid[0])

    def run(self):
        fall_time = 0
        fall_speed = 0.5
        running = True

        while running:
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision(self.current_piece, offset_x=-1):
                            self.current_piece.x -= 1
                    if event.key == pygame.K_RIGHT:
                        if not self.check_collision(self.current_piece, offset_x=1):
                            self.current_piece.x += 1
                    if event.key == pygame.K_DOWN:
                        if not self.check_collision(self.current_piece, offset_y=1):
                            self.current_piece.y += 1
                    if event.key == pygame.K_UP:
                        rotated = Tetromino()
                        rotated.shape = list(zip(*self.current_piece.shape[::-1]))
                        rotated.x, rotated.y = self.current_piece.x, self.current_piece.y
                        if not self.check_collision(rotated):
                            self.current_piece = rotated

            if fall_time / 1000 > fall_speed:
                if not self.check_collision(self.current_piece, offset_y=1):
                    self.current_piece.y += 1
                else:
                    self.merge_piece()
                    self.remove_full_rows()
                    self.current_piece = self.next_piece
                    self.next_piece = Tetromino()
                    if self.game_over():
                        running = False
                fall_time = 0

            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_next_piece()

            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 200))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()