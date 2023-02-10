import os
from abc import ABC, abstractmethod
import pygame
from player import Player
from button import TextButton, ImageButton, ScreenText

class Game(ABC):
    def __init__(self, levels, screen):
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
        self.screen = screen
        self.levels = levels
        self.levels[0].is_locked = False
        self.current_level = 0
        self.player = None
        self.clock = pygame.time.Clock()
        self.player = None

    @abstractmethod
    def main(self, flavour):
        pass

    @staticmethod
    def display_starting_screen(screen):
        text_first_line = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "My Bad", "#290f6a", 50)
        text_second_line = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "Bad Ice-Cream", "#290f6a", 70)
        text_third_line = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "Attempt", "#290f6a", 50)
        start_btn = TextButton(200, 350, 400, 100, "Click to Lick", 40)
        scores_btn = TextButton(200, 500, 400, 100, "Scores", 40)

        while True:
            text_first_line.draw(screen, 280, 50)
            text_second_line.draw(screen, 100, 120)
            text_third_line.draw(screen, 280, 200)
            start_btn.draw(screen)
            scores_btn.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if start_btn.is_clicked(click_pos):
                        return "start"
                    if scores_btn.is_clicked(click_pos):
                        return "scores"
            pygame.display.update()
            screen.fill("#d7e5f0")

    @staticmethod
    def display_game_mode_choice(screen):
        text = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "Choose a flavour:",  "#4e4e94", 60)
        single_player_btn = TextButton(70, 360, 300, 120, "Single player", 30)
        multi_player_btn = TextButton(440, 360, 300, 120, "Multi player", 30)

        while True:
            text.draw(screen, 90, 100)
            single_player_btn.draw(screen)
            multi_player_btn.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if single_player_btn.is_clicked(click_pos):
                        return "single-player"
                    if multi_player_btn.is_clicked(click_pos):
                        return "multi-player"

            pygame.display.update()
            screen.fill("#d7e5f0")

    def display_player_choice(self):
        text = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "Choose a flavour:",  "#4e4e94", 60)
        chocolate_btn = ImageButton(42, 360, 210, 210, pygame.image.load(os.path.join("assets", "chocolate", "chocolate_front.png")).convert_alpha(), (176, 176))
        vanilla_btn = ImageButton(294, 360, 210, 210, pygame.image.load(os.path.join("assets", "vanilla", "vanilla_front.png")).convert_alpha(), (176, 176))
        pink_btn = ImageButton(546, 360, 210, 210, pygame.image.load(os.path.join("assets", "pink", "pink_front.png")).convert_alpha(), (176, 176))
        
        while True:
            text.draw(self.screen, 100, 100)
            chocolate_btn.draw(self.screen)
            vanilla_btn.draw(self.screen)
            pink_btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("closed window")
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
        text = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "Choose a level:",  "#4e4e94", 60)
        level1_btn = TextButton(100, 150, 118, 118, "1", 50, not self.levels[0].is_locked)
        level2_btn = TextButton(100, 308, 118, 118, "2", 50, not self.levels[1].is_locked)
        level3_btn = TextButton(100, 466, 118, 118, "3", 50, not self.levels[2].is_locked)

        while True:
            text.draw(self.screen, 100, 50)
            level1_btn.draw(self.screen)
            level2_btn.draw(self.screen)
            level3_btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("closed window")
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

    def display_level_complete(self, score, is_multiplayer, has_won):
        if is_multiplayer:
            if has_won == "No":
                text = "YOU LOSE"
            elif has_won == "Yes":
                text = "YOU WIN"
            else:
                text = "TIE GAME"
        else:
            if has_won == "No":
                text = "YOU GOT EATEN"
            else:
                text = "LEVEL COMPLETE"
        message = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), text, "#735737", 40)
        score_text = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), f"score: {score}", "#735737", 40)
        select_level_btn = TextButton(300, 300, 200, 80, "select level", 20)
        back_to_menu_btn = TextButton(300, 400, 200, 80, "back to menu", 20)

        pygame.draw.rect(self.screen, "#735737", pygame.Rect(145, 115, 510, 394))
        pygame.draw.rect(self.screen, "#d7e5f0", pygame.Rect(155, 125, 490, 374))

        message.draw(self.screen, 220, 170)
        score_text.draw(self.screen, 220, 210)
        select_level_btn.draw(self.screen)
        back_to_menu_btn.draw(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise RuntimeError("closed window")
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                if select_level_btn.is_clicked(click_pos):
                    return "select level"
                if back_to_menu_btn.is_clicked(click_pos):
                    return "back to menu"
        pygame.display.update()

        
