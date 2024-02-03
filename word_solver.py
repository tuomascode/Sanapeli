import numpy as np
from words import return_wordlist

class WordSimilarityEvaluator:
    def __init__(self, all_words):
        self.seen = set()
        self.all_words = all_words
        np.random.shuffle(self.all_words)
        self.processed_words = []

    def evaluate_similarity(self, a_word, b_word):
        score = len([a_word[i] for i in range(5) if a_word[i]==b_word[i]]) * 10
        score += len([a_word[i] for i in range(5) if a_word[i] in b_word]) * 10
        score += (5 - len(set([i for i in a_word])))*15
        return score
    
    def get_interesting_words(self):
        for word in self.all_words:
            if len(set([i for i in word])) == 5:
                self.processed_words.append(word)
                break
        for word in self.all_words:
            similarity_score = sum(self.evaluate_similarity(word, existing_word) for existing_word in self.processed_words) / len(self.processed_words)
            if similarity_score <= 13:
                self.processed_words.append(word)
        return self.processed_words
            
    
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
        self.characters="abcdefghijklmnopqrstuwvyzåäö"
        self.transform = dict(zip([i for  i in self.characters],[i for i in range(1,len(self.characters)+1)]))
        self.all_words = np.array([0, 0, 0, 0, 0])
        word_list = return_wordlist()
        for word in word_list:
            word_np_array = self.transform_word_to_numpy_array(word)
            self.all_words = np.vstack([self.all_words, word_np_array])
        self.all_words = self.all_words[1:]
        self.possible_words = self.all_words
        self.called = 0
        self.interesting_words = WordSimilarityEvaluator(self.all_words).get_interesting_words()

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

    def solve_possible_words(self, guess_word, correct_word):
        """
        Solves the list of possible words when guess word is checked against given correct word.
        For example. Guess word rasti and correct word kaasu => all words with r filtered out.
        """
        self.possible_words = self.remove_non_possible_words(guess_word, correct_word, self.possible_words)

    def get_number_of_words_left_after_remove(self, guess_word, correct_word, words):
        adjusted_table = np.array([self.transform_word_to_numpy_array(word) for word in words])
        adjusted_table = self.remove_non_possible_words(guess_word, correct_word, adjusted_table)
        return adjusted_table.shape[0]
    
    def reduce_interesting_words(self, guess_word, correct_word):
        from time import time
        begin = time()
        if isinstance(guess_word, str):
            guess_array = self.transform_word_to_numpy_array(guess_word)
            correct_array = self.transform_word_to_numpy_array(correct_word)
        else:
            guess_array = guess_word
            correct_array = correct_word
        interesting_words = []
        for word in self.interesting_words:
            for i in range(5):
                if guess_array[i] in word or correct_array[i] in word:
                    continue
                interesting_words.append(word)
        print(f'Time spent reducing words: {time()-begin:.2f}s')
        return interesting_words

    def solve_best_guess_words(self):
        list_of_possible_words = self.possible_words
        if len(list_of_possible_words) == 1:
            return [self.transform_np_array_to_word(list_of_possible_words[0])]
        
        np.random.shuffle(list_of_possible_words)
        scores = BestWorstHandler()
        index = 0
        for guess_word in list_of_possible_words:
            index +=1
            worst = 0
            for correct_word in list_of_possible_words:
                possibilies = self.get_number_of_words_left_for_guess_two(guess_word, correct_word, list_of_possible_words, scores.worst_worst_score)
                if possibilies > worst:
                    worst = possibilies
                if worst >= scores.worst_worst_score:
                    break
            scores.add_new_score(worst, self.transform_np_array_to_word(guess_word))
        return scores.get_best_guesses()

    def get_number_of_words_left_for_guess(self, guess_word, presumed_correct_word, list_of_possible_words):
        """
        Assume that presumed_correct_word is the right one. If you guess 'guess_word', what is the number of possible words left?
        """
        green_numbers = [guess_word[i] if guess_word[i] == presumed_correct_word[i] else 0 for i in range(5)]
        yellow_numbers = [guess_word[i] if guess_word[i] != presumed_correct_word[i] and guess_word[i] in presumed_correct_word else 0 for i in range(5)]
        black_numbers = [guess_word[i] for i in range(5) if guess_word[i] not in presumed_correct_word]
        possibilies = len(list_of_possible_words)
        for test_numbers in list_of_possible_words:
            if False in [green_numbers[i] == test_numbers[i] or green_numbers[i] == 0 for i in range(5)]:
                possibilies -= 1
                continue
            # if True in [black_number in test_numbers for black_number in black_numbers]:
            #     possibilies -= 1
            #     continue
            # if False in [yellow_numbers[i] == 0 or (yellow_numbers[i] in test_numbers and yellow_numbers[i] != test_numbers[i]) for i in range(5)]:
            #     possibilies -= 1
            #     continue
        return possibilies
    
    def get_number_of_words_left_for_guess_two(self, guess_word, presumed_correct_word, list_of_possible_words, worst_score):
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
    
    def get_number_of_words_left_for_guess_three(self, guess_word, presumed_correct_word, list_of_possible_words):
        green_numbers = [guess_word[i] if guess_word[i] == presumed_correct_word[i] else 0 for i in range(5)]
        yellow_numbers = [guess_word[i] if guess_word[i] != presumed_correct_word[i] and guess_word[i] in presumed_correct_word else 0 for i in range(5)]
        black_numbers = [guess_word[i] for i in range(5) if guess_word[i] not in presumed_correct_word]

        for index, number in enumerate(green_numbers):
            if number == 0:
                continue
            mask = ~(list_of_possible_words[:, index] != number)

        return 0

    def transform_word_to_numpy_array(self, word):
        return np.array([self.transform[i] for i in word])
    
    def transform_np_array_to_word(self, array):
        return "".join(self.characters[i - 1] for i in array)
    
    def get_non_shared_numbers(self, guess_array, correct_array):
        return sorted([i for i in guess_array if i not in correct_array])
    
    def remove_words_that_contain_numbers(self, non_shared_numbers, adjusted_table):
        for number in non_shared_numbers:
            adjusted_table = adjusted_table[~np.any(adjusted_table[:,] == number, axis=1)] 
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
    
    def remove_words_with_non_matching_numbers(self, non_matching_numbers, adjusted_table):
        for index, number in enumerate(non_matching_numbers):
            if number == 0:
                continue
            adjusted_table = adjusted_table[~(adjusted_table[:, index] == number)]
        return adjusted_table

    def get_possible_words_as_strings(self):
        return [self.transform_np_array_to_word(numbers) for numbers in self.possible_words]

    def get_interesting_words(self):
        interesting_words = []
        for word in self.all_words:
            if self.unique_letters_in_word(word):
                interesting_words.append(word)
        interesting_unique_words = []
        seen = set()
        for word in interesting_words:
            if self.transform_np_array_to_word(sorted(word)) not in seen:
                seen.add(self.transform_np_array_to_word(sorted(word)))
                interesting_unique_words.append(word)
        return interesting_words
    
    def unique_letters_in_word(self, word):
        return len(set([i for i in word])) == 5


def test():
    score = BestWorstHandler()
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
    score.add_new_score(2, "twoagain") == 2
    # score.report()
    word_pairs = [("ratki", "katki"), ("koira", "kaivo"), ("sihti", "puhti"),("kiila","hauki"), ("siima", "mahti")]
    for guess, correct in word_pairs:
        WH = WordHints()
        guess, correct = WH.transform_word_to_numpy_array(guess), WH.transform_word_to_numpy_array(correct)
        WH.solve_possible_words(guess, correct)
        WH = WordHints()
        possibilies = WH.get_number_of_words_left_for_guess(guess, correct, WH.all_words)
        pos_two = WH.get_number_of_words_left_for_guess_three(guess, correct, WH.all_words)
        print(possibilies, pos_two)
        assert possibilies == pos_two


def main():
    if True:
        test()
        exit()
    WH = WordHints()
    
if __name__ == '__main__':
    main()
    