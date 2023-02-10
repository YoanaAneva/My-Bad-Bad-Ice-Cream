import os
import time
import pygame
from game import Game
from player import Player
from fruit import Fruit
from ice_cube import IceCube

PLAYER_SPEED = 3

class SinglePlayerGame(Game):
    def __init__(self, levels, screen):
        super().__init__(levels, screen)

    def main(self):
        response = self.display_starting_screen()
        if not response:
            return
        
        flavour = self.display_player_choice()
        # the window has been closed
        if not flavour:
            return
        level = self.display_level_choice()
        # the window has been closed
        if not level:
            return

        self.current_level = level - 1
        curr_level = self.levels[self.current_level]

        self.player = Player(curr_level.player_init_pos[0], curr_level.player_init_pos[1], flavour, PLAYER_SPEED)

        # prev_frame_time = time.time()
        running = True
        while running:
            # now = time.time()
            # dt = now - prev_frame_time
            # prev_frame_time = now

            curr_level.draw_board(self.screen, self.player.score)

            self.player.draw(self.screen)
            for enemy in curr_level.enemies:
                enemy.draw(self.screen)
            
            # now = time.time()
            # dt = now - prev_frame_time
            # prev_frame_time = now
            # print("2", dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
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
                self.player.die()
  
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

            curr_level.update_stage()

            if curr_level.is_over:
                self.display_level_complete(self.player.score, False)

            self.clock.tick(60)

            
