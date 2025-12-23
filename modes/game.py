import os
import time
from abc import ABC, abstractmethod
from typing import List
import pygame
from game.level import Level, GAME_DURATION
from game.surroundings_collisions import FROZEN_FRUIT_NUM, FRUIT_NUM


class Game(ABC):
    """ Class to keep the information about a game. It is inherited by
    SinglePlayerGame and MultiPlayerGame that each implement their own
    logic for the main function
    """

    def __init__(self, levels: List[Level], screen: pygame.Surface):
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
        self.screen = screen
        self.levels = levels
        self.levels[0].is_locked = False  # unlock the first level
        self.current_level = 0            # keeps the number of current level
        self.player = None                # the player will be initialized later
        self.clock = pygame.time.Clock()

    @abstractmethod
    def main(self, flavour):
        pass
    
    def calculate_player_score_for_level(self, start_time: float, player_points: int) -> int:
        """ To get player's score for the level, the player's points
        are multiplied by 1 + the remaining seconds until 2 mins
        """
        time_passed = time.time() - start_time
        time_remaining = GAME_DURATION - time_passed if GAME_DURATION - time_passed > 0 else 0
        return int(player_points * (1 + time_remaining / 100))

    def is_in_top_10_scores(self, score: int, file_path: str) -> bool:
        with open(file_path) as file:
            counter = 9
            for line in file:
                number = int(line.split(":")[-1])
                if score > number:
                    return True
                if counter <= 0:
                    return False
                counter -= 1
        return True
    
    def write_in_scores(self, name: str, score: int, file_path: str) -> None:
        other_scores = []
        curr_pos = 0
        with open(file_path, "r+") as file:
            line = file.readline()
            while line != "":
                if line != "\n":
                    number = int(line.split(":")[-1])
                if score >= number:
                    other_scores = [line] + file.readlines()
                    break
                curr_pos = file.tell()
                line = file.readline()
            if other_scores != []:
                other_scores = other_scores[:-1]
            file.seek(curr_pos)
            file.write(f"{name} : {score}\n")
            file.writelines(other_scores)

    def melt(self, start_time: float, board: List[List[int]], is_multi_player: bool = False) -> bool:
        """Check if a specific time of the game has come when the board ice should be melted 
        and the player and enemies killed
        """
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
