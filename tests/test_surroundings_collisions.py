import unittest
import pygame
from entities.player import Player
from game.surroundings_collisions import check_for_ice_collisions,\
                                    check_for_frame_collisions,\
                                    check_for_igloo_collisions

FRAME_DIMS = (50, 48)
BLOCK_SIZE = 44

class TestSurroundingsCollisions(unittest.TestCase):
    def test_check_for_frame_collisions(self):
        pygame.display.set_mode((232, 228))
        # the player should be really close to the obstacle in
        # order to not be allowed to go any further (that's why -5)
        player_speed = 5
        player = Player(FRAME_DIMS[0] - player_speed, FRAME_DIMS[1] - player_speed, "pink", player_speed)

        expected_player_rect = pygame.Rect(FRAME_DIMS[0], FRAME_DIMS[1], BLOCK_SIZE, BLOCK_SIZE)
    
        check_for_frame_collisions(player.rect, {}, False)
     
        self.assertEqual(player.rect, expected_player_rect)

    def test_check_for_igloo_collisions(self):
        pygame.display.set_mode((232, 228))
        # the player should be really close to the obstacle in
        # order to not be allowed to go any further (that's why -5)
        player = Player(FRAME_DIMS[0] + BLOCK_SIZE, FRAME_DIMS[1], "pink", 5)
        valid_moves = {"up" : True, 
                       "down" : True, 
                       "left" : True,
                       "right" : True}
        # 4 - indicates igloo
        board = [[0, 0, 0, 0],
                 [0, 4, 4, 0],
                 [0, 4, 4, 0],
                 [0, 0, 0, 0]]

        excepted_valid_moves = {"up" : True, 
                                "down" : False, 
                                "left" : True,
                                "right" : True}

        check_for_igloo_collisions(player.rect, board, valid_moves)

        self.assertEqual(valid_moves, excepted_valid_moves)

    def test_check_for_ice_collisions(self):
        pygame.display.set_mode((232, 228))
        # the player should be really close to the obstacle in
        # order to not be allowed to go any further (that's why -5)
        player = Player(FRAME_DIMS[0] + BLOCK_SIZE - 5, FRAME_DIMS[1] + BLOCK_SIZE - 5, "pink", 5)
        valid_moves = {"up" : True, 
                       "down" : True, 
                       "left" : True,
                       "right" : True}
        # 1 - indicates block with ice on it
        board = [[0, 1, 0, 0],
                 [1, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

        excepted_valid_moves = {"up" : False, 
                                "down" : True, 
                                "left" : False,
                                "right" : True}

        check_for_ice_collisions(player.rect, board, valid_moves)

        self.assertEqual(valid_moves, excepted_valid_moves)
    

if __name__ == '__main__':
    unittest.main()