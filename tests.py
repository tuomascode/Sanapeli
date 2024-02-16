import unittest
from random import choice
import time
import numpy as np
import word_solver  # Import the module you want to test
import game_handler
import words


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

    def test_clue_solve_one(self):
        interesting_solve_words = ["neppi","safka","saada"]
        for correct_word in interesting_solve_words:
            self.WH = word_solver.WordHints()
            guess = "litra"
            self.WH.solve_possible_words(guess, correct_word)
            clue_words = self.WH.solve_clues()
            self.WH.solve_possible_words(clue_words[0], correct_word)
    
    def test_best_worst(self):
        score = word_solver.BestWorstHandler()
        assert score.worst_worst_score == 300
        score.add_new_score(1, "one")
        assert score.worst_worst_score == 300
        score.add_new_score(2, "two")
        assert score.worst_worst_score == 300
        score.add_new_score(3, "three")
        assert score.worst_worst_score == 300
        score.add_new_score(4, "four")
        assert score.worst_worst_score == 300
        score.add_new_score(5, "five")
        assert score.worst_worst_score == 300
        score.add_new_score(6, "six")
        assert score.worst_worst_score == 300
        score.add_new_score(7, "seven")
        assert score.worst_worst_score == 300
        score.add_new_score(8, "eight")
        assert score.worst_worst_score == 300
        score.add_new_score(9, "nine")
        assert score.worst_worst_score == 300
        score.add_new_score(10, "ten")
        assert score.worst_worst_score == 10
        score.add_new_score(11, "eleven")
        assert score.worst_worst_score == 10
        score.add_new_score(12, "twelve")
        assert score.worst_worst_score == 10
        score.add_new_score(2, "twoagain")
        assert score.worst_worst_score == 9

class TestSolverWithGame(unittest.TestCase):

    def setUp(self) -> None:
        # Option for limited testing. Set False to test all finnish words
        self.test_limited = True

        # Option to fail if solve_clues takes too long
        self.test_time = False
        self.allowed_time = 0

    def test_solver(self):
        """
        Full solve_clues algorithm and also game functionality test.
        """
        self.max_time_spent = 0
        np.random.seed(0)
        test_words = words.return_wordlist()
        if self.test_limited:
            test_words = [choice(test_words) for i in range(10)]

        def type_word_and_play_row(word, GH:'game_handler.GameHandler'):
            for letter in word:
                GH.type_a_letter(letter)
            assert "play_row" == GH.check_answer()
            GH.play_row()

        def check_for_win(GH:'game_handler.GameHandler', start_time):
            if GH.winning:
                time_spent = start_time - time.time()
                if time_spent > self.max_time_spent:
                    self.max_time_spent = time_spent
                return True
            return False

        for word in test_words:
            start = time.time()
            guess = "litra"
            guesses = [guess]
            WH = word_solver.WordHints()
            GH = game_handler.GameHandler(word)
            type_word_and_play_row(guess, GH)
            if check_for_win(GH, start):
                continue
            for _ in range(4):
                WH.solve_possible_words(guess, GH.correct_word)
                guess = WH.solve_clues()[0]
                guesses.append(guess)
                type_word_and_play_row(guess, GH)
                if check_for_win(GH, start):
                    break
            if GH.losing:
                self.fail(f"solve algorithm failed.\n"
                          f"Guesses: {guesses}\n"
                          f"Correct word: {word}")
            end = time.time()
            if end-start > self.max_time_spent:
                self.max_time_spent = end -start
        if self.test_time and self.allowed_time < self.max_time_spent:
            self.fail(f"Algorithm took too long:{self.max_time_spent}")    
        

if __name__ == '__main__':
    unittest.main()