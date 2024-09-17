import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 100)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

BRICK_COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

# Game settings
FPS = 60
PADDLE_SPEED = 7
BALL_SPEED = 5
LIVES = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Clock to control frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.width) // 2
        self.rect.y = SCREEN_HEIGHT - self.height - 10
        self.speed = PADDLE_SPEED

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 10
        self.image = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
        self.speed_y = -BALL_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wall collision (left/right)
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x

        # Ceiling collision
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
        self.speed_y = -BALL_SPEED

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color, points):
        super().__init__()
        self.width = 75
        self.height = 30
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points

# Function to create a grid of bricks
def create_bricks(rows, cols):
    bricks = pygame.sprite.Group()
    brick_width = 75
    brick_height = 30
    padding = 5
    offset_x = (SCREEN_WIDTH - (cols * (brick_width + padding))) // 2
    offset_y = 60

    for row in range(rows):
        for col in range(cols):
            x = offset_x + col * (brick_width + padding)
            y = offset_y + row * (brick_height + padding)
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            brick = Brick(x, y, color, points=(rows - row) * 10)
            bricks.add(brick)
    return bricks

# Main game function
def main():
    # Game variables
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks(6, 10)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    all_sprites.add(bricks)
    lives = LIVES
    score = 0
    running = True

    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left()
        if keys[pygame.K_RIGHT]:
            paddle.move_right()

        # Update ball
        ball.update()

        # Ball and paddle collision
        if ball.rect.colliderect(paddle.rect):
            ball.speed_y = -ball.speed_y
            # Adjust ball direction based on where it hits the paddle
            offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.width / 2)
            ball.speed_x = BALL_SPEED * offset

        # Ball and bricks collision
        brick_collision_list = pygame.sprite.spritecollide(ball, bricks, True)
        for brick in brick_collision_list:
            ball.speed_y = -ball.speed_y
            score += brick.points

        # Ball falls below the paddle
        if ball.rect.top > SCREEN_HEIGHT:
            lives -= 1
            if lives > 0:
                ball.reset()
            else:
                # Game over
                game_over_screen(score)
                running = False

        # Win condition
        if len(bricks) == 0:
            # Next level or win
            win_screen(score)
            running = False

        # Drawing
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 20))

        pygame.display.flip()

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        restart_text = font.render("Press ENTER to Restart or ESC to Quit", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def win_screen(score):
    while True:
        screen.fill(BLACK)
        win_text = font.render("YOU WIN!", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        restart_text = font.render("Press ENTER to Play Again or ESC to Quit", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
