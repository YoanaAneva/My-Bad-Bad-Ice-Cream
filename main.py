import pygame

from enemy import Enemy
from board_maps import level1_stage1, level1_stage2, level2_stage1, level2_stage2, level3_stage1, level3_stage2 
from level import Level
from single_player_game import SinglePlayerGame
from multi_player_game import MultiPlayerGame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()
enemy = Enemy(666, 92, 2); enemies = pygame.sprite.Group(); enemies.add(enemy)
enemy_for_level2 = Enemy(666, 180, 2); enemies2 = pygame.sprite.Group(); enemies2.add(enemy_for_level2)
enemy_for_level3 = Enemy(666, 48, 2); enemies3 = pygame.sprite.Group(); enemies3.add(enemy_for_level3)
level1 = Level([level1_stage1, level1_stage2], ["banana", "watermelon"], enemies, (94, 92))
level2 = Level([level2_stage1, level2_stage2], ["ice-cream", "banana"], enemies2, (314, 92))
level3 = Level([level3_stage1, level3_stage2], ["watermelon", "ice-cream"], enemies3, (50, 48))
# game = MultiPlayerGame([level1, level2, level3], screen)
game = SinglePlayerGame([level1, level2, level3], screen)
game.main()

pygame.quit()