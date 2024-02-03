import pygame

class GameDrawer:
    def __init__(self, show_clues = False):
        """
        Responsible for everything that is drawed to screen
        """
        pygame.init()
        if show_clues:
            self.screen = pygame.display.set_mode((565, 700))
        else:
            self.screen = pygame.display.set_mode((400, 700))
        self.letter_handler = GuessWords()
        self.guess_box_handler_word = GuessWordBoxes()
        self.keyboard = Keyboard()
        self.x = 40
        self.y = 650
        self.game_state = dict()
        self.show_clues = show_clues

    def reset(self):
        self.letter_handler = GuessWords()
        self.guess_box_handler_word = GuessWordBoxes()
        self.keyboard = Keyboard()
        self.game_state = dict()

    def draw(self):
        self.draw_basics()
        self.draw_game_state()
        self.draw_boxes()
        self.draw_hint_box(self.game_state["clues"])
        self.letter_handler.draw_letters(self.screen, self.game_state["letters"])
        self.keyboard.draw_buttons(self.screen)
        pygame.display.flip()

    def draw_basics(self):
        self.screen.fill((150, 150, 150))
        pygame.draw.rect(self.screen, (80,80,80), ((self.x - 3, self.y - 3), (136,44)))
        pygame.draw.rect(self.screen,(200,200,200), ((self.x, self.y), (130, 38)))
        self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Vihjeet (§)", True, (20,20,20)), (self.x+5, self.y+5))

    def draw_hint_box(self, clues):
        self.screen.blit(pygame.font.SysFont("Georgia", 40).render("Vihjeet:", True, (20, 20, 20)), (400, 50))
        for index in range(len(clues)):
            self.screen.blit(pygame.font.SysFont("Georgia", 28).render(f"{index+1}. {clues[index]}",True,(20,20,20)),(415,150+index*40))

    def draw_game_state(self):
        winning = self.game_state["winning"]
        losing = self.game_state["losing"]
        game_row = self.game_state["game_row"]
        cursor_index = self.game_state["cursor_index"]
        word_in_dictionary = self.game_state["word_in_dictionary"]
        all_letters_typed = self.game_state["all_letters_typed"]
        correct_word = self.game_state["correct_word"]
        if not winning:
            if game_row != 5:
                pointer = pointteri((45 + (cursor_index * 60), 45 + (game_row*60), 60, 60))
                pygame.draw.rect(self.screen, pointer.vari, pointer.posko)
                del pointer
            if not word_in_dictionary and all_letters_typed:
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Sanaa ei löytynyt",True,(20,20,20)),(50,350))
            elif losing == True:
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Hävisit pelin, oikea sana oli:",True,(20,20,20)),(50,350))
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render(correct_word, True, (20, 20, 20)), (50, 380))
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Paina enter pelataksesi uudestaan", True, (20, 20, 20)), (50, 410))
        else:
            self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Voitit pelin!",True, (20, 20, 20)), (50, 350))
            self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Paina enteriä pelataksesi uudestaan!", True, (20, 20, 20)), (50, 380))

    def draw_boxes(self):
        self.guess_box_handler_word.draw(self.screen)

    def update_guess_related_values(self, game_state):
        self.update_input_related_values(game_state)
        self.colour_guess_boxes_black()
        self.colour_partially_matching_guess_boxes_yellow()
        self.colour_matching_guess_boxes_green()
        self.keyboard.colour_keys_with_colourmap(game_state["colour_map"])

    def update_input_related_values(self, game_state):
        self.game_state = game_state
        
    def colour_guess_boxes_black(self):
        game_row = self.game_state["game_row"] - 1
        for i in range(5):
            self.guess_box_handler_word.colour_box_with_colour(game_row, i, "black")

    def colour_matching_guess_boxes_green(self):
        guess_word = self.game_state["guess_word"]
        correct_word = self.game_state["correct_word"]
        game_row = self.game_state["game_row"] - 1
        for i in range(len(guess_word)):
            if guess_word[i] == correct_word[i]:
                self.guess_box_handler_word.colour_box_with_colour(game_row, i, "green")

    def colour_partially_matching_guess_boxes_yellow(self):
        guess_word = self.game_state["guess_word"]
        correct_word = self.game_state["correct_word"]
        game_row = self.game_state["game_row"] - 1
        remaining_letters = [correct_word[i] for i in range(5) if correct_word[i] in guess_word and correct_word[i] != guess_word[i]]
        for remaining_letter in remaining_letters:
            for index in range(5):
                if guess_word[index] == remaining_letter and not self.guess_box_handler_word.get_box_row(game_row)[index].is_green:
                    self.guess_box_handler_word.colour_box_with_colour(game_row, index, "yellow")
                    break

    def open_or_close_hint_window(self):
        if self.show_clues:
            self.show_clues = False
        else:
            self.show_clues = True
        self.toggle_hint_window()

    def toggle_hint_window(self):
        if self.show_clues:
            self.screen = pygame.display.set_mode((565, 700))
        else:
            self.screen = pygame.display.set_mode((400, 700))

