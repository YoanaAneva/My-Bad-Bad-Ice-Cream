import os
import copy
import time
from typing import List, Tuple
import pygame
from fruit import Fruit
from ice_cube import IceCube
from widgets import ScreenText

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624
FRAME_DIMENSIONS = (50, 48)

EMPTY_CELL = 0
ICE_NUM = 1
FROZEN_FRUIT_NUM = 2
FRUIT_NUM = 3
IGLOO_NUM = 4
OFFSET = 5

GAME_DURATION = 90

class Level:
    def __init__(self, stage_boards: List[List[int]], fruit_types: List[str], enemies: pygame.sprite.Group, player_init_pos: Tuple[int, int], other_player_init_pos=None):
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
        self.stage = 0
        self.stage_boards = stage_boards
        self.fruit_types = fruit_types
        self.board = copy.deepcopy(self.stage_boards[0])
        self.enemies = enemies
        self.fruit = pygame.sprite.Group()
        self.ice_cubes = []
        self.is_over = False
        self.is_locked = True
        self.player_init_pos = player_init_pos
        self.other_player_init_pos = other_player_init_pos
        self.clock = pygame.transform.scale(pygame.image.load(os.path.join("assets", "clock.png")).convert_alpha(), (36, 36))

    def update_groups(self) -> None:
        rows = len(self.board)
        cols = len(self.board[0])
        for i in range(rows):
            for j in range(cols):
                if self.board[i][j] == ICE_NUM:
                    self.add_ice_if_not_in_list(i, j)
                if FROZEN_FRUIT_NUM <= self.board[i][j] <= FRUIT_NUM:
                    self.add_fruit_if_not_in_group(i, j)
                if self.board[i][j] == EMPTY_CELL:
                    self.remove_fruit_or_ice(i, j)

    def draw_board(self, screen: pygame.Surface, start_time: float, player_points: int, other_points: int = None) -> None:
        self.update_groups()
        for fruit in self.fruit:
            fruit.draw(screen)
        for ice_cube in self.ice_cubes:
            ice_cube.draw(screen)

        time_text = self.handle_time_text(start_time)
        pygame.draw.rect(screen, "#d7e5f0", pygame.Rect(679, 5, 66, 36))
        time_remaining = ScreenText(time_text, "#1c2e4a", 25)
        time_remaining.draw(screen, 683, 6)
        screen.blit(self.clock, (750, 5))

        pygame.draw.rect(screen, "#d7e5f0", pygame.Rect(35, 5, 260, 36))
        points = ScreenText(f"Your points: {player_points}", "#1c2e4a", 25)
        points.draw(screen, 45, 6)
        if other_points != None:
            pygame.draw.rect(screen, "#d7e5f0", pygame.Rect(330, 5, 270, 36))
            points = ScreenText(f"Other points: {other_points}", "#1c2e4a", 25)
            points.draw(screen, 339, 6)

    def update_stage(self) -> None:
        if not self.fruit and not self.is_over:
            self.stage += 1
            if self.stage >= len(self.stage_boards):
                self.is_over = True
            else:
                self.update_board(self.stage_boards[self.stage])

    def update_board(self, new_board: List[int]) -> None:
        rows = len(self.board)
        cols = len(self.board[0])
        for i in range(rows):
            for j in range(cols):
                if new_board[i][j] == FRUIT_NUM:
                    if self.board[i][j] == ICE_NUM:
                        self.remove_fruit_or_ice(i, j)
                        self.board[i][j] = FROZEN_FRUIT_NUM
                    else:
                        self.board[i][j] = FRUIT_NUM

    def reset(self) -> None:
        self.is_over = False
        self.stage = 0
        self.board = copy.deepcopy(self.stage_boards[0])
        self.fruit.remove(self.fruit.sprites())
        self.ice_cubes.clear()
        for enemy in self.enemies:
            enemy.is_dead = False

    def add_fruit_if_not_in_group(self, i, j) -> None:
        is_frozen = self.board[i][j] == FROZEN_FRUIT_NUM
        for fruit in self.fruit:
            if fruit.get_map_coordinates() == (i, j):
                fruit.is_frozen = is_frozen
                return
        new_fruit_x = j * 44 + FRAME_DIMENSIONS[0]
        new_fruit_y = i * 44 + FRAME_DIMENSIONS[1]
        new_fruit = Fruit(self.fruit_types[self.stage], new_fruit_x, new_fruit_y)
        new_fruit.is_frozen = is_frozen
        self.fruit.add(new_fruit)

    def add_ice_if_not_in_list(self, i, j) -> None:
        for ice_cube in self.ice_cubes:
            if ice_cube.get_map_coordinates() == (i, j):
                return
        new_ice_cube_x = j * 44 + FRAME_DIMENSIONS[0]
        new_ice_cube_y = i * 44 + FRAME_DIMENSIONS[1]
        new_ice_cube = IceCube(new_ice_cube_x, new_ice_cube_y)
        self.ice_cubes.append(new_ice_cube)

    def remove_fruit_or_ice(self, i, j) -> None:
        for fruit in self.fruit:
            if fruit.get_map_coordinates() == (i, j):
                fruit.kill()
                return
        if self.ice_cubes:
            for ind in range(len(self.ice_cubes)):
                if self.ice_cubes[ind].get_map_coordinates() == (i, j):
                    del self.ice_cubes[ind]
                    return

    def handle_time_text(self, start_time: float) -> str:
        if not self.is_over:
            time_passed = time.time() - start_time
            time_remaining = GAME_DURATION - time_passed if GAME_DURATION - time_passed > 0 else 0

            remaining_mins = int(time_remaining // 60)
            remaining_seconds = int(time_remaining % 60)
            seconds_text = f"{remaining_seconds}" if remaining_seconds >= 10 else f"0{remaining_seconds}"
            time_text = f"{remaining_mins}:{seconds_text}" 
            return time_text
        return "-:--"