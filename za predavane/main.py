import random
import pygame
from enemy import Enemy
from board_maps import level1_stage1, level1_stage2, level2_stage1, level2_stage2, level3_stage1, level3_stage2 
from level import Level
from single_player_game import SinglePlayerGame
from multi_player_game import MultiPlayerGame
from displays import Display
import json

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()
enemy1_for_level1 = Enemy(666, 488, 2)
enemy2_for_level1 = Enemy(226, 400, 2)
enemies1 = pygame.sprite.Group(); 
enemies1.add(enemy1_for_level1)
enemies1.add(enemy2_for_level1)

enemy1_for_level2 = Enemy(94, 224, 2)
enemy2_for_level2 = Enemy(138, 488, 2)
enemy3_for_level2 = Enemy(666, 400, 2)
enemies2 = pygame.sprite.Group()
enemies2.add(enemy1_for_level2)
enemies2.add(enemy2_for_level2)
enemies2.add(enemy3_for_level2)

enemy_name = random.choice(["Blinki", "Pinki"])
enemy1_for_level3 = Enemy(710, 532, 2, enemy_name)
enemy2_for_level3 = Enemy(710, 532, 2, enemy_name)
enemies3 = pygame.sprite.Group()
enemies3.add(enemy1_for_level3)
enemies3.add(enemy2_for_level3)

level1 = Level([level1_stage1, level1_stage2], ["banana", "watermelon"], enemies1, (94, 92))
level2 = Level([level2_stage1, level2_stage2], ["ice-cream", "banana"], enemies2, (314, 92))
level3 = Level([level3_stage1, level3_stage2], ["watermelon", "ice-cream"], enemies3, (50, 48))

display = Display(screen)

game_type = None
game = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    try:
        choice = display.display_starting_screen()
    # the window has been closed
    except RuntimeError:
        break
    if choice == "start":
        try:
            game_type = display.display_game_mode_choice()
        except RuntimeError:
            break
    else:
        try:
            choice = display.display_scores()
        except RuntimeError:
            break
        if choice == "back to menu":
            continue
    if game_type == "multi-player":
        game = MultiPlayerGame([level1, level2, level3], screen)
    else:
        game = SinglePlayerGame([level1, level2, level3], screen)
    try:
        flavour = display.display_player_choice()
        game.main(flavour)
    except RuntimeError:
        break

pygame.quit()