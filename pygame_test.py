import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface([20, 20])
        self.surf = pygame.image.load(os.path.join("assets", "player1.png"))
        # self.surf.set_colorkey("black")
        # self.surf.fill("orange")
        self.rect = self.surf.get_rect()
    
    def move(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join("assets", "enemy1.png"))
        # self.surf.set_colorkey("black")
        self.rect = self.surf.get_rect(
            center = (random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20))
        )
        self.speed = random.randint(5, 20)
    
    def move(self):
        self.rect.move_ip(5, 0)
        
        if self.rect.left < 0:
            self.rect.move_ip(100, 0)
        
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.move_ip(20, -100)

        if self.rect.right > SCREEN_WIDTH:
            self.rect.move_ip(-100, 5)
        
        if self.rect.top < 0:
            self.rect.move_ip(0, 100)


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
bg = pygame.image.load(os.path.join("assets", "background.png"))

player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

        if isinstance(sprite, Enemy):
            sprite.move()
        else:
            sprite.move(pressed_keys)

    pygame.sprite.spritecollide(player, enemies, True)

    pygame.display.flip()

    screen.blit(bg, (0, 0))
    # screen.fill((0, 0, 0))

    clock = pygame.time.Clock()
    clock.tick(60)

pygame.quit()