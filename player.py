import os
from typing import Tuple, List, Sequence
import pygame
from surroundings_collisions import get_valid_moves, EMPTY_CELL, ICE_NUM, FROZEN_FRUIT_NUM, FRUIT_NUM, IGLOO_NUM


class Player(pygame.sprite.Sprite):
    """Preserves info about the player"""

    def __init__(self, x: int, y: int, flavour: str, speed: int):
        super(Player, self).__init__()
        self.flavor = flavour
        self.speed = speed
        self.surf = pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_front_2.png")).convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x, y)
        self.direction = "front"
        self.points = 0
        self.is_dead = False
        self.images = {"front": [pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_front_1.png")).convert_alpha(),
                                 pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_front_2.png")).convert_alpha(),
                                 pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_front_3.png")).convert_alpha()],
                        "back" : [pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_back_1.png")).convert_alpha(),
                                  pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_back_2.png")).convert_alpha(),
                                  pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_back_3.png")).convert_alpha()],
                        "left" : [pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_left_1.png")).convert_alpha(),
                                  pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_left_2.png")).convert_alpha(),
                                  pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_left_3.png")).convert_alpha()],
                        "right" : [pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_right_1.png")).convert_alpha(),
                                   pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_right_2.png")).convert_alpha(),
                                   pygame.image.load(os.path.join("assets", f"{flavour}", f"{flavour}_right_3.png")).convert_alpha()]}
        self.count_steps = 0

    def draw(self, screen: pygame.Surface) -> None:
        if not self.is_dead:
            self.surf = self.images[self.direction][self.count_steps // 6]

        screen.blit(self.surf, self.rect)

    def die(self) -> None:
        self.is_dead = True
        self.surf = pygame.image.load(os.path.join("assets", f"{self.flavor}", f"dead_{self.flavor}.png")).convert_alpha()

    def get_curr_board_cell(self) -> Tuple[int, int]:
        i = self.rect.center[1] // 44 - 1
        j = self.rect.center[0] // 44 - 1
        return (i, j)

    def __str__(self):
        return f"({self.flavor}, {self.rect}, {self.direction})"

    def move(self, pressed_keys: Sequence[bool], board: List[List[int]]) -> None:
        valid_moves = get_valid_moves(self.rect, board)

        if pressed_keys[pygame.K_UP]:
            self.direction = "back"
            if valid_moves["up"]:
                self.rect.move_ip(0, -self.speed)

        if pressed_keys[pygame.K_DOWN]:
            self.direction = "front"
            if valid_moves["down"]:
                self.rect.move_ip(0, self.speed)

        if pressed_keys[pygame.K_LEFT]:
            self.direction = "left"
            if valid_moves["left"]:
                self.rect.move_ip(-self.speed, 0)

        if pressed_keys[pygame.K_RIGHT]:
            self.direction = "right"
            if valid_moves["right"]:
                self.rect.move_ip(self.speed, 0) 

        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_RIGHT]:
            if self.count_steps < 17:
                self.count_steps += 1
            else:
                self.count_steps = 0


    def change_board(self, board: List[List[int]], fruits: pygame.sprite.Group,
                     enemies: pygame.sprite.Group, 
                     other_player_cell: Tuple[int, int] = None) -> None:
        """Check if there is ice in front of the player 
        and decide whether it will break it or make more
        """
        i = self.get_curr_board_cell()[0]
        j = self.get_curr_board_cell()[1]
        
        if ((self.direction == "front" and i < len(board)-1 and ICE_NUM <= board[i+1][j] <= FROZEN_FRUIT_NUM) or
            (self.direction == "back" and i > 0 and ICE_NUM <= board[i-1][j] <= FROZEN_FRUIT_NUM) or 
            (self.direction == "left" and j > 0 and ICE_NUM <= board[i][j-1] <= FROZEN_FRUIT_NUM) or 
            (self.direction == "right" and j < len(board[i])-1 and ICE_NUM <= board[i][j+1] <= FROZEN_FRUIT_NUM)
            ):
            self.break_ice(board, i, j, fruits)
        else:
            self.blow_ice(board, i, j, fruits, enemies, other_player_cell)

    def blow_ice(self, board: List[List[int]], i: int, j: int, fruits: pygame.sprite.Group, enemies: pygame.sprite.Group, other_player_cell: Tuple[int, int]) -> None:
        if self.direction == "front":
            i += 1
            while i < len(board) and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j) or is_touching_player(other_player_cell, i, j):
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
                i += 1

        if self.direction == "back":
            i -= 1
            while i >= 0 and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j) or is_touching_player(other_player_cell, i, j):
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
                i -= 1

        if self.direction == "right":
            j += 1
            while j < len(board[i]) and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j) or is_touching_player(other_player_cell, i, j):
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
                j += 1

        if self.direction == "left":
            j -= 1
            while j >= 0 and board[i][j] != IGLOO_NUM and board[i][j] != ICE_NUM:
                if is_touching_enemy(enemies, i, j) or is_touching_player(other_player_cell, i, j):
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

def get_fruit_by_coordinates(fruits: pygame.sprite.Group, i: int, j: int) -> pygame.sprite:
    for fruit in fruits:
        if fruit.get_coordinates() == (i, j):
            return fruit

    raise ValueError("No fruit with this coordinates")

def is_touching_enemy(enemies: pygame.sprite.Group, i: int, j: int) -> bool:
    for enemy in enemies:
        if enemy.curr_board_cell == (i, j):
            return True
    return False

def is_touching_player(other_player_cell: Tuple[int, int], i: int, j: int) -> bool:
    if other_player_cell == (i, j):
        return True
    return False 
