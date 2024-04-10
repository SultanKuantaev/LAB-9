import pygame, sys, random, time
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE, RED, GREEN, BLACK, WHITE = (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0), (255, 255, 255)

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0  

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background
background = pygame.image.load(r"c:\Users\HUAWEI\Downloads\AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"c:\Users\HUAWEI\Pictures\Screenshots\Снимок экрана 2024-04-03 203447.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"c:\Users\HUAWEI\Downloads\Pygame_rects.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):  
    def __init__(self, weight=1):
        super().__init__()
        self.weight = weight
        # Choose the image based on the coin's weight
        if self.weight == 1:
            image_path = r"c:\Users\HUAWEI\Pictures\Снимок экрана 2024-04-06 233601.png"  # Path for the first coin image
            
        else:
            image_path = r"c:\Users\HUAWEI\Pictures\Снимок экрана 2024-04-06 233526.png"  # Path for the second coin image
        self.image = pygame.image.load(image_path)  
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.kill()

# Initialize player and enemy
P1 = Player()
E1 = Enemy()

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)  # Add player and enemy to all_sprites group

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED and COINS_COLLECTED >= 15:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    coins_collected_text = font_small.render(str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_collected_text, (SCREEN_WIDTH - 100, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    coin_hit_list = pygame.sprite.spritecollide(P1, coins, True)
    for coin in coin_hit_list:
        COINS_COLLECTED += coin.weight

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if random.randint(1, 100) > 98:
        # Adjust coin spawning to randomly choose a weight
        new_coin_weight = 3 if random.randint(1, 2) == 1 else 1  # 50% chance for each weight
        new_coin = Coin(new_coin_weight)
        coins.add(new_coin)
        all_sprites.add(new_coin)

    pygame.display.update()
    FramePerSec.tick(FPS)
