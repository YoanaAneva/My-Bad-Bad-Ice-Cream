import pygame
import os
from surroundings_collisions import get_valid_moves

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, pace, pace_size):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join("assets", "polar_bear_with_spoon_front.png")).convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x, y)
        self.direction = "front"
        self.pace = pace
        self.pace_size = pace_size
        self.pace_time = 0
        self.images = {"front" : pygame.image.load(os.path.join("assets", "polar_bear_with_spoon_front.png")).convert_alpha(),
                        "back" : pygame.image.load(os.path.join("assets", "polar_bear_with_spoon_back.png")).convert_alpha(),
                        "left" : pygame.image.load(os.path.join("assets", "polar_bear_with_spoon_left.png")).convert_alpha(),
                        "right" : pygame.image.load(os.path.join("assets", "polar_bear_with_spoon_right.png")).convert_alpha()}

    def get_curr_board_cell(self):
        return ((self.rect.center[1] - 50) // 44, (self.rect.center[0] - 48) // 44)

    def draw(self, screen):
        self.surf = self.images[self.direction]
        screen.blit(self.surf, self.rect)

    def move_squares(self, board, frame_dims, screen_dims):
        time_now = pygame.time.get_ticks()
        
        if time_now > self.pace_time + self.pace:
            self.pace_time = time_now
            
            valid_moves = get_valid_moves(self.rect, board, frame_dims, screen_dims, True)

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
                self.rect.move_ip(0, self.pace_size)
            if self.direction == "right":
                self.rect.move_ip(self.pace_size, 0)
            if self.direction == "back":
                self.rect.move_ip(0, -self.pace_size)
            if self.direction == "left":
                self.rect.move_ip(-self.pace_size, 0)
