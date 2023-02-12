import unittest
import pygame
from .. import Player

class TestPlayer(unittest.TestCase):
    def test_movement(self):
        pygame.init()
        screen = pygame.display.set_mode((132, 132))
        pressed_keys = {pygame.K_UP : False, pygame.K_DOWN : False, pygame.K_LEFT : False, pygame.K_RIGHT : True}
        board = [[0,0,0], [0,0,0], [0,0,0]]
        expected_player_rect = pygame.Rect(5, 0, 44, 44)
        pygame.quit()
        Player()
    
if __name__ == '__main__':
    unittest.main()