import os
import pygame
from typing import Tuple

class Fruit(pygame.sprite.Sprite):
    def __init__(self, fruit_type: str, x: int, y: int):
        super(Fruit, self).__init__()
        self.surf = pygame.image.load(os.path.join("assets", f"{fruit_type}.png"))
        self.frozen_surf = pygame.image.load(os.path.join("assets", f"frozen_{fruit_type}.png")).convert_alpha()
        self.rect = self.surf.get_rect()
        self.is_frozen = False
        self.x = x
        self.y = y
        self.rect.move_ip(x, y) 

    def draw(self, screen: pygame.Surface):
        if not self.is_frozen:
            screen.blit(self.surf, (self.x, self.y))
        else:
            screen.blit(self.frozen_surf, (self.x, self.y))

    def get_coordinates(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def get_map_coordinates(self) -> Tuple[int, int]:
        return ((self.y - 48) // 44, (self.x - 50) // 44)