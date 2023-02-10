import os
import pygame
from game import Game
from player import Player
from client import Client
from exchange_info import ExchangeInfo, PlayerInitInfo
from button import ScreenText

class MultiPlayerGame(Game):
    def __init__(self, levels, screen):
        super().__init__(levels, screen)
        self.other_player = None
        self.client = Client()

    def main(self):
        flavour = self.display_player_choice()
        if not flavour:
            return
        level = self.display_level_choice()
        if not level:
            return  
        
        self.current_level = level - 1
        curr_level = self.levels[self.current_level]

        self.player = Player(curr_level.player_init_pos[0], curr_level.player_init_pos[1], flavour, 5)

        player_init_info = PlayerInitInfo(curr_level.player_init_pos[0], curr_level.player_init_pos[1], flavour, level)
        self.client.connect_to_server(player_init_info)
        self.display_waiting_screen()

        # connecting to the server and receiving the other player initialization info
        # in the form of PlayerInitInfo instance
        other_init_info = self.client.get_init_info()
        x = other_init_info.player_x
        y = other_init_info.player_y
        flavour = other_init_info.player_flavour
        self.other_player = Player(x, y, flavour, 5)

        running = True
        while running:
            # the info to be sent to the server
            client_info = ExchangeInfo(self.player.direction, self.player.rect, 
                                        self.player.score, self.player.is_dead)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        # if space is pressed the player will either blow or break some ice
                        self.player.change_board(curr_level.board, curr_level.fruit, curr_level.enemies, 
                                                    self.other_player.get_curr_board_cell())
                        # the board is changed so we should send the changed matrix to the server
                        client_info = ExchangeInfo(self.player.direction, self.player.rect, self.player.score, 
                                                    self.player.is_dead, curr_level.board)
            pressed_keys = pygame.key.get_pressed()

            # getting a list of all the fruit sprites the player has collided with
            # the third passed parameter is False for killing the sprites
            eaten_sprites = pygame.sprite.spritecollide(self.player, curr_level.fruit, False)
            if eaten_sprites != []:
                for sprite in eaten_sprites:
                    # the player cannot eat frozen fruit
                    if not sprite.is_frozen:
                        # getting the row and column index of the fruit and 
                        # setting its value to zero which indicates an empty cell
                        fruit_coords = sprite.get_map_coordinates()
                        curr_level.board[fruit_coords[0]][fruit_coords[1]] = 0
                        sprite.kill()
                        self.player.score += 5
                        # the board has been changed so the changed matrix is also
                        # included in the info that will be sent to the server
                        client_info = ExchangeInfo(self.player.direction, self.player.rect, 
                                                   self.player.score, self.player.is_dead, curr_level.board)
            
            # sending the information about the player to the server
            # and receiving the other player information
            other_client_info = self.client.send(client_info)

            #updating the other player with the received info from the server
            self.update_other_player(other_client_info)

            # if a object with board passed as an init argument is sent
            # we should update the board of the current level
            if other_client_info.board:
                curr_level.board = other_client_info.board

            if self.other_player.is_dead:
                self.other_player.die()

            if not self.player.is_dead:
                self.player.move(pressed_keys, curr_level.board)
            
            for enemy in curr_level.enemies:
                enemy.move(self.player, curr_level.board)

            # checking for a collision between the player and one of the enemies
            if pygame.sprite.spritecollideany(self.player, curr_level.enemies):
                self.player.die()

            self.player.draw(self.screen)
            self.other_player.draw(self.screen)
            for enemy in curr_level.enemies:
                enemy.draw(self.screen)

            # updating the display surface to the screen
            pygame.display.flip()

            #displaying the background
            self.screen.blit(self.background, (0, 0))

            curr_level.draw_board(self.screen, self.player.score, self.other_player.score)

            # checking if all of the fruit has been eaten
            # and if so updating the level stage
            curr_level.update_stage()

            self.clock.tick(60)
    
    def update_other_player(self, received_info):
        self.other_player.direction = received_info.player_direction
        self.other_player.rect = received_info.player_rect
        self.other_player.score = received_info.player_score
        self.other_player.is_dead = received_info.has_died

    def display_waiting_screen(self):
        font = pygame.font.Font(os.path.join("assets", "PixelIntv-OPxd.ttf"), 50)
        text_first_line = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "Waiting for",  "#4e4e94", 50)
        text_second_line = ScreenText(os.path.join("assets", "PixelIntv-OPxd.ttf"), "the other player",  "#4e4e94", 50)

        self.screen.fill("#d7e5f0")
        text_first_line.draw(self.screen, 120, 220)
        text_second_line.draw(self.screen, 120, 290)
        pygame.display.update()



