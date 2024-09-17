import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Squirrel Finder")

# Clock to control frame rate
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font for text
font = pygame.font.SysFont('Arial', 20)

# Load images and scale them to 40x40 pixels
koala_img = pygame.image.load('koala.png')
koala_img = pygame.transform.scale(koala_img, (40, 40))
strawberry_img = pygame.image.load('strawberry.png')
strawberry_img = pygame.transform.scale(strawberry_img, (40, 40))
squirrel_img = pygame.image.load('squirrel.png')
squirrel_img = pygame.transform.scale(squirrel_img, (40, 40))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = koala_img
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 7

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep player on the screen
        self.rect.clamp_ip(screen.get_rect())

# Strawberry class
class Strawberry(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = strawberry_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 40)
        self.rect.y = random.randint(0, screen_height - 40)
        self.vx = random.choice([-4, -3, -2, 2, 3, 4])
        self.vy = random.choice([-4, -3, -2, 2, 3, 4])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.vx = -self.vx
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.vy = -self.vy

# Squirrel class
class Squirrel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = squirrel_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 40)
        self.rect.y = random.randint(0, screen_height - 40)
        self.vx = random.choice([-5, -4, -3, 3, 4, 5])
        self.vy = random.choice([-5, -4, -3, 3, 4, 5])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.vx = -self.vx
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.vy = -self.vy

# Function to display instructions
def show_instructions():
    screen.fill(BLACK)
    instructions = [
        "Squirrel Finder",
        "",
        "Instructions:",
        "- You are the koala.",
        "- Use the arrow keys to move.",
        "- Avoid the strawberries.",
        "- Touch the squirrel to win.",
        "- Strawberries spawn every second.",
        "- Squirrel spawns after 3 seconds.",
        "- Game will restart automatically.",
        "",
        "Press any key to start."
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 30 + i * 30))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Function to display game over screen
def show_game_over(message):
    screen.fill(BLACK)
    text = font.render(message, True, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 20))
    subtext = font.render("Restarting...", True, WHITE)
    screen.blit(subtext, (screen_width // 2 - subtext.get_width() // 2, screen_height // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(2000)

# Main game loop
def main():
    player = Player()
    player_group = pygame.sprite.Group(player)
    strawberry_group = pygame.sprite.Group()
    squirrel_group = pygame.sprite.Group()

    while True:
        show_instructions()

        # Game variables
        start_ticks = pygame.time.get_ticks()
        strawberry_timer = pygame.time.get_ticks()
        squirrel_spawned = False
        running = True

        # Reset player position
        player.rect.center = (screen_width // 2, screen_height // 2)

        # Clear groups
        strawberry_group.empty()
        squirrel_group.empty()

        while running:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys_pressed = pygame.key.get_pressed()
            player.update(keys_pressed)

            # Spawn strawberry every second
            if pygame.time.get_ticks() - strawberry_timer > 1000:
                strawberry = Strawberry()
                strawberry_group.add(strawberry)
                strawberry_timer = pygame.time.get_ticks()

            # Spawn squirrel after 3 seconds
            if not squirrel_spawned and pygame.time.get_ticks() - start_ticks > 3000:
                squirrel = Squirrel()
                squirrel_group.add(squirrel)
                squirrel_spawned = True

            # Update sprites
            strawberry_group.update()
            squirrel_group.update()

            # Collision detection
            if pygame.sprite.spritecollideany(player, strawberry_group):
                show_game_over("You Died!")
                running = False
                break

            if pygame.sprite.spritecollideany(player, squirrel_group):
                show_game_over("You Win!")
                running = False
                break

            # Drawing
            screen.fill(BLACK)
            player_group.draw(screen)
            strawberry_group.draw(screen)
            squirrel_group.draw(screen)

            # Draw "openai" text
            openai_text = font.render("openai", True, WHITE)
            screen.blit(openai_text, (10, screen_height - 30))

            # Draw timer
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            timer_text = font.render(f"Time: {elapsed_time:.1f}", True, WHITE)
            screen.blit(timer_text, (screen_width - 120, 10))

            pygame.display.flip()

if __name__ == "__main__":
    main()
