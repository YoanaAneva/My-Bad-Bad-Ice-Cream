import os
from abc import ABC, abstractmethod
import pygame

class Game(ABC):
    def __init__(self, levels):
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
        self.levels = levels
        self.player = None

    @abstractmethod
    def main(self):
        pass