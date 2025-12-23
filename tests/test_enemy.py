import unittest
import pygame
from entities.player import Player 
from entities.enemy import Enemy

FRAME_DIMS = (50, 48)
BLOCK_SIZE = 44

class TestEnemy(unittest.TestCase):
    def test_initialization(self):
        pygame.display.set_mode((232, 228))
        expected_rect = pygame.Rect(0 + FRAME_DIMS[0], 0 + FRAME_DIMS[1], BLOCK_SIZE, BLOCK_SIZE)
        expected_board_cell = 0, 0

        enemy = Enemy(0 + FRAME_DIMS[0], 0 + FRAME_DIMS[1], 5, "Polar bear with a spoon")

        self.assertEqual(enemy.rect, expected_rect)
        self.assertEqual(enemy.direction, "front")
        self.assertEqual(enemy.speed, 5)
        self.assertEqual(enemy.name, "Polar bear with a spoon")
        self.assertFalse(enemy.is_dead)
        self.assertEqual(enemy.visited_points, [])
        self.assertEqual(enemy.curr_board_cell, expected_board_cell)

    def test_move_in_squares(self):
        enemy_speed = 5
        enemy = Enemy(0 + FRAME_DIMS[0], FRAME_DIMS[1], enemy_speed)
        board = [[0, 0, 0, 0],
                 [1, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

        # the enemy first checks if it can move down by 5 pixels but since 
        # there is ice in front of it, it tries to move right which is possible
        expected_rect = pygame.Rect(enemy_speed + FRAME_DIMS[0], FRAME_DIMS[1], BLOCK_SIZE, BLOCK_SIZE)
        enemy.move_squares(board)

        self.assertEqual(enemy.direction, "right")
        self.assertEqual(enemy.rect, expected_rect)

    def test_chasing(self):
        speed = 5
        pygame.display.set_mode((232, 228))
        # the enemy's name is Blinki so it chases the player from behind
        enemy = Enemy(FRAME_DIMS[0], FRAME_DIMS[1], speed, "Blinki")
        enemies = pygame.sprite.Group()
        enemies.add(enemy)
        # the player's top is located 7 pixels below and 3 pixel to right of the enemy
        # so it must take the enemy 3 steps to collide with the player
        player = Player(BLOCK_SIZE + 7 + FRAME_DIMS[0], 3 + BLOCK_SIZE + FRAME_DIMS[1], "pink", speed)
        board = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

        enemy.move(player, board)
        enemy.move(player, board)
        enemy.move(player, board)
        
        colliding = pygame.sprite.spritecollideany(player, enemies)
        self.assertIsNotNone(colliding)

if __name__ == '__main__':
    unittest.main()
