import pygame
import os

class IceCube(pygame.sprite.Sprite):
    def __init__(self):
        super(IceCube, self).__init__()
        self.surf = pygame.image.load(os.path.join("assets", "ice.png"))
        self.rect = self.surf.get_rect()

    def draw(self, screen, top_x, top_y):
        screen.blit(self.surf, (top_x, top_y))
    
