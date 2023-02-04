import pygame
import os
import time
from surroundings_collisions import get_valid_moves

EMPTY_CELL = 0
ICE_NUM = 1
FROZEN_FRUIT_NUM = 2
FRUIT_NUM = 3
IGLOO_NUM = 4
OFFSET = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, flavour):
        super(Player, self).__init__()
        self.flavor = flavour
        self.surf = pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_front.png"))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x, y)
        self.direction = "front"
        self.score = 0
        self.is_dead = False
        self.images = {"front": pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_front.png")),
                        "back" : pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_back.png")),
                        "left" : pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_left.png")),
                        "right" : pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_right.png"))}

    def draw(self, screen):
        if not self.is_dead:
            self.surf = self.images[self.direction]

        screen.blit(self.surf, self.rect)

    def die(self):
        self.is_dead = True
        self.surf = pygame.image.load(os.path.join("assets", f"{self.flavor}", f"dead_{self.flavor}.png")).convert_alpha()

    def get_curr_board_cell(self):
        i = self.rect.center[1] // 44 - 1
        j = self.rect.center[0] // 44 - 1
        return (i, j)

    def __str__(self):
        return f"({self.flavor}, {self.rect}, {self.direction})"

    def move(self, pressed_keys, frame_dims, screen_dims, board):
        valid_moves = get_valid_moves(self.rect, board, frame_dims, screen_dims)

        if pressed_keys[pygame.K_UP]:
            self.direction = "back"
            if valid_moves["up"]:
                self.rect.move_ip(0, -5)

        if pressed_keys[pygame.K_DOWN]:
            self.direction = "front"
            if valid_moves["down"]:
                self.rect.move_ip(0, 5)

        if pressed_keys[pygame.K_LEFT]:
            self.direction = "left"
            if valid_moves["left"]:
                self.rect.move_ip(-5, 0)

        if pressed_keys[pygame.K_RIGHT]:
            self.direction = "right"
            if valid_moves["right"]:
                self.rect.move_ip(5, 0) 

        # is_touching_frame(self.rect, frame_dims, screen_dims)

    def change_board(self, board, fruits, enemies, screen):
        i = self.get_curr_board_cell()[0]
        j = self.get_curr_board_cell()[1]
        
        if ((self.direction == "front" and i < len(board) - 1 and ICE_NUM <= board[i + 1][j] <= FROZEN_FRUIT_NUM) or 
        (self.direction == "back" and i > 0 and ICE_NUM <= board[i - 1][j] <= FROZEN_FRUIT_NUM) or 
        (self.direction == "left" and j > 0 and ICE_NUM <= board[i][j - 1] <= FROZEN_FRUIT_NUM) or 
        (self.direction == "right" and j < len(board[i]) - 1 and ICE_NUM <= board[i][j + 1] <= FROZEN_FRUIT_NUM)):
            self.break_ice(board, i, j, fruits)
        else:
            self.blow_ice(board, i, j, fruits, enemies, screen)

    def blow_ice(self, board, i, j, fruits, enemies, screen):
        if self.direction == "front":
            i += 1
            while i < len(board) and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j):
                    break
                if board[i][j] == FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = True
                    board[i][j] = FROZEN_FRUIT_NUM
                else:
                    board[i][j] = ICE_NUM
                    ice_cube = pygame.image.load(os.path.join("assets", "ice.png")).convert_alpha()
                    screen.blit(ice_cube, (j * 44 + 50, i * 44 + 48))
                i += 1

        if self.direction == "back":
            i -= 1
            while i >= 0 and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j):
                    break
                if board[i][j] == FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = True
                    board[i][j] = FROZEN_FRUIT_NUM
                else:
                    board[i][j] = ICE_NUM
                    ice_cube = pygame.image.load(os.path.join("assets", "ice.png")).convert_alpha()
                    screen.blit(ice_cube, (j * 44 + 50, i * 44 + 48))
                i -= 1

        if self.direction == "right":
            j += 1
            while j < len(board[i]) and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j):
                    break
                if board[i][j] == FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = True
                    board[i][j] = FROZEN_FRUIT_NUM
                else:
                    ice_cube = pygame.image.load(os.path.join("assets", "ice.png")).convert_alpha()
                    screen.blit(ice_cube, (j * 44 + 50, i * 44 + 48))
                    board[i][j] = ICE_NUM
                j += 1

        if self.direction == "left":
            j -= 1
            while j >= 0 and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j):
                    break
                if board[i][j] == FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = True
                    board[i][j] = FROZEN_FRUIT_NUM
                else:
                    ice_cube = pygame.image.load(os.path.join("assets", "ice.png")).convert_alpha()
                    screen.blit(ice_cube, (j * 44 + 50, i * 44 + 48))
                    board[i][j] = ICE_NUM
                j -= 1

    def break_ice(self, board, i, j, fruits):
        if self.direction == "front":
            i += 1
            while i < len(board) and (board[i][j] == ICE_NUM or board[i][j] == FROZEN_FRUIT_NUM):
                if board[i][j] == FROZEN_FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = False
                    board[i][j] = FRUIT_NUM
                else:
                    board[i][j] = EMPTY_CELL
                i += 1
        
        if self.direction == "back":
            i -= 1
            while i >= 0 and (board[i][j] == ICE_NUM or board[i][j] == FROZEN_FRUIT_NUM):
                if board[i][j] == FROZEN_FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                        print(j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = False
                    board[i][j] = FRUIT_NUM
                else:
                    board[i][j] = EMPTY_CELL
                i -= 1

        if self.direction == "right":
            j += 1
            while j < len(board[i]) and (board[i][j] == ICE_NUM or board[i][j] == FROZEN_FRUIT_NUM):
                if board[i][j] == FROZEN_FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = False
                    board[i][j] = FRUIT_NUM
                else:
                    board[i][j] = EMPTY_CELL
                j += 1
        
        if self.direction == "left":
            j -= 1
            while j >= 0 and (board[i][j] == ICE_NUM or board[i][j] == FROZEN_FRUIT_NUM):
                if board[i][j] == FROZEN_FRUIT_NUM:
                    try:
                        fruit = get_fruit_by_coordinates(fruits, j * 44 + 50, i * 44 + 48)
                    except ValueError as err:
                        raise err
                    fruit.is_frozen = False
                    board[i][j] = FRUIT_NUM
                else:
                    board[i][j] = EMPTY_CELL
                j -= 1
             
def is_touching_frame(player_rect, frame_dimensions, screen_dimensions):
    if player_rect.top < frame_dimensions[1]:
        player_rect.top = frame_dimensions[1]
    
    if player_rect.bottom > screen_dimensions[1] - frame_dimensions[1]:
        player_rect.bottom = screen_dimensions[1] - frame_dimensions[1]
    
    if player_rect.left < frame_dimensions[0]:
        player_rect.left = frame_dimensions[0]
    
    if player_rect.right > screen_dimensions[0] - frame_dimensions[0]:
        player_rect.right = screen_dimensions[0] - frame_dimensions[0]

def get_fruit_by_coordinates(fruits, i, j):
    for fruit in fruits:
        if fruit.get_coordinates() == (i, j):
            return fruit

    raise ValueError("No fruit with this coordinates")

def is_touching_enemy(enemies, i, j):
    for enemy in enemies:
        if enemy.curr_board_cell == (i, j):
            return True
    return False