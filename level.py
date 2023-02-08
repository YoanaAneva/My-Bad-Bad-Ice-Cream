import pygame
import os
from fruit import Fruit
from ice_cube import IceCube

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624
FRAME_DIMENSIONS = (50, 48)

EMPTY_CELL = 0
ICE_NUM = 1
FROZEN_FRUIT_NUM = 2
FRUIT_NUM = 3
IGLOO_NUM = 4
OFFSET = 5

class Level:
    def __init__(self, stage_boards, fruit_types, enemies, player_init_pos):
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
        self.stage = 0
        self.stage_boards = stage_boards
        self.fruit_types = fruit_types
        self.board = self.stage_boards[0]
        self.enemies = enemies
        self.fruit = pygame.sprite.Group()
        self.is_over = False
        self.player_init_pos = player_init_pos

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw_board(self, screen, player_score, other_score=None):
        self.fruit.remove(self.fruit.sprites())
        rows = len(self.board)
        cols = len(self.board[0])
        for i in range(rows):
            for j in range(cols):
                if self.board[i][j] == ICE_NUM:
                    ice_cube = IceCube()
                    ice_cube.draw(screen, j * 44 + FRAME_DIMENSIONS[0], i * 44 + FRAME_DIMENSIONS[1])
                if FROZEN_FRUIT_NUM <= self.board[i][j] <= FRUIT_NUM:
                    new_fruit = Fruit(self.fruit_types[self.stage], j * 44 + FRAME_DIMENSIONS[0], i * 44 + FRAME_DIMENSIONS[1])
                    if self.board[i][j] == FROZEN_FRUIT_NUM:
                        new_fruit.is_frozen = True
                    self.fruit.add(new_fruit)
                    new_fruit.draw(screen)

        font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), 30)
        pygame.draw.rect(screen, "#d7e5f0", pygame.Rect(50, 5, 250, 40))
        score = font.render(f"Your score: {player_score}", True, "#1c2e4a")
        screen.blit(score, (55, 7))
        if other_score:
            pygame.draw.rect(screen, "#d7e5f0", pygame.Rect(400, 5, 250, 40))
            score = font.render(f"Other score: {other_score}", True, "#1c2e4a")
            screen.blit(score, (405, 7))

    def update_stage(self):
        if not self.fruit:
            self.stage += 1
            if self.stage == len(self.stage_boards):
                self.is_over = True
            else:
                self.update_board(self.stage_boards[self.stage])

    def update_board(self, new_board):
        rows = len(self.board)
        cols = len(self.board[0])
        for i in range(rows):
            for j in range(cols):
                if new_board[i][j] == FRUIT_NUM:
                    if self.board[i][j] == ICE_NUM:
                        self.board[i][j] = FROZEN_FRUIT_NUM
                    else:
                        self.board[i][j] = FRUIT_NUM