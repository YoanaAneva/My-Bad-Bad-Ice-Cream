import pygame
import os
from math import sqrt
from typing import List, Tuple
from player import Player
from surroundings_collisions import get_valid_moves, FRAME_DIMENSIONS, SCREEN_DIMENSIONS

MIN_CYCLE_LEN = 30

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int, name: str = None):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join("assets", "polar_bear","polar_bear_with_spoon_front.png")).convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x, y)
        self.direction = "front"
        self.speed = speed
        self.name = name
        self.is_dead = False
        self.visited_cells = []
        self.images = {"front" : pygame.image.load(os.path.join("assets", "polar_bear", "polar_bear_with_spoon_front.png")).convert_alpha(),
                        "back" : pygame.image.load(os.path.join("assets", "polar_bear", "polar_bear_with_spoon_back.png")).convert_alpha(),
                        "left" : pygame.image.load(os.path.join("assets", "polar_bear", "polar_bear_with_spoon_left.png")).convert_alpha(),
                        "right" : pygame.image.load(os.path.join("assets", "polar_bear", "polar_bear_with_spoon_right.png")).convert_alpha(),
                        "dead" : pygame.image.load(os.path.join("assets", "polar_bear", "dead_polar_bear.png")).convert_alpha()}

    @property
    def curr_board_cell(self) -> Tuple[int, int]:
        return ((self.rect.center[1] - FRAME_DIMENSIONS[0]) // 44, (self.rect.center[0] - FRAME_DIMENSIONS[1]) // 44)

    def draw(self, screen: pygame.Surface):
        if not self.is_dead:
            self.surf = self.images[self.direction]
        else:
            self.surf = self.images["dead"]
        screen.blit(self.surf, self.rect)

    def move(self, player: Player, board: List[int]):
        if self.name == None:
            self.move_squares(board)
        else:
            self.chase(player, board)

    def move_squares(self, board: List[int]):        
            valid_moves = get_valid_moves(self.rect, board, True)

            if self.direction == "front":
                if not valid_moves["down"]:
                    self.direction = "right"
            elif self.direction == "right":
                if not valid_moves["right"]:   
                    self.direction = "back"
            elif self.direction == "back":
                if not valid_moves["up"]:
                    self.direction = "left"
            elif self.direction == "left":
                if not valid_moves["left"]:
                    self.direction = "front"
            
            if self.direction == "front":
                self.rect.move_ip(0, self.speed)
            if self.direction == "right":
                self.rect.move_ip(self.speed, 0)
            if self.direction == "back":
                self.rect.move_ip(0, -self.speed)
            if self.direction == "left":
                self.rect.move_ip(-self.speed, 0)

    def calculate_target(self, player: Player) -> Tuple[int, int]:
        if self.name == "Blinki":
            return player.rect.center

        if self.name == "Pinki":
            if player.direction == "right":
                if player.rect.center[0] + 10 > SCREEN_DIMENSIONS[0] - FRAME_DIMENSIONS[0]:
                    return (SCREEN_DIMENSIONS[0] - FRAME_DIMENSIONS[0] - player.rect.center[0], player.rect.center[1])
                else:
                    return (player.rect.center[0] + 10, player.rect.center[1])
            
            if player.direction == "left":
                if player.rect.center[0] - 10 <= FRAME_DIMENSIONS[0]:
                    return (FRAME_DIMENSIONS[0], player.rect.center[1])
                else:
                    return (player.rect.center[0] - 10, player.rect.center[1]) 
                
            if player.direction == "back":
                if player.rect.center[1] - 10 <= FRAME_DIMENSIONS[1]:
                    return (player.rect.center[0], FRAME_DIMENSIONS[1])
                else:
                    return (player.rect.center[0], player.rect.center[1] - 10)
            
            if player.direction == "front":
                if player.rect.center[1] + 10 >= SCREEN_DIMENSIONS[1] - FRAME_DIMENSIONS[1]:
                    return (player.rect.center[0], SCREEN_DIMENSIONS[1] - FRAME_DIMENSIONS[1] - player.rect.center[1])
                else:
                    return (player.rect.center[0], player.rect.center[1] + 10)

    def decide_next_move(self, player: Player, board: List[int]) -> str:
        valid_moves = get_valid_moves(self.rect, board, True)
        closest_distance = -1
        next_move = None
        next_step = (0, 0)
        target = self.calculate_target(player)

        step_up = self.rect.center[0], self.rect.center[1] - self.speed
        step_down = self.rect.center[0], self.rect.center[1] + self.speed
        step_left = self.rect.center[0] - self.speed, self.rect.center[1]
        step_right = self.rect.center[0] + self.speed, self.rect.center[1]

        if self.direction == "back":
            if valid_moves["up"] and not self.is_recently_visited(step_up):
                closest_distance = calculate_distance_to_target(step_up, target)
                next_step = step_up
                next_move = "up"
            if valid_moves["left"] and not self.is_recently_visited(step_left):
                distance_between_left_and_target = calculate_distance_to_target(step_left, target)
                if distance_between_left_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_left_and_target
                    next_step = step_left
                    next_move = "left"
            if valid_moves["right"] and not self.is_recently_visited(step_right):
                distance_between_right_and_target = calculate_distance_to_target(step_right, target)
                if distance_between_right_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_right_and_target
                    next_step = step_right
                    next_move = "right"

        if self.direction == "front":
            if valid_moves["down"] and not self.is_recently_visited(step_down):
                closest_distance = calculate_distance_to_target(step_down, target) 
                next_step = step_down
                next_move = "down"
            if valid_moves["left"] and not self.is_recently_visited(step_left):
                distance_between_left_and_target = calculate_distance_to_target(step_left, target)
                if distance_between_left_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_left_and_target
                    next_step = step_left
                    next_move = "left"
            if valid_moves["right"] and not self.is_recently_visited(step_right):
                distance_between_right_and_target = calculate_distance_to_target(step_right, target)
                if distance_between_right_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_right_and_target
                    next_step = step_right
                    next_move = "right"

        if self.direction == "left":
            if valid_moves["left"] and not self.is_recently_visited(step_left):
                closest_distance = calculate_distance_to_target(step_left, target)
                next_step = step_left
                next_move = "left"
            if valid_moves["up"] and not self.is_recently_visited(step_up):
                distance_between_up_and_target = calculate_distance_to_target(step_up, target)
                if distance_between_up_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_up_and_target
                    next_step = step_up
                    next_move = "up"
            if valid_moves["down"] and not self.is_recently_visited(step_down):
                distance_between_down_and_target = calculate_distance_to_target(step_down, target)
                if distance_between_down_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_down_and_target
                    next_step = step_down
                    next_move = "down"
        
        if self.direction == "right":
            if valid_moves["right"] and not self.is_recently_visited(step_right):
                closest_distance = calculate_distance_to_target(step_right, target)
                next_step = step_right
                next_move = "right"
            if valid_moves["up"] and not self.is_recently_visited(step_up):
                distance_between_up_and_target = calculate_distance_to_target(step_up, target)
                if distance_between_up_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_up_and_target
                    next_step = step_up
                    next_move = "up"
            if valid_moves["down"] and not self.is_recently_visited(step_down):
                distance_between_down_and_target = calculate_distance_to_target(step_down, target)
                if distance_between_down_and_target < closest_distance or closest_distance == -1:
                    closest_distance = distance_between_down_and_target
                    next_step = step_down
                    next_move = "down"

        self.visited_cells.append(next_step)
        if len(self.visited_cells) > MIN_CYCLE_LEN:
            del self.visited_cells[0]
        return next_move
                
    def chase(self, player: Player, board: List[int]):
        next_move = self.decide_next_move(player, board)

        if not player.is_dead:
            if next_move == "up":
                self.direction = "back"
                self.rect.move_ip(0, -self.speed)
            if next_move == "down":
                self.direction = "front"
                self.rect.move_ip(0, self.speed)        
            if next_move == "left":
                self.direction = "left"
                self.rect.move_ip(-self.speed, 0)        
            if next_move == "right":
                self.direction = "right"
                self.rect.move_ip(self.speed, 0)

    def is_recently_visited(self, step: Tuple[int, int]) -> bool:
        for coordinates in self.visited_cells:
            if coordinates == step:
                return True
        return False

def calculate_distance_to_target(enemy_center, player_center):
    x1 = enemy_center[0]
    y1 = enemy_center[1]
    x2 = player_center[0]
    y2 = player_center[1]
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
