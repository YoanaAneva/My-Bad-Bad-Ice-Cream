import time
import os
import pygame
from widgets import TextButton, ImageButton, ScreenText, InputBox

class Display:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def display_starting_screen(self) -> str:
        text_first_line = ScreenText("My Bad", "#290f6a", 50)
        text_second_line = ScreenText("Bad Ice-Cream", "#290f6a", 70)
        text_third_line = ScreenText("Attempt", "#290f6a", 50)
        start_btn = TextButton(200, 350, 400, 100, "Click to Lick", 40)
        scores_btn = TextButton(200, 500, 400, 100, "Scores", 40)

        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("Closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if start_btn.is_clicked(click_pos):                     
                        choice = "start"
                    if scores_btn.is_clicked(click_pos):                     
                        choice = "scores"
                        
            text_first_line.draw(self.screen, 280, 50)
            text_second_line.draw(self.screen, 100, 120)
            text_third_line.draw(self.screen, 280, 200)
            start_btn.draw(self.screen)
            scores_btn.draw(self.screen)
            pygame.display.update()
            self.screen.fill("#d7e5f0")

        time.sleep(0.2)
        return choice

    def display_game_mode_choice(self) -> str:
        text = ScreenText("Choose a flavour:",  "#4e4e94", 60)
        single_player_btn = TextButton(70, 360, 300, 120, "Single player", 30)
        multi_player_btn = TextButton(440, 360, 300, 120, "Multi player", 30)

        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("Closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if single_player_btn.is_clicked(click_pos):                    
                        choice = "single-player"
                    elif multi_player_btn.is_clicked(click_pos):                      
                        choice = "multi-player"

            text.draw(self.screen, 90, 100)
            single_player_btn.draw(self.screen)
            multi_player_btn.draw(self.screen)
            pygame.display.update()
            self.screen.fill("#d7e5f0")

        time.sleep(0.2)
        return choice
            
    def display_scores(self) -> str:
        back_btn = TextButton(650, 520, 100, 70, "back", 30)
        score_lines = []
        with open(os.path.join("assets", "scores.txt")) as file:
            for line in file:
                score_line = ScreenText(line.strip(), "#4e4e94", 40)
                score_lines.append(score_line)

        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("Closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if back_btn.is_clicked(click_pos):
                        choice = "back to menu"

            back_btn.draw(self.screen)
            k = 15
            for score_line in score_lines:
                score_line.draw(self.screen, 70, k)
                k += 60
            pygame.display.update()
            self.screen.fill("#d7e5f0")

        time.sleep(0.2)
        return choice

    def display_player_choice(self) -> str:
        text = ScreenText("Choose a flavour:",  "#4e4e94", 60)
        chocolate_btn = ImageButton(42, 360, 210, 210, pygame.image.load(os.path.join("assets", "chocolate", "chocolate_front.png")).convert_alpha(), (176, 176))
        vanilla_btn = ImageButton(294, 360, 210, 210, pygame.image.load(os.path.join("assets", "vanilla", "vanilla_front.png")).convert_alpha(), (176, 176))
        pink_btn = ImageButton(546, 360, 210, 210, pygame.image.load(os.path.join("assets", "pink", "pink_front.png")).convert_alpha(), (176, 176))
        
        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("Closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if chocolate_btn.is_clicked(click_pos):
                        choice = "chocolate"
                    if vanilla_btn.is_clicked(click_pos):
                        choice = "vanilla"
                    if pink_btn.is_clicked(click_pos):
                        choice = "pink"

            text.draw(self.screen, 100, 100)
            chocolate_btn.draw(self.screen)
            vanilla_btn.draw(self.screen)
            pink_btn.draw(self.screen)
            pygame.display.update()
            self.screen.fill("#d7e5f0")

        time.sleep(0.2)
        return choice

    def display_level_choice(self, levels) -> str:
        text = ScreenText("Choose a level:",  "#4e4e94", 60)
        if len(levels) > 0:
            level1_btn = TextButton(60, 150, 118, 118, "1", 50, not levels[0].is_locked)
        if len(levels) > 1:
            level2_btn = TextButton(60, 308, 118, 118, "2", 50, not levels[1].is_locked)
        if len(levels) > 2:
            level3_btn = TextButton(60, 466, 118, 118, "3", 50, not levels[2].is_locked)
        level1_text1 = ScreenText("Just have fun and eat some fruit.", "#4e4e94", 20) 
        level1_text2 = ScreenText("There are polar bears out for some tasty" , "#4e4e94", 20)
        level1_text3 = ScreenText("ice-cream, but they ain't very smart... " , "#4e4e94", 20)
        level2_text1 = ScreenText("Be concerned about time during this", "#4e4e94", 20)
        level2_text2 = ScreenText("level. Hurry up or the reality we", "#4e4e94", 20)
        level2_text3 = ScreenText("live in may surprise you in a bad way...", "#4e4e94", 20)
        level3_text1 = ScreenText("There is something else you gotta worry", "#4e4e94", 20)
        level3_text2 = ScreenText("about this level. The bears are now ", "#4e4e94", 20)
        level3_text3 = ScreenText("starving and won't just wander around...", "#4e4e94", 20)

        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("Closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if level1_btn.is_clicked(click_pos):
                        choice = 1
                    if level2_btn.is_clicked(click_pos):
                        choice = 2
                    if level3_btn.is_clicked(click_pos):
                        choice = 3
            mouse_pos = pygame.mouse.get_pos()
            if level1_btn.has_cursor_over_it(mouse_pos):
                level1_text1.draw(self.screen, 205, 180)
                level1_text2.draw(self.screen, 205, 210)
                level1_text3.draw(self.screen, 205, 240)
            if level2_btn.has_cursor_over_it(mouse_pos):
                level2_text1.draw(self.screen, 205, 340)
                level2_text2.draw(self.screen, 205, 370)
                level2_text3.draw(self.screen, 205, 400)
            if level3_btn.has_cursor_over_it(mouse_pos):
                level3_text1.draw(self.screen, 205, 495)
                level3_text2.draw(self.screen, 205, 525)
                level3_text3.draw(self.screen, 205, 555)
            text.draw(self.screen, 100, 50)
            level1_btn.draw(self.screen)
            level2_btn.draw(self.screen)
            level3_btn.draw(self.screen)
            pygame.display.update()
            self.screen.fill("#d7e5f0")
            clock = pygame.time.Clock()
            clock.tick(60)

        time.sleep(0.2)
        return choice

    def display_level_complete(self, curr_score: int, total_score: int, is_multiplayer: bool, has_won: str) -> str:
        if is_multiplayer:
            if has_won == "No":
                text = "YOU LOSE"
            elif has_won == "Yes":
                text = "YOU WIN"
            else:
                text = "TIE GAME"
        else:
            if has_won == "No":
                text = "YOU DIED"
            else:
                text = "LEVEL COMPLETE"
        message = ScreenText(text, "#735737", 40)
        score_text = ScreenText(f"score: {curr_score}", "#735737", 40)
        total_score_text = ScreenText(f"total score: {total_score}", "#735737", 40)
        select_level_btn = TextButton(300, 310, 200, 80, "select level", 20)
        back_to_menu_btn = TextButton(300, 410, 200, 80, "back to menu", 20)

        pygame.draw.rect(self.screen, "#735737", pygame.Rect(145, 115, 510, 394))
        pygame.draw.rect(self.screen, "#d7e5f0", pygame.Rect(155, 125, 490, 374))

        message.draw(self.screen, 260, 150)
        score_text.draw(self.screen, 210, 190)
        total_score_text.draw(self.screen, 210, 230)
        select_level_btn.draw(self.screen)
        back_to_menu_btn.draw(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise RuntimeError("Closed window")
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                if select_level_btn.is_clicked(click_pos):
                    return "select level"
                if back_to_menu_btn.is_clicked(click_pos):
                    return "back to menu"
        pygame.display.update()

    def display_name_input_screen(self, global_score: int) -> str:
        message1 = ScreenText("Your score is in", "#4e4e94", 50)
        message11 = ScreenText("top 10's!", "#4e4e94", 50)
        message2 = ScreenText(f"SCORE: {global_score}", "#4e4e94", 50)
        message3 = ScreenText("Enter your name and press Enter", "#4e4e94", 35)
        input_box = InputBox(50, 430, 300, 80, "#4e4e94")

        while True:
            message1.draw(self.screen, 150, 70)
            message11.draw(self.screen, 250, 140)
            message2.draw(self.screen, 50, 260)
            message3.draw(self.screen, 50, 350)
            input_box.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise RuntimeError("Closed window")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    input_box.check_if_selected(click_pos)
                if event.type == pygame.KEYDOWN:
                    if input_box.is_selected:
                        if event.key == pygame.K_RETURN:
                            time.sleep(0.2)
                            return input_box.input_text
                        if event.key == pygame.K_BACKSPACE:
                            input_box.delete_char()
                        else:
                            input_box.add_char(event.unicode)
            pygame.display.update()
            self.screen.fill("#d7e5f0")

    def display_melted_info(self) -> None:
        pygame.draw.rect(self.screen, "#d7e5f0", pygame.Rect(60, 90, 680, 220))
        text_line1 = ScreenText("Too late!", "#4c0001", 50)
        text_line2 = ScreenText("Global Warming just", "#4c0001", 50)
        text_line3 = ScreenText("melted The Arctic...", "#4c0001", 50)
        text_line1.draw(self.screen, 200, 100)
        text_line2.draw(self.screen, 90, 170)
        text_line3.draw(self.screen, 90, 240)

        pygame.display.update()            
        time.sleep(5)
