import pygame
import os
from player import Player
from enemy import Enemy
from ice_cube import IceCube
from fruit import Fruit
from board_maps import level1_stage1, level2_stage1

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624
FRAME_DIMENSIONS = (50, 48)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load(os.path.join("assets", "background.png")).convert()

player = Player(314, 92)
enemy1 = Enemy(94, 136, 5, 3)
enemy2 = Enemy(666, 180, 5, 3)
enemy3 = Enemy(138, 488, 5, 3)
fruits = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
ice_cubes = pygame.sprite.Group()
board = level1_stage1

def add_fruit(fruit_type):
    top_x = 50
    top_y = 48

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 3:
                fruit = Fruit(fruit_type, j * 44 + top_x, i * 44 + top_y)
                fruits.add(fruit)


def draw_board(board):
    top_x = 50
    top_y = 48

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                ice_cube = IceCube()
                ice_cube.draw(screen, j * 44 + top_x, i * 44 + top_y)

    for fruit in fruits:
        fruit.draw(screen)

    font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), 30)
    pygame.draw.rect(screen, "#d7e5f0", pygame.Rect(40, 5, 200, 40))
    score = font.render(f"Score: {player.score}", True, "#1c2e4a")
    screen.blit(score, (55, 7))

add_fruit("banana")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    if pressed_keys[pygame.K_SPACE]:
        player.change_board(board, fruits, enemies)

    if not player.is_dead:
        player.move(pressed_keys, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT), board)
    for enemy in enemies:
        enemy.move_squares(board, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.flip()
    
    screen.blit(bg, (0, 0))

    draw_board(board)

    eaten_sprites = pygame.sprite.spritecollide(player, fruits, False)
    if eaten_sprites != []:
        for sprite in eaten_sprites:
            if isinstance(sprite, Fruit) and not sprite.is_frozen:
                board[sprite.get_map_coordinates()[0]][sprite.get_map_coordinates()[1]] = 0
                sprite.kill()
                player.score += 5
    
    
    if pygame.sprite.spritecollideany(player, enemies):
        player.die()

    clock = pygame.time.Clock()
    clock.tick(30)
        
pygame.quit()
