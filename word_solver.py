import numpy as np
from sanat import korjaa_csv

class WordHints:
    def __init__(self):
        self.characters="abcdefghijklmnopqrstuwvyzåäö"
        self.transform = dict(zip([i for  i in self.characters],[i for i in range(1,len(self.characters)+1)]))
        self.all_words = np.array([0, 0, 0, 0, 0])
        
        with open("vitoset.csv") as word_file:
            for word in word_file:
                word_np_array = self.transform_word_to_numpy_array(word.strip(";").strip("\n"))
                self.all_words = np.vstack([self.all_words, word_np_array])
        self.all_words = self.all_words[1:]
        self.possible_words = self.all_words

    def remove_non_possible_words(self, guess_word, correct_word, adjusted_table):
        print(guess_word)
        guess_array = self.transform_word_to_numpy_array(guess_word)
        correct_array = self.transform_word_to_numpy_array(correct_word)

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
        Returns the list of possible words when guess word is checked against given correct word.
        For example. Guess word rasti and correct word kaasu => all words with r filtered out.
        """
        self.possible_words = self.remove_non_possible_words(guess_word, correct_word, self.possible_words)

    def get_number_of_words_left_after_remove(self, guess_word, correct_word, words):
        adjusted_table = np.array([self.transform_word_to_numpy_array(word) for word in words])
        adjusted_table = self.remove_non_possible_words(guess_word, correct_word, adjusted_table)
        return adjusted_table.shape[0]


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
    



            
    

def main():
    WH = WordHints()
    WH.solve_possible_words("kaivo", 
                            "koira")
    
if __name__ == '__main__':
    main()
    