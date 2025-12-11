import time
import os
from typing import List
import pygame
from game import Game
from player import Player
from fruit import Fruit
from level import Level
from displays import Display

PLAYER_SPEED = 3

class SinglePlayerGame(Game):
    def __init__(self, levels: List[Level], screen: List[List[int]]):
        super().__init__(levels, screen)

    def main(self, player_flavour: str) -> None:
        """ Perform the main loop of the game including drawing,
        movement, collision detection, etc.
        """
        choice = None
        global_score = 0  
        display = Display(self.screen)
        while choice != "back to menu":
            try:
                level = display.display_level_choice(self.levels)
            # the window has been closed
            except RuntimeError as e:
                raise e

            self.current_level = level - 1
            curr_level = self.levels[self.current_level]

            self.player = Player(curr_level.player_init_pos[0], curr_level.player_init_pos[1], player_flavour, PLAYER_SPEED)
            start_time = time.time()
            score_for_this_level = 0
            is_melted = False

            while True:
                curr_level.draw_board(self.screen, start_time, self.player.points)

                self.player.draw(self.screen)
                for enemy in curr_level.enemies:
                    enemy.draw(self.screen)

                if is_melted:
                    display.display_melted_info()
                    is_melted = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise RuntimeError("closed window")
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.change_board(curr_level.board, curr_level.fruit,
                                                        curr_level.enemies)
                
                pressed_keys = pygame.key.get_pressed()

                eaten_sprites = pygame.sprite.spritecollide(self.player, curr_level.fruit, False)
                if eaten_sprites != []:
                    for sprite in eaten_sprites:
                        if isinstance(sprite, Fruit) and not sprite.is_frozen:
                            fruit_coords = sprite.get_map_coordinates()
                            curr_level.board[fruit_coords[0]][fruit_coords[1]] = 0  
                            sprite.kill()
                            self.player.points += 5
                
                if not self.player.is_dead:
                    self.player.move(pressed_keys, curr_level.board)
                for enemy in curr_level.enemies:
                    if not enemy.is_dead:
                        enemy.move(self.player, curr_level.board)

                if pygame.sprite.spritecollideany(self.player, curr_level.enemies):
                    if not curr_level.is_over:
                        curr_level.is_over = True
                        self.player.die()

                if curr_level.is_over:
                    has_won = None
                    if start_time != -1:
                        score_for_this_level = self.calculate_player_score_for_level(start_time, self.player.points)
                        global_score += score_for_this_level
                        start_time = -1
                    if not self.player.is_dead:
                        if self.current_level < len(self.levels) - 1 and self.levels[self.current_level + 1].is_locked:
                            self.levels[self.current_level + 1].is_locked = False
                    else:
                        has_won = "No"
                    try:
                        choice = display.display_level_complete(score_for_this_level, global_score, False, has_won)
                        if choice:
                            curr_level.reset()
                            break
                    #the window has been closed
                    except RuntimeError as e:
                        raise e

                pygame.display.flip()
                self.screen.blit(self.background, (0, 0))
                curr_level.update_stage()

                if self.current_level == 1:
                    if not curr_level.is_over:
                        if self.melt(start_time, curr_level.board):
                            curr_level.is_over = True
                            is_melted = True

                self.clock.tick(60)

            if choice == "back to menu":
                fp = os.path.join("assets", "scores.txt")
                if self.is_in_top_10_scores(global_score, fp):
                    player_name = display.display_name_input_screen(global_score)
                    self.write_in_scores(player_name, global_score, fp)
            
