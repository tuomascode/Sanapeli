import unittest
import numpy as np
import word_solver  # Import the module you want to test
import main
import game_handler
import inputs
import drawer

class TestGameFunctions(unittest.TestCase):
    def setup(self):
        self.gh = game_handler.GameHandler()

    def testBackspace(self):
        pass
    
    def test_non_dict_word_rejected(self):
        pass


class TestWordSolver(unittest.TestCase):
    def setUp(self):
        self.WH = word_solver.WordHints()

    def tearDown(self):
        pass

    def test_function1(self):
        self.assertEqual(self.WH.transform_np_array_to_word(np.array([1,1,1,1,1])), "aaaaa")

    def test_non_shared(self):
        guess = [1, 2, 3, 4, 5]
        correct = [1, 2, 3, 4, 6]
        non_shared = [5]
        self.assertEqual(self.WH.get_non_shared_numbers(guess, correct), non_shared)
        guess = [1, 7, 3, 4, 5]
        correct = [1, 2, 3, 4, 6]
        non_shared = [5, 7]
        self.assertEqual(self.WH.get_non_shared_numbers(guess, correct), non_shared)
        guess = [1, 7, 3, 4, 5]
        correct = [1, 2, 5, 4, 6]
        non_shared = [3, 7]
        self.assertEqual(self.WH.get_non_shared_numbers(guess, correct), non_shared)


if __name__ == '__main__':
    unittest.main()