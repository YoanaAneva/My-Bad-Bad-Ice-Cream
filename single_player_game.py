import os
import time
import copy
import pygame
from game import Game
from player import Player
from fruit import Fruit

PLAYER_SPEED = 3

class SinglePlayerGame(Game):
    def __init__(self, levels, screen):
        super().__init__(levels, screen)

    def main(self, player_flavour):
        choice = None
        while choice != "back to menu":
            try:
                level = self.display_level_choice()
            # the window has been closed
            except RuntimeError as e:
                raise e

            self.current_level = level - 1
            curr_level = self.levels[self.current_level]

            self.player = Player(curr_level.player_init_pos[0], curr_level.player_init_pos[1], player_flavour, PLAYER_SPEED)
            start_time = time.time()
            # prev_frame_time = time.time()
            while True:
                # now = time.time()
                # dt = now - prev_frame_time
                # prev_frame_time = now

                curr_level.draw_board(self.screen, start_time, self.player.score)

                self.player.draw(self.screen)
                for enemy in curr_level.enemies:
                    enemy.draw(self.screen)

                # now = time.time()
                # dt = now - prev_frame_time
                # prev_frame_time = now
                # print("2", dt)

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
                            self.player.score += 5
                
                if not self.player.is_dead:
                    self.player.move(pressed_keys, curr_level.board)
                for enemy in curr_level.enemies:
                    enemy.move(self.player, curr_level.board)

                if pygame.sprite.spritecollideany(self.player, curr_level.enemies):
                    if not curr_level.is_over:
                        curr_level.is_over = True
                        self.player.die()

                if curr_level.is_over:
                    if not self.player.is_dead:
                        if self.current_level < len(self.levels) - 1 and self.levels[self.current_level + 1].is_locked:
                            self.levels[self.current_level + 1].is_locked = False
                            has_won = None
                    else:
                        has_won = "No"
                    try:
                        choice = self.display_level_complete(self.player.score, False, has_won)
                        if choice:
                            curr_level.reset()
                            break
                    #the window has been closed
                    except RuntimeError as e:
                        raise e

                pygame.display.flip()
                self.screen.blit(self.background, (0, 0))

                curr_level.update_stage()

                self.clock.tick(60)

            
