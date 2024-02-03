import unittest
import numpy as np
import word_solver  # Import the module you want to test
import game_handler
import inputs
import drawer

class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        self.gh = game_handler.GameHandler()

    def test_simle_winning_game(self):
        self.gh.correct_word = "lista"
        self.gh.type_a_letter("l")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("i")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("s")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("t")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("a")
        assert "play_row" == self.gh.check_answer()
        assert self.gh.word_in_dictionary
        self.gh.play_row()
        assert self.gh.winning

    def test_losing_game(self):
        self.gh.correct_word = "lista"
        self.gh.type_a_letter("l")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("i")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("s")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("t")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("i")
        assert "continue" == self.gh.check_answer()
        assert not self.gh.word_in_dictionary

    def test_backspace(self):
        self.gh.type_a_letter("a")
        self.gh.type_a_letter("a")
        self.gh.type_a_letter("a")
        self.gh.type_a_letter("a")
        self.gh.type_a_letter("a")
        assert "continue" == self.gh.check_answer()
        assert not self.gh.word_in_dictionary
        self.gh.remove_letter()
        assert self.gh.guess_word == "aaaa"
        self.gh.remove_letter()
        assert self.gh.guess_word == "aaa"
        self.gh.remove_letter()
        assert self.gh.guess_word == "aa"
        self.gh.remove_letter()
        assert self.gh.guess_word == "a"
        self.gh.remove_letter()
        assert self.gh.guess_word == ""
        self.gh.remove_letter()
        assert self.gh.guess_word == ""

    def test_two_phase_win(self):
        self.gh.correct_word = "lista"
        self.gh.type_a_letter("k")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("i")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("i")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("m")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("a")
        assert "play_row" == self.gh.check_answer()
        assert self.gh.word_in_dictionary
        self.gh.play_row()
        assert not self.gh.winning
        self.gh.type_a_letter("l")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("i")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("s")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("t")
        assert "continue" == self.gh.check_answer()
        self.gh.type_a_letter("a")
        assert "play_row" == self.gh.check_answer()
        assert self.gh.word_in_dictionary
        self.gh.play_row()
        assert self.gh.winning
        
    def test_lose(self):
        self.gh.correct_word = "maila"
        bad_word = "lista"
        for i in range(5):
            for letter in bad_word:
                self.gh.type_a_letter(letter)
                if letter != "a":
                    assert "continue" == self.gh.check_answer()
                    assert not self.gh.word_in_dictionary
                else:
                    assert "play_row" == self.gh.check_answer()
                    assert self.gh.word_in_dictionary
                    self.gh.play_row()
                    assert not self.gh.winning
        assert self.gh.losing

    def test_reset(self):
        self.gh.correct_word = "maila"
        bad_word = "lista"
        for i in range(5):
            for letter in bad_word:
                self.gh.type_a_letter(letter)
                if letter != "a":
                    assert "continue" == self.gh.check_answer()
                    assert not self.gh.word_in_dictionary
                else:
                    assert "play_row" == self.gh.check_answer()
                    assert self.gh.word_in_dictionary
                    self.gh.play_row()
                    assert not self.gh.winning
        assert self.gh.losing
        self.gh.reset_game_with_same_solution()
        assert self.gh.correct_word == "maila"
        from random import seed
        seed(0)
        self.gh.reset_game()
        assert self.gh.correct_word != "maila"

    def test_get_game_state(self):
        self.gh.correct_word = "maila"
        bad_word = "lista"
        for i in range(5):
            assert self.gh.get_game_state()["game_row"] == i
            for letter in bad_word:
                self.gh.type_a_letter(letter)
                if letter != "a":
                    assert "continue" == self.gh.check_answer()
                    assert not self.gh.word_in_dictionary
                    assert not self.gh.all_letters_typed
                else:
                    assert self.gh.all_letters_typed
                    assert "play_row" == self.gh.check_answer()
                    assert self.gh.word_in_dictionary
                    self.gh.play_row()
                    assert not self.gh.winning
        assert self.gh.losing
        game_state = self.gh.get_game_state()
        assert game_state["losing"]
        assert not game_state["winning"]
        assert len(game_state["colour_map"]) == 3
        assert isinstance( game_state["colour_map"], dict)
        assert game_state["letters"] == [list("lista")] * 5


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


def test_all():
    unittest.main()

if __name__ == '__main__':
    test_all()