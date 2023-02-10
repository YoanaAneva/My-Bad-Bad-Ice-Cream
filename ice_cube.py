import pygame
import os

class IceCube():
    def __init__(self, x, y):
        self.surf = pygame.image.load(os.path.join("assets", "ice.png"))
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.surf, (self.x, self.y))
    
    def get_map_coordinates(self):
        return ((self.y- 48) // 44, (self.x - 50) // 44)
    
