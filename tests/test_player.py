import unittest
import pygame
from player import Player 
from enemy import Enemy
from fruit import Fruit

FRAME_DIMS = (50, 48)
BLOCK_SIZE = 44

class TestPlayer(unittest.TestCase):
    def test_basics(self):
        pygame.init()
        pygame.display.set_mode((232, 228))
        expected_rect = pygame.Rect(FRAME_DIMS[0], FRAME_DIMS[1], BLOCK_SIZE, BLOCK_SIZE)
        # the player should be at cell (0,0)
        expected_board_cell = 0, 0

        player = Player(FRAME_DIMS[0], FRAME_DIMS[1], "vanilla", 5)
        board_cell = player.get_curr_board_cell()

        self.assertEqual(player.flavor, "vanilla")
        self.assertEqual(player.speed, 5)
        self.assertEqual(player.rect, expected_rect)
        self.assertEqual(player.direction, "front")
        self.assertEqual(player.points, 0)
        self.assertFalse(player.is_dead)
        self.assertEqual(board_cell, expected_board_cell)

        player.die()

        self.assertTrue(player.is_dead)

        pygame.quit()

    def test_movement(self):
        pygame.init()
        pygame.display.set_mode((232, 228))
        player_speed = 5
        pressed_keys = {pygame.K_UP : False, 
                        pygame.K_DOWN : False, 
                        pygame.K_LEFT : False, 
                        pygame.K_RIGHT : True}
        # the first player is spawned at the first cell of the board
        player1 = Player(FRAME_DIMS[0], FRAME_DIMS[1], "vanilla", player_speed)
        # the player is spawned at the second cell of the board
        player2 = Player(BLOCK_SIZE + FRAME_DIMS[0], FRAME_DIMS[1], "pink", player_speed)

        board = [[0, 0, 1], 
                 [0, 0, 0], 
                 [0, 0, 0]]

        # the first player should move 5 pixels to the right 
        expected_player1_rect = pygame.Rect(player_speed + FRAME_DIMS[0], FRAME_DIMS[1], BLOCK_SIZE, BLOCK_SIZE)
        # the second player should not move as there is an obstacle on its right
        expected_player2_rect = pygame.Rect(BLOCK_SIZE + FRAME_DIMS[0], FRAME_DIMS[1], BLOCK_SIZE, BLOCK_SIZE)
        expected_direction = "right"

        player1.move(pressed_keys, board)
        player2.move(pressed_keys, board)

        pygame.quit()

        self.assertEqual(player1.rect, expected_player1_rect)
        self.assertEqual(player2.rect, expected_player2_rect)
        self.assertEqual(player1.direction, expected_direction)
        self.assertEqual(player2.direction, expected_direction)

    def test_blowing_and_breaking_ice(self):
        pygame.init()
        pygame.display.set_mode((232, 228))
        player_speed = 5

        # the first player is spawned at the first cell of the board (0,0), facing front
        player = Player(FRAME_DIMS[0], FRAME_DIMS[1], "vanilla", player_speed)

        # fruit is spawned at the cell in front of the player (1,0)
        fruit = Fruit("banana", FRAME_DIMS[0], BLOCK_SIZE + FRAME_DIMS[1])
        fruits = pygame.sprite.Group()
        fruits.add(fruit)

        # enemy is spawned two block ahead of the player (cell(3,0))
        enemy = Enemy(FRAME_DIMS[0], 3 * BLOCK_SIZE + FRAME_DIMS[1], 2)
        enemies = pygame.sprite.Group()
        enemies.add(enemy)

        pygame.quit()

        # 0 - empty cell, 1 - ice, 2 - frozen fruit, 3 -fruit
        board = [[0, 0, 0, 0], 
                 [3, 0, 0, 0], 
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
        # the fruit on cell (1,0) should be frozrn, cell (2,0) should have ice
        # and cell (3,0) should not change because there is enemy on it 
        board_after_blowing_ice = [[0, 0, 0, 0],
                                   [2, 0, 0, 0],
                                   [1, 0, 0, 0],
                                   [0, 0, 0, 0]]
        # fruit on cell (1,0) should unfreeze anf the ice on cell (2,0) should disappear
        board_after_breaking_ice = [[0, 0, 0, 0],
                                    [3, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]]
        
        
        player.change_board(board, fruits, enemies)
        self.assertEqual(board, board_after_blowing_ice)

        player.change_board(board_after_blowing_ice, fruits, enemies)
        self.assertEqual(board_after_blowing_ice, board_after_breaking_ice)
    

if __name__ == '__main__':
    unittest.main()