class GuessWords:
    def __init__(self):
        """
        This Class is responsible for drawing guessed letters.
        """
        self.letter_drawers = [[LetterDrawer((50+(j*60)+8, 50+(i*60)+3)) for j in range(5)] for i in range(5)]

    def draw_letters(self, screen, letters):
        """
        Arguments:
        - screen object to be drawn to.
        - 5x5 matrix of characters which are drawn. Empty chars are not drawn
        """
        for row in range(5):
            for column in range(5):
                letter = letters[row][column]
                if letter != "":
                    self.letter_drawers[row][column].draw_letter(letter, screen)

    def last_letter_is_filled(self, row, column):
        return self.letters[row][column] != ""

class LetterDrawer:
    def __init__(self, position):
        """
        Holds the position of the letter and draws the letter
        """
        self.position = position
        self.font = pygame.font.SysFont("Georgia", 40)

    def draw_letter(self, new_letter, screen):
        text = self.font.render(new_letter.upper(), True, (20, 20, 20))
        screen.blit(text, self.position)

class Keyboard:
    def __init__(self) -> None:
        first_row = "qwertyuiop".upper()
        second_row = "asdfghjklöä".upper()
        third_row = "zxcvbnm".upper()
        self.letters = []
        for i in range(len(first_row)):
            self.letters.append(KeyboardKey((22+i*36, 440), first_row[i]))
        for i in range(len(second_row)):
            self.letters.append(KeyboardKey((5+i*36, 480), second_row[i]))
        for i in range(len(third_row)):
            self.letters.append(KeyboardKey((72+i*36, 520), third_row[i]))

    def draw_buttons(self,  screen):
        for letter_button in self.letters:
            letter_button.draw_box_and_letter(screen)

    def colour_keys_with_colourmap(self, colour_map:dict):
        for colour, letters in colour_map.items():
            self.colour_all_keys_with(colour, letters)

    def colour_all_keys_with(self, colour, colourmap_letters):
        for letter in self.letters:
            if letter.letter.lower() in colourmap_letters: 
                letter.update_colour(colour)


class KeyboardKey:
    def __init__(self, position, letter):
        self.colours = {
            "neutral" : (120, 120, 120),
            "green" : (180,255,190),
            "yellow" : (255, 255, 51),
            "black" : (100, 100, 100)
        }
        self.color_comparison = {
            "neutral" : 0,
            "black" : 1,
            "yellow" : 2,
            "green" : 3

        }
        self.position = position
        self.size = (33, 33)
        self.letter = letter
        self.colour = self.colours["neutral"]
        self.colour_name = "neutral"
        self.text_position = (position[0] + 8, position[1] + 3)

    def update_colour(self, colour):
        if self.takes_precedent(colour):
            self.colour = self.colours[colour]
            self.colour_name = colour

    def draw_box_and_letter(self, screen):
        pygame.draw.rect(screen, self.colour, (self.position, self.size))
        text = pygame.font.SysFont("Georgia", 25).render(self.letter, True, (20, 20, 20))
        screen.blit(text, self.text_position)

    def takes_precedent(self, incoming_colour):
        old_colour = self.colour_name
        if self.color_comparison[incoming_colour] > self.color_comparison[old_colour]:
            return True
        return False


class GuessWordBoxes:
    def __init__(self):
        self.laatikot = []
        for i in range(5):
            self.laatikot.append([])
            for j in range(5):
                self.laatikot[i].append(WordBox((50+(j*60), 50+(i*60),50,50)))

    def draw(self, screen):
        for i in self.laatikot:
            for j in i:
                pygame.draw.rect(screen, j.vari, j.posko)

    def colour_box_with_colour(self, row, index, colour):
        box = self.laatikot[row][index]
        box.update_colour(colour)

    def get_box_row(self, row):
        return self.laatikot[row]

class WordBox:
    def __init__(self, positiokoko):
        self.colours = {
            "neutral" : (80, 80, 80),
            "green" : (180,255,190),
            "yellow" : (255, 255, 51),
            "black" : (100, 100, 100)
        }
        self.vari = self.colours["neutral"]
        self.posko = positiokoko
        self.is_green = False
    
    def update_colour(self, new_colour):
        self.vari = self.colours[new_colour]
        if new_colour == "green":
            self.is_green = True


class pointteri:
    def __init__(self,positiokoko):
        self.vari=(240,240,240)
        self.posko=positiokoko
