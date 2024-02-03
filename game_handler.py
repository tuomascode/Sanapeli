from random import choice
from words import return_wordlist
from word_solver import WordHints


class GameHandler:
    def __init__(self):
        self.solver = WordHints()
        hints = ["kasti", "taksi", "ratki", "kausi", "kilta", "kitua", "kiusa", "rasti", "silta", "raksi"]
        hints = ["litra", "kasti", "taksi", "liuta", "kitua", "ratki", "lasti", "oikea", "lista", "rasti"]
        self.letters = [["" for i in range(5)] for j in range(5)]
        self.clues = [hint.upper() for hint in hints]
        self.possible_words_left = []
        self.all_words_list = return_wordlist()
        self.correct_word = choice(self.all_words_list)
        self.cursor_index = 0
        self.game_row = 0
        self.losing = False
        self.winning = False
        self.word_in_dictionary = True
        self.interesting_solve_words = ["palte","nyreä","kyylä","neppi","safka","saada","paali",]
        self.colour_map = {"black":[],"yellow":[],"green":[]}

    def move_cursor_right(self):
        if self.cursor_index<4:
            self.cursor_index+=1

    def move_cursor_left(self):
        if self.cursor_index>0:
            self.cursor_index-=1

    ### GET_ATTR_FUNCTIONS ###
    
    def reset_game_with_same_solution(self):
        correct_word = self.correct_word
        new_game = GameHandler()
        self.__dict__.update(new_game.__dict__)
        self.correct_word = correct_word
        return "continue"

    def reset_game(self):
        new_game = GameHandler()
        self.__dict__.update(new_game.__dict__)
        return "continue"
    
    def remove_letter(self):
        self.word_in_dictionary = True
        last_letter = self.cursor_index == 4 and self.last_letter_is_filled
        self.letters[self.game_row][self.cursor_index] = ""
        if not last_letter:
            self.move_cursor_left()
            self.letters[self.game_row][self.cursor_index] = ""

    def type_a_letter(self, letter):
        self.letters[self.game_row][self.cursor_index] = letter
        self.move_cursor_right()

    def check_answer(self):
        print("checking guess:", self.guess_word, "with row", self.game_row)
        self.word_in_dictionary = False
        if self.guess_word in self.all_words_list:
            self.word_in_dictionary = True
            return "play_row"
        return "continue"
    
    def play_row(self):
        print("Playing row with guess:", self.guess_word)
        self.update_colour_map()
        self.cursor_index = 0
        self.solver.solve_possible_words(self.guess_word, self.correct_word)
        self.clues = self.solver.solve_best_guess_words()
        self.clues = [i.upper() for i in self.clues]
        self.winning = False not in [self.guess_word[i] == self.correct_word[i] for i in range(5)]
        self.game_row += 1
        if not self.winning and self.game_row == 5:
            self.losing=True

    def quit(self):
        exit()

    ### UTILITY AND PROPERTY FUNCS ####

    def get_game_state(self):
        """
        Returns a dict:
        {
        winning = self.game_state["winning"]
        losing = self.game_state["losing"]
        game_row = self.game_state["game_row"]
        cursor_index = self.game_state["cursor_index"]
        word_in_dictionary = self.game_state["word_in_dictionary"]
        all_letters_typed = self.game_state["all_letters_typed"]
        correct_word = self.game_state["correct_word"]
        guess_word = self.game_state["guess_word"]
        }
        """
        game_states_to_fetched = [  "winning",
                                    "losing",
                                    "game_row",
                                    "cursor_index",
                                    "word_in_dictionary",
                                    "all_letters_typed",
                                    "correct_word",
                                    "clues",
                                    "letters",
                                    "colour_map"]
        game_state = dict()
        for state_parameter in game_states_to_fetched:
            game_state[state_parameter] = getattr(self, state_parameter)
        game_state["guess_word"] = "".join(self.letters[self.game_row - 1])
        return game_state

    def update_colour_map(self):
        self.colour_map["black"] = [letter for letter in self.guess_word]
        self.colour_map["yellow"] = [self.guess_word[i] for i in range(5) if self.guess_word[i] in self.correct_word and self.guess_word[i] != self.correct_word[i]]
        self.colour_map["green"] = [self.guess_word[i] for i in range(5) if self.guess_word[i] == self.correct_word[i]]

    @property
    def guess_word(self):
        if self.game_row > 4:
            return "".join(self.letters[4])
        return "".join(self.letters[self.game_row])
    
    @property
    def last_letter_is_filled(self):
        return self.letters[self.game_row][self.cursor_index] != ""

    @property
    def all_letters_typed(self):
        return len(self.guess_word) == 5

