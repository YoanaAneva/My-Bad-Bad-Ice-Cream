import unittest
import pygame
from entities.fruit import Fruit
from entities.enemy import Enemy
from game.level import Level
from game.board_maps import mock_board_stage1, mock_board_stage2, mock_board_stage1_no_fruit, mock_board_updated

class TestLevel(unittest.TestCase):
    def test_initialization(self):
        level = make_mock_level()

        self.assertEqual(level.stage, 0)
        self.assertEqual(level.board, level.stage_boards[0])
        self.assertEqual(level.fruit.sprites(), [])
        self.assertEqual(level.ice_cubes, [])
        self.assertEqual(level.is_over, False)
        self.assertEqual(level.is_locked, True)

    def test_updating_groups(self):
        level = make_mock_level()

        # the first board contains 4 fruits and 8 ice cubes
        expected_num_of_fruits = 4
        expected_num_of_ice_cubes = 8

        # at the beginning the level's group of fruit and list of ice is empty
        # when the update_groups functions is called the lists are filled/updated 
        level.update_groups()

        self.assertEqual(len(level.fruit.sprites()), expected_num_of_fruits)
        self.assertEqual(len(level.ice_cubes), expected_num_of_ice_cubes)

    def test_updating_board(self):
        level = make_mock_level()

        # is ice on the current board
        self.assertEqual(level.board[1][1], 1)

        level.update_board(mock_board_stage2)

        # the board must have frozen fruit number now because the 
        # new board has a fruit at this cell
        self.assertEqual(level.board[1][1], 2)

    def test_updating_stage(self):
        level = make_mock_level()
        expected_board = mock_board_updated
        # the level stage should go from 0 to 1
        expected_stage = 1
        # imitating that all the fruit has been eaten
        level.board = mock_board_stage1_no_fruit
        
        level.update_stage()

        self.assertEqual(level.board, expected_board)
        self.assertEqual(level.stage, expected_stage)

    def test_resetting(self):
        level = make_mock_level()
        # making some changes over the level
        change_level(level)
        
        level.reset()

        self.assertFalse(level.is_over)
        self.assertEqual(level.board, level.stage_boards[0])
        self.assertEqual(level.stage, 0)
        self.assertEqual(level.fruit.sprites(), [])
        self.assertEqual(level.ice_cubes, [])
        self.assertFalse(level.enemies.sprites()[0].is_dead)


def make_mock_level():
    pygame.display.set_mode((232, 228))
    enemy = Enemy(0, 0, 0)
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)
    boards = [mock_board_stage1, mock_board_stage2]
    level = Level(boards, ["banana", "watermelon"], enemy_group, (0, 0))
    return level

def change_level(level):
    level.board = mock_board_stage1_no_fruit
    level.stage = 2        
    new_fruit = Fruit("banana", 10, 10)
    level.fruit.add(new_fruit)
    level.enemies.sprites()[0].is_dead = True

if __name__ == '__main__':
    unittest.main()