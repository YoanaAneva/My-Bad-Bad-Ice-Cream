import os
from abc import ABC, abstractmethod
import pygame

TEXT_COLOR = "#735737"
CLICKED_TEXT_COLOR = "#eddec5"

class Button(ABC):
    def __init__(self, x, y, width, height, content_surf):
        self.dimensions = (width, height)
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join("assets", "button.png")).convert_alpha(), (width, height))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x, y)
        self.content_surf = content_surf
        self.content_rect = self.content_surf.get_rect()

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        screen.blit(self.content_surf, (self.rect.center[0] - self.content_rect.width/2, self.rect.center[1] - self.content_rect.height/2))
    
    def is_clicked(self, point):
        if self.rect.collidepoint(point):
            self.handle_click()
            return True
        return False
    
    @abstractmethod
    def handle_click(self):
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join("assets", "clicked_button.png")).convert_alpha(), (self.dimensions))

class ImageButton(Button):
    def __init__(self, x, y, width, height, image, image_dims):
        image = pygame.transform.scale(image, image_dims)
        super().__init__(x, y, width, height, image)
    
    def handle_click(self):
        super().handle_click()


class TextButton(Button):
    def __init__(self, x, y, width, height, text, text_size):
        self.text = text
        self.font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), text_size)
        text_surf = self.font.render(text, True, TEXT_COLOR)
        super().__init__(x, y, width, height, text_surf)

    def handle_click(self):
        self.content_surf = self.font.render(self.text, True, CLICKED_TEXT_COLOR)
        super().handle_click()


class ScreenText:
    def __init__(self, font_path, text, colour, size):
        self.text = text
        self.colour = colour
        self.size = size
        self.font = pygame.font.Font(font_path, size)
    
    def draw(self, screen, x, y):
        text_surf = self.font.render(self.text, True, self.colour)
        screen.blit(text_surf, (x, y))
