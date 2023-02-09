import os
import time
import pygame
from game import Game
from button import TextButton, ImageButton

class SinglePlayerGame(Game):
    def __init__(self, levels, screen):
        super().__init__(levels, screen)

    def main(self):
        self.display_level_choice()

        running = True
        while running:
            curr_level = self.levels[self.current_level]
            curr_level.draw_board(self.screen, self.player.score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        self.player.change_board(curr_level.board, curr_level.fruit,
                                                    curr_level.enemies)

            eaten_sprites = pygame.sprite.spritecollide(self.player, curr_level.fruit, False)
            if eaten_sprites != []:
                for sprite in eaten_sprites:
                    if not sprite.is_frozen:
                        fruit_coords = sprite.get_map_coordinates()
                        curr_level.board[fruit_coords[0]][fruit_coords[1]] = 0
                        sprite.kill()
                        self.player.score += 5

            pressed_keys = pygame.key.get_pressed()
            
            if not self.player.is_dead:
                self.player.move(pressed_keys, curr_level.board)

            for enemy in curr_level.enemies:
                enemy.move(self.player, curr_level.board)
            
            if pygame.sprite.spritecollideany(self.player, curr_level.enemies):
                self.player.die()

            self.player.draw(self.screen)

            for enemy in curr_level.enemies:
                enemy.draw(self.screen)

            curr_level.update_stage()

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

            self.clock.tick(30)

            
