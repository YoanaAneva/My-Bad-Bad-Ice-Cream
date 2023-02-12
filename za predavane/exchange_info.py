from typing import List
import pygame

class ExchangeInfo:
    def __init__(self, player_direction: str, player_rect: pygame.Rect, player_points: int, has_died: bool, board: List[int] = None):
        self.player_direction = player_direction
        self.player_rect = player_rect
        self.player_points = player_points
        self.has_died = has_died
        self.board = board

    def __str__(self):
        return f"({self.player_direction}, {self.player_rect})"

class PlayerInitInfo:
    def __init__(self, player_x: int, player_y: int, player_flavour: str, level: int):
            self.player_x = player_x
            self.player_y = player_y
            self.player_flavour = player_flavour
            self.level = level        