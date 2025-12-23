import unittest
import os
import pygame
from modes.single_player_game import SinglePlayerGame
from test_level import make_mock_level

class TestGame(unittest.TestCase):
    def test_writing_scores(self):
        game = make_mock_game()
        mock_scores_path = os.path.join("assets", "mock_scores.txt")

        small_score = 8
        big_score = 1000000
        not_bad_score = 500

        # for this test to pass the scores in mock_scores.txt should be at least 10
        self.assertFalse(game.is_in_top_10_scores(small_score, mock_scores_path))

        self.assertTrue(game.is_in_top_10_scores(big_score, mock_scores_path))
        self.assertTrue(game.is_in_top_10_scores(not_bad_score, mock_scores_path))

    def test_writing_scores(self):
        game = make_mock_game()
        mock_scores_path = os.path.join("assets", "mock_scores.txt")

        big_score = 1000000
        not_bad_score = 500

        game.write_in_scores("player1", 1000000, mock_scores_path)
        game.write_in_scores("player2", not_bad_score, mock_scores_path)

        with open(mock_scores_path) as f:
            scores = f.readlines()
        scores = [score.strip() for score in scores]

        self.assertTrue(len(scores) == 10)
        self.assertEqual(f"player1 : {big_score}", scores[0])
        self.assertTrue(f"player2 : {not_bad_score}" in scores)
    
def make_mock_game():
    level = make_mock_level()
    screen = pygame.display.set_mode((100, 100))
    game = SinglePlayerGame([level], screen)

    return game

if __name__ == '__main__':
    unittest.main()