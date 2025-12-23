
"""Module that helps in drawing and displaying different elements to
the screen such as buttons, text boxes
"""

import os
from abc import ABC, abstractmethod
from typing import Tuple
import pygame

TEXT_COLOR = "#735737"
CLICKED_TEXT_COLOR = "#eddec5"
FONT_PATH = os.path.join("assets", "PixelIntv-OPxd.ttf")

class Button(ABC):
    def __init__(self, x: int, y: int, width: int, height: int, content_surf: pygame.Surface, is_available: bool):
        self.dimensions = (width, height)
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join("assets", "button.png")).convert_alpha(), (width, height))
        self.clicked_surf = pygame.transform.scale(pygame.image.load(os.path.join("assets", "clicked_button.png")).convert_alpha(), (width, height))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x, y)
        self.content_surf = content_surf
        self.content_rect = self.content_surf.get_rect()
        self.is_available = is_available

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_available:
            screen.blit(self.surf, self.rect)
        else:
            screen.blit(self.clicked_surf, self.rect)
        screen.blit(self.content_surf, (self.rect.center[0] - self.content_rect.width/2, self.rect.center[1] - self.content_rect.height/2))
    
    def is_clicked(self, point: Tuple[int, int]) -> bool:
        if self.is_available:
            if self.rect.collidepoint(point):
                self.handle_click()
                return True
        return False
    
    def has_cursor_over_it(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    @abstractmethod
    def handle_click(self) -> None:
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join("assets", "clicked_button.png")).convert_alpha(), (self.dimensions))

class ImageButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface, image_dims: Tuple[int, int], is_available=True):
        image = pygame.transform.scale(image, image_dims)
        super().__init__(x, y, width, height, image, is_available)
    
    def handle_click(self) -> None:
        super().handle_click()


class TextButton(Button):
    def __init__(self, x: int, y:int, width: int, height: int, text: str, text_size: int, is_available=True):
        self.text = text
        self.font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), text_size)
        if is_available:
            text_surf = self.font.render(text, True, TEXT_COLOR)
        else:
            text_surf = self.font.render(text, True, CLICKED_TEXT_COLOR)
        super().__init__(x, y, width, height, text_surf, is_available)

    def handle_click(self) -> None:
        self.content_surf = self.font.render(self.text, True, CLICKED_TEXT_COLOR)
        super().handle_click()


class ScreenText:
    def __init__(self, text: str, colour: str | Tuple[int, int, int], size: int):
        self.text = text
        self.colour = colour
        self.size = size
        self.font = pygame.font.Font(FONT_PATH, size)
    
    def draw(self, screen: pygame.Surface, x: int, y: int):
        text_surf = self.font.render(self.text, True, self.colour)
        screen.blit(text_surf, (x, y))


class InputBox:
    def __init__(self, x: int, y: int, width: int, height: int, text_color: str | Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_color = text_color
        self.is_selected = False
        self.passive_color = "#536878"
        self.active_color = text_color
        self.color = self.passive_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(FONT_PATH, 50)
        self.input_text = ""
    
    def check_if_selected(self, click_pos: Tuple[int, int]) -> None:
        if self.rect.collidepoint(click_pos):
            self.is_selected = True
            self.color = self.active_color

    def delete_char(self) -> None:
        self.input_text = self.input_text[:-1]
    
    def add_char(self, char: str) -> None:
        self.input_text += char

    def draw(self, screen: pygame.Surface) -> None:
        text_surface = self.font.render(self.input_text, True, self.color)
        self.rect.width = max(self.width, text_surface.get_width() + 40)
        pygame.draw.rect(screen, self.color, self.rect, 5)
        screen.blit(text_surface, (self.x + 20, self.y + 5))


            
