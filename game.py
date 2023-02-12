import os
import time
from abc import ABC, abstractmethod
from typing import Tuple, List
import pygame
from level import Level
from widgets import TextButton, ImageButton, ScreenText, InputBox
from surroundings_collisions import FROZEN_FRUIT_NUM, FRUIT_NUM

GAME_DURATION = 90

class Game(ABC):
    def __init__(self, levels: List[Level], screen: pygame.Surface):
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
        self.screen = screen
        self.levels = levels
        self.levels[0].is_locked = False
        self.current_level = 0
        self.player = None
        self.clock = pygame.time.Clock()
        self.player = None

    @abstractmethod
    def main(self, flavour):
        pass
    
    # to get player's score for the level, the player's points are
    # multiplied by 1 + the remaining seconds until 2 mins
    def calculate_player_score_for_level(self, start_time: float, player_points: int) -> int:
        time_passed = time.time() - start_time
        time_remaining = GAME_DURATION - time_passed if GAME_DURATION - time_passed > 0 else 0
        return int(player_points * (1 + time_remaining / 100))

    def is_in_top_10_scores(self, score: int) -> bool:
        with open(os.path.join("assets", "scores.txt")) as file:
            counter = 10
            for line in file:
                number = int(line.split(":")[-1])
                if score > number:
                    return True
                if counter <= 0:
                    return False
                counter -= 1
        return True
    
    def write_in_scores(self, name: str, score: int) -> None:
        other_scores = []
        curr_pos = 0
        with open(os.path.join("assets", "scores.txt"), "r+") as file:
            line = file.readline()
            while line != "":
                if line != "\n":
                    number = int(line.split(":")[-1])
                if score > number:
                    other_scores = [line] + file.readlines()
                    break
                curr_pos = file.tell()
                line = file.readline()
            file.seek(curr_pos)
            file.write(f"{name} : {score}\n")
            file.writelines(other_scores)



    def melt(self, start_time: float, board: List[int], is_multi_player: bool = False) -> bool:
        if GAME_DURATION - (time.time() - start_time) <= 0:
            self.levels[self.current_level].ice_cubes
            self.player.die()
            if is_multi_player:
                self.other_player.die()
            for enemy in self.levels[self.current_level].enemies:
                enemy.is_dead = True
            for ice_cube in self.levels[self.current_level].ice_cubes:
                ice_cube.melt()
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == FROZEN_FRUIT_NUM:
                        board[i][j] = FRUIT_NUM
            return True
        return False
