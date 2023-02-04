import pygame
import os
from player import Player
from enemy import Enemy
from ice_cube import IceCube
from fruit import Fruit
from board_maps import level1_stage1, level1_stage2, level2_stage1, level3_stage1 
from level import Level
from client import Client
from exchange_info import ExchangeInfo, PlayerInitInfo, Info
from random import choice

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

enemy1 = Enemy(94, 92, 5, 4,)
enemy2 = Enemy(710, 92, 5, 4)
enemies = pygame.sprite.Group()
# enemies.add(enemy1)
# enemies.add(enemy2)

level1 = Level([level1_stage1, level1_stage2], ["banana", "watermelon"], enemies)
level1.draw_background(screen)

# client = Client()
# client.connect()
# player = Player(314, 400, "pink")
# init_info_for_player = PlayerInitInfo(314, 400, "pink")
# other_init_info = client.send(init_info_for_player)
# other_player = Player(other_init_info.player_x, other_init_info.player_y, other_init_info.player_flavour)

# flavour = choice(["chocolate", "pink", "vanilla"])
# player = Player(94, 92, flavour)
# player_init_info = PlayerInitInfo(94, 92, flavour)

# client.connect_to_server(player_init_info)

# other_init_info = client.get_init_info()
# other_player = Player(other_init_info.player_x, other_init_info.player_y, other_init_info.player_flavour)
# print(other_player)
player = Player(94, 92, "vanilla")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    # player_info = ExchangeInfo(player.direction, player.rect, level1.board)
    # other_client_info = client.send(player_info)

    # other_player.direction = other_client_info.player_direction
    # other_player.rect = other_client_info.player_rect
    # level1.board = other_client_info.board
    # other_player.draw(screen)

    if pressed_keys[pygame.K_SPACE]:
        player.change_board(level1.board, level1.fruit, enemies, screen)

    if not player.is_dead:
        player.move(pressed_keys, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT), level1.board)

    for enemy in enemies:
        enemy.move(player, level1.board, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT))

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



