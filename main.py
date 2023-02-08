import pygame
from random import choice

from player import Player
from enemy import Enemy
from fruit import Fruit
from board_maps import level1_stage1, level1_stage2, level2_stage1, level3_stage1 
from level import Level
from client import Client
from exchange_info import ExchangeInfo, PlayerInitInfo

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

is_multiplayer = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

enemy1 = Enemy(666, 588, 3)
enemy2 = Enemy(94, 92, 3)
enemies = pygame.sprite.Group()
enemies.add(enemy1)
# enemies.add(enemy2)

level1 = Level([level1_stage1, level1_stage2], ["banana", "watermelon"], enemies)
level1.draw_background(screen)

flavour = choice(["chocolate", "pink", "vanilla"])
player = Player(94, 92, flavour)

if is_multiplayer:
    client = Client()
    player_init_info = PlayerInitInfo(94, 92, flavour)

    client.connect_to_server(player_init_info)

    other_init_info = client.get_init_info()
    other_player = Player(other_init_info.player_x, other_init_info.player_y, other_init_info.player_flavour)

client_info = None
running = True
while running:
    if is_multiplayer:
        client_info = ExchangeInfo(player.direction, player.rect, player.score, player.is_dead)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_multiplayer:
                    player.change_board(level1.board, level1.fruit, enemies, screen, other_player.get_curr_board_cell())
                    client_info = ExchangeInfo(player.direction, player.rect, player.score, player.is_dead, level1.board)
                else:
                    player.change_board(level1.board, level1.fruit, enemies, screen)

    pressed_keys = pygame.key.get_pressed()
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    
    eaten_sprites = pygame.sprite.spritecollide(player, level1.fruit, False)
    if eaten_sprites != []:
        for sprite in eaten_sprites:
            if isinstance(sprite, Fruit) and not sprite.is_frozen:
                level1.board[sprite.get_map_coordinates()[0]][sprite.get_map_coordinates()[1]] = 0
                sprite.kill()
                player.score += 5
        if is_multiplayer:
            client_info = ExchangeInfo(player.direction, player.rect, player.score, player.is_dead, level1.board)

    if is_multiplayer:
        other_client_info = client.send(client_info)
        other_player.direction = other_client_info.player_direction
        other_player.rect = other_client_info.player_rect
        other_player.score = other_client_info.player_score
        other_player.is_dead = other_client_info.has_died
        if other_client_info.board:
            level1.board = other_client_info.board

        if other_player.is_dead:
            other_player.die()
        other_player.draw(screen)

    if not player.is_dead:
        player.move(pressed_keys, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT), level1.board)

    for enemy in enemies:
        enemy.move(player, level1.board, FRAME_DIMENSIONS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.flip()
    
    level1.draw_background(screen)
    if is_multiplayer:
        level1.draw_board(screen, player.score, other_player.score)
    else:
        level1.draw_board(screen, player.score)

    if pygame.sprite.spritecollideany(player, enemies):
        player.die()

    print(level1.stage)
    level1.update_stage()

    clock = pygame.time.Clock()
    clock.tick(60)
 
pygame.quit()



