import pygame

from enemy import Enemy
from board_maps import level1_stage1, level1_stage2, level2_stage1, level3_stage1 
from level import Level
from single_player_game import SinglePlayerGame
from multi_player_game import MultiPlayerGame

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

pygame.init()
enemy = Enemy(666, 588, 3); enemies = pygame.sprite.Group(); enemies.add(enemy)
enemy_for_level2 = Enemy(666, 180, 3); enemies2 = pygame.sprite.Group(); enemies2.add(enemy_for_level2)
level1 = Level([level1_stage1, level1_stage2], ["banana", "watermelon"], enemies, (94, 92))
level2 = Level([level2_stage1], ["ice-cream"], enemies2, (314, 92))
level3 = Level([level3_stage1], ["watermelon"], enemies2, (94, 92))
game = MultiPlayerGame([level1, level2, level3], screen)
# game = SinglePlayerGame([level1, level2, level3], screen)
game.main()

pygame.quit()