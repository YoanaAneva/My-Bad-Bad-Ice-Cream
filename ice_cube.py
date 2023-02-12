import os
import pygame

class IceCube():
    def __init__(self, x: int, y: int):
        self.surf = pygame.image.load(os.path.join("assets", "ice.png")).convert_alpha()
        self.melted_surf = pygame.image.load(os.path.join("assets", "melted_ice.png")).convert_alpha()
        self.x = x
        self.y = y

    def melt(self):
        self.surf = self.melted_surf

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, (self.x, self.y))
    
    def get_map_coordinates(self):
        return ((self.y- 48) // 44, (self.x - 50) // 44)
    
