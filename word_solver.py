import numpy as np
import json
import math
import time
from random import choices
from words import return_wordlist
from utils import solve_most_common_letters

class ColoredLetters:
    def __init__(self):
        self.found_letters = set()

    def add_letters(self, guess):
        for i in guess:
            self.found_letters.add(i)

    def is_seen(self, letter):
        return letter in self.found_letters


class BestWorstHandler:
    def __init__(self):
        self.top_ten = []
        self.full = False

    @property
    def worst_worst_score(self):
        if not self.full:
            return 300
        return max([i[0] for i in self.top_ten])

    def add_new_score(self, score, word):
        if not self.full and score < self.worst_worst_score:
            self.top_ten.append((score, word))
            if len(self.top_ten) == 10:
                self.full = True
            return
        max_value = self.worst_worst_score
        self.top_ten.sort(key=lambda x:x[0])
        if score < max_value:
            self.top_ten = self.top_ten[:9] + [(score, word)]
            return

    def report(self):
        with open("scores.txt", "w") as file:
            for score, word in self.top_ten:
                file.write(f"{word} {score}\n")

    def get_best_guesses(self):
        self.top_ten.sort(key=lambda x:x[0])
        return [i[1] for i in self.top_ten]


class WordHints:
    def __init__(self):
        self.characters = "abcdefghijklmnopqrstuwvyzåäö"
        self.common_letters = solve_most_common_letters()
        self.transform = dict(zip([i for  i in self.characters],[i for i in range(1,len(self.characters)+1)]))
        self.finnish_letters = self.transform_word_to_numpy_array(self.common_letters)
        self.all_words = self.transform_wordlist_to_numpy_array(return_wordlist())
        self.possible_words = self.all_words
        self.colored_letters = ColoredLetters()
        self.seen_sets = set()

    # MAIN FUNCTIONS #

    """
    Functions that other modules call. Everything else should be local.
    """

    def solve_possible_words(self, guess_word, correct_word):
        """
        Solves the list of possible words when guess word is checked against given correct word.
        For example. Guess word rasti and correct word kaasu => all words with r filtered out.
        Also keeps track of seen letters.
        """
        self.possible_words = self.remove_non_possible_words(guess_word, correct_word, self.possible_words)
        self.colored_letters.add_letters(self.transform_word_to_numpy_array(guess_word))

    def solve_clues(self):
        """
        Solve hint words using math and magic
        """
        self.seen_sets = set()
        base_probability = 1 / len(self.possible_words)
        if base_probability >= 1/2:
            return self.get_possible_words_as_string()

        if len(self.possible_words)<10:
            return self.rank_guesses_by_worst_outcome(self.all_words)

        solved_guess_letters = self.recursive_guess_letter_solve([], self.all_words)[1]
        guesses = self.get_guess_words_that_have_letters(solved_guess_letters)
        return self.rank_guesses_by_worst_outcome(guesses)

    # HELPER FUNCTIONS #

    def transform_wordlist_to_numpy_array(self, wordlist):
        all_words = np.array([0, 0, 0, 0, 0])
        for word in wordlist:
            word_np_array = self.transform_word_to_numpy_array(word)
            all_words = np.vstack([all_words, word_np_array])
        return all_words[0:]

    def transform_word_to_numpy_array(self, word):
        return np.array([self.transform[i] for i in word])
    
    def transform_np_array_to_word(self, array):
        return "".join(self.characters[i - 1] for i in array)

    def remove_non_possible_words(self, guess_word, correct_word, adjusted_table):
        if isinstance(guess_word, str):
            guess_array = self.transform_word_to_numpy_array(guess_word)
            correct_array = self.transform_word_to_numpy_array(correct_word)
        else:
            guess_array = guess_word
            correct_array = correct_word

        numbers_in_correct_position = [guess_array[i] if guess_array[i] == correct_array[i] else 0 for i in range(5)]
        adjusted_table = self.get_words_that_have_number_in_specific_position(numbers_in_correct_position, adjusted_table)

        non_shared_numbers = self.get_non_shared_numbers(guess_array, correct_array)
        adjusted_table = self.remove_words_that_contain_numbers(non_shared_numbers, adjusted_table)

        shared_non_correct_pos_numbers = [guess_array[i] for i in range(5) if (guess_array[i] in correct_array and guess_array[i]!=correct_array[i])]
        adjusted_table = self.get_words_that_contain_numbers(shared_non_correct_pos_numbers, adjusted_table)

        non_matching_numbers = [guess_array[i] if (guess_array[i] != correct_array[i]) else 0 for i in range(5)]
        adjusted_table = self.remove_words_with_non_matching_numbers(non_matching_numbers, adjusted_table)
        return adjusted_table

    def get_words_that_have_number_in_specific_position(self, numbers_in_correct_position, adjusted_table):
        for index, number in enumerate(numbers_in_correct_position):
            if number == 0:
                continue
            adjusted_table = adjusted_table[~(adjusted_table[:, index] != number)]
        return adjusted_table
    
    def get_words_that_contain_numbers(self, shared_numbers, adjusted_table):
        for number in shared_numbers:
            adjusted_table = adjusted_table[np.any(adjusted_table[:,] == number, axis=1)] 
        return adjusted_table
    
    def get_non_shared_numbers(self, guess_array, correct_array):
        return sorted([i for i in guess_array if i not in correct_array])
    
    def get_guess_words_that_have_letters(self, letters):
        words = self.all_words
        for letter in letters:
            words = self.get_words_that_contain(letter, words)
        return words
    
    def get_words_that_contain(self, letter, word_list):
        word_list = word_list[np.any(word_list[:,] == letter, axis=1)] 
        return word_list
    
    def get_words_that_dont_contain(self, letter, word_list):
        word_list = word_list[~np.any(word_list[:,] == letter, axis=1)] 
        return word_list

    def remove_words_that_contain_numbers(self, non_shared_numbers, adjusted_table):
        for number in non_shared_numbers:
            adjusted_table = adjusted_table[~np.any(adjusted_table[:,] == number, axis=1)] 
        return adjusted_table
    
    def remove_words_with_non_matching_numbers(self, non_matching_numbers, adjusted_table):
        for index, number in enumerate(non_matching_numbers):
            if number == 0:
                continue
            adjusted_table = adjusted_table[~(adjusted_table[:, index] == number)]
        return adjusted_table

    def solve_largest_word_group(self, letters):
        """
        Ask, what is the largest group of words, when
        dividing all possible words to all possible subgroups with letters.
        """
        all_words = self.possible_words.copy()
        lists = [all_words]
        for letter in letters:
            new_lists = []
            for word_list in lists:
                new_lists.append(self.get_words_that_contain(letter, word_list))
                new_lists.append(self.get_words_that_dont_contain(letter, word_list))
            lists = new_lists
        largest_seen_group = 0
        for word_list in lists:
            if len(word_list) > largest_seen_group:
                largest_seen_group = len(word_list)
        return largest_seen_group
       
    def rank_guesses_by_worst_outcome(self, words_to_be_checked):
        scores = BestWorstHandler()
        for guess_word in words_to_be_checked:
            worst = 0
            for correct_word in self.possible_words:
                possibilies = self.get_number_of_words_left_for_guess(guess_word, correct_word, self.possible_words, scores.worst_worst_score)
                if possibilies > worst:
                    worst = possibilies
                if worst >= scores.worst_worst_score:
                    break
            scores.add_new_score(worst, self.transform_np_array_to_word(guess_word))
        return scores.get_best_guesses()

    def recursive_guess_letter_solve(self, letters:list, guess_words:list):
        """
        This slightly complicated recursive function looks to solve which letters
        divide the possible words most effectively.
        
        F.e. words "car", "rack", "track", "croak".
        The letter "a" would be bad, since all words have "a".
        The letter "k" would produce groups ["car"] and ["rack", "track", "croak"]  => sizes 1 and 3.
        Letters "t" and "o" would produce groups => ["car", "rack"],["track"],["croak"], meaning sizes 2, 1, 1
        This recursive function looks for division with the largest word group being as small as possible.
        """
        if len(letters) == 5 or len(guess_words) == 1:
            return self.solve_largest_word_group(letters), letters

        smallest_largest_seen = float('inf')
        if len(letters) > 0:
            smallest_largest_seen = self.solve_largest_word_group(letters)

        best_letters = letters
        for letter in self.finnish_letters:
            if letter in letters or self.colored_letters.is_seen(letter):
                continue
            temp = letters.copy()
            temp.append(letter)
            check_string = self.transform_np_array_to_word(sorted(temp))
            if check_string in self.seen_sets:
                continue
            self.seen_sets.add(check_string)
            temp_guesses = guess_words.copy()
            temp_guesses = self.get_words_that_contain(letter, temp_guesses)
            if len(temp_guesses) == 0:
                continue
            result_largest, result_letters = self.recursive_guess_letter_solve(temp, temp_guesses)
            if result_largest < smallest_largest_seen:
                smallest_largest_seen = result_largest
                best_letters = result_letters
        return smallest_largest_seen, best_letters

    def get_number_of_words_left_for_guess(self, guess_word, presumed_correct_word, list_of_possible_words, worst_score):
        """
        Assume that presumed_correct_word is the right one. If you guess 'guess_word', what is the number of possible words left?
        """
        green_numbers = [guess_word[i] if guess_word[i] == presumed_correct_word[i] else 0 for i in range(5)]
        yellow_numbers = [guess_word[i] if guess_word[i] != presumed_correct_word[i] and guess_word[i] in presumed_correct_word else 0 for i in range(5)]
        black_numbers = [guess_word[i] for i in range(5) if guess_word[i] not in presumed_correct_word]
        possibilies = 0
        for test_numbers in list_of_possible_words:
            # does green numbers exclude this guy. If so, then don't count it. If not, then this guy would be left
            if False in [green_numbers[i] == test_numbers[i] or green_numbers[i] == 0 for i in range(5)]:
                continue
            if True in [black_number in test_numbers for black_number in black_numbers]:
                continue
            if False in [yellow_numbers[i] == 0 or (yellow_numbers[i] in test_numbers and yellow_numbers[i] != test_numbers[i]) for i in range(5)]:
                continue
            possibilies += 1
            if possibilies >= worst_score:
                return worst_score + 5
        return possibilies

    def get_possible_words_as_string(self):
        return [self.transform_np_array_to_word(i) for i in self.possible_words]


def main():
    raise NotImplementedError("No main function implemented for file")


if __name__ == '__main__':
    main()
    