import os
from abc import ABC, abstractmethod
import pygame
from player import Player
from button import TextButton, ImageButton

class Game(ABC):
    def __init__(self, levels, screen):
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
        self.screen = screen
        self.levels = levels
        self.current_level = 0
        self.player = None
        self.clock = pygame.time.Clock()
        self.player = Player(94, 92, "vanilla")

    @abstractmethod
    def main(self):
        pass

    @staticmethod
    def display_game_mode_choice(screen):
        font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), 60)
        text_surf = font.render("How many scoops?", True, "#4e4e94")
        single_player_btn = TextButton(70, 360, 300, 120, "Single player", 30)
        multi_player_btn = TextButton(440, 360, 300, 120, "Multi player", 30)

        while True:
            screen.blit(text_surf, (90, 100))
            single_player_btn.draw(screen)
            multi_player_btn.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Closed window"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if single_player_btn.is_clicked(click_pos):
                        return "single-player"
                    if multi_player_btn.is_clicked(click_pos):
                        return "multi-player"

            pygame.display.update()
            screen.fill("#d7e5f0")

    def display_player_choice(self):
        font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), 60)
        text_surf = font.render("Choose a flavour:", True, "#4e4e94")
        chocolate_btn = ImageButton(42, 360, 210, 210, pygame.image.load(os.path.join("assets", "chocolate", "chocolate_front.png")).convert_alpha(), (176, 176))
        vanilla_btn = ImageButton(294, 360, 210, 210, pygame.image.load(os.path.join("assets", "vanilla", "vanilla_front.png")).convert_alpha(), (176, 176))
        pink_btn = ImageButton(546, 360, 210, 210, pygame.image.load(os.path.join("assets", "pink", "pink_front.png")).convert_alpha(), (176, 176))
        
        while True:
            self.screen.blit(text_surf, (100, 100))
            chocolate_btn.draw(self.screen)
            vanilla_btn.draw(self.screen)
            pink_btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if chocolate_btn.is_clicked(click_pos):
                        return "chocolate"
                    if vanilla_btn.is_clicked(click_pos):
                        return "vanilla"
                    if pink_btn.is_clicked(click_pos):
                        return "pink"

            pygame.display.update()
            self.screen.fill("#d7e5f0")

    def display_level_choice(self):
        font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), 60)
        text_surf = font.render("Choose a level:", True, "#4e4e94")
        level1_btn = TextButton(100, 150, 118, 118, "1", 50)
        level2_btn = TextButton(100, 308, 118, 118, "2", 50)
        level3_btn = TextButton(100, 466, 118, 118, "3", 50)

        while True:
            self.screen.blit(text_surf, (100, 50))
            level1_btn.draw(self.screen)
            level2_btn.draw(self.screen)
            level3_btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if level1_btn.is_clicked(click_pos):
                        return 1
                    if level2_btn.is_clicked(click_pos):
                        return 2
                    if level3_btn.is_clicked(click_pos):
                        return 3

            pygame.display.update()
            self.screen.fill("#d7e5f0")


