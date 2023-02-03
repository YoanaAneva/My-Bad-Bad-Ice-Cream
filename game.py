import pygame
import os
from player import Player
from enemy import Enemy
from ice_cube import IceCube
from fruit import Fruit
from board_maps import level1_stage1, level1_stage2, level2_stage1, level3_stage1 
from level import Level

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624
FRAME_DIMENSIONS = (50, 48)

EMPTY_CELL = 0
ICE_NUM = 1
FROZEN_FRUIT_NUM = 2
FRUIT_NUM = 3
IGLOO_NUM = 4
OFFSET = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player(50, 488, "chocolate")
enemy1 = Enemy(226, 318, 5, 4, "Blinki")
enemy2 = Enemy(666, 180, 5, 4, "Pinki")
# enemy3 = Enemy(138, 488, 5, 3)
enemies = pygame.sprite.Group()
# enemies.add(enemy1)
enemies.add(enemy2)
# enemies.add(enemy3)


level1 = Level([level1_stage1, level1_stage2], ["banana", "watermelon"], enemies)
level1.draw_background(screen)

other_player = None

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
        player.change_board(level1.board, level1.fruit, enemies, screen)

    if not player.is_dead:
        player.move(pressed_keys, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT), level1.board)
    # for enemy in enemies:
    #     enemy.move_squares(level1.board, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # enemy1.chase(player, level1.board)
    enemy2.chase(player, level1.board)
    # enemy2.move_squares(level1.board, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # enemy1.move2(player, level1.board)

    pygame.display.flip()
    
    level1.draw_background(screen)
    level1.draw_board(screen, player.score)

    eaten_sprites = pygame.sprite.spritecollide(player, level1.fruit, False)
    if eaten_sprites != []:
        for sprite in eaten_sprites:
            if isinstance(sprite, Fruit) and not sprite.is_frozen:
                level1.board[sprite.get_map_coordinates()[0]][sprite.get_map_coordinates()[1]] = 0
                sprite.kill()
                player.score += 5
    

    if pygame.sprite.spritecollideany(player, enemies):
        player.die()

    level1.update_stage()

    clock = pygame.time.Clock()
    clock.tick(30)
        
pygame.quit()



