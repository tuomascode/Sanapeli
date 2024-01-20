import pygame
from random import choice
from sanat import palauta_tulos, return_wordlist
from word_solver import WordHints

class GuessWords:
    def __init__(self):
        self.letters = [[Kirjain((50+(j*60)+8, 50+(i*60)+3)) for j in range(5)] for i in range(5)]
    
    def add_letter_to_index(self, row, index, letter):
        self.letters[row][index].lisaa_kirjain(letter)

    def get_row_word(self, row):
        return "".join(self.letters[row][i].kirjain for i in range(5))
    
    def get_letter(self, row, index):
        return self.letters[row][index]

    def draw_letters(self, screen):
        for word in self.letters:
            for letter in word:
                if letter.on:
                    screen.blit(letter.teksti, letter.paikka)

class Kirjain:
    def __init__(self,positio):
        self.on=False
        self.kirjain=""

        self.fontti = pygame.font.SysFont("Georgia", 40)
        self.teksti = self.fontti.render(self.kirjain, True, (20, 20, 20))
        self.paikka=positio

    def lisaa_kirjain(self,kirjain):
        self.on=True
        self.kirjain=kirjain
        self.teksti = self.fontti.render(self.kirjain.upper(), True, (20, 20, 20))

    def backspace(self):
        self.on=False
        self.kirjain=""
        self.teksti = self.fontti.render(self.kirjain, True, (20, 20, 20))

    def resetoi(self):
        self.kirjain=""
        self.on=False

class nappaimisto:
    def __init__(self, positio, kirjain):
        self.posko = positio, (33, 33)
        self.kirjain = kirjain
        self.vari = (120,120,120)
        self.fontti = pygame.font.SysFont("Georgia", 25)
        self.teksti = self.fontti.render(self.kirjain, True, (20, 20, 20))
        self.paikka = (positio[0] + 8, positio[1] + 3)

    def vaihda_vihrea(self):
        self.vari = (180, 255, 190)

    def vaihda_harmaa(self):
        self.vari = (200, 200, 200)

    def vaihda_kelt(self):
        self.vari = (255, 255, 51)

    def vaihda_musta(self):
        self.vari = (50, 50, 50)

    def resetoi(self):
        self.vari = (120, 120, 120)

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

    def color_box_with_color(self, row, index, color):
        if color == "green":
            key = "vaihda_vihrea"
        if color == "black":
            key = "vaihda_musta"
        if color == "yellow":
            key = "vaihda_kelt"
        box = self.laatikot[row][index]
        getattr(box, key)()

    def get_box_row(self, row):
        return self.laatikot[row]

class WordBox:
    def __init__(self, positiokoko):
        self.vari =(80, 80, 80)
        self.posko=positiokoko
        self.vihrea=False

    def vaihda_vihrea(self):
        self.vari=(180,255,190)
        self.vihrea=True

    def vaihda_harmaa(self):
        self.vari=(200, 200, 200)

    def vaihda_kelt(self):
        self.vari=(255, 255, 51)

    def vaihda_musta(self):
        self.vari=(100, 100, 100)

    def resetoi(self):
        self.vari=(80, 80, 80)

class pointteri:
    def __init__(self,positiokoko):
        self.vari=(240,240,240)
        self.posko=positiokoko

class EventChecker:
    def __init__(self) -> None:
        self.hint_box_x = 40
        self.hint_box_y = 650

    def selected_hints(self, event):
        # Press hintbox or § key
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            return (self.hint_box_x < mouse_x < self.hint_box_x + 130 and 
                self.hint_box_y < mouse_y < self.hint_box_y + 40)
        elif event.type == pygame.KEYDOWN:
            return event.unicode=="§" 
        return False

    def get_event_type(self, event, game_handler):
        if self.selected_hints(event):
            return "open_or_close_hint_window"
        if event.type == pygame.KEYDOWN:
            if game_handler.havio or game_handler.voitto:
                if event.key == pygame.K_RETURN:
                    return "reset_game"
                return None
            if event.key == pygame.K_RETURN and game_handler.five_letters_typed:
                return "check_answer"
            if event.key == pygame.K_x:
                return "reset_game_with_same_solution"
            if event.key == pygame.K_BACKSPACE:
                return "remove_letter"
            if event.unicode in game_handler.merkit and event.unicode !="":
                game_handler.last_typed_letter = event.unicode
                return "type_a_letter"
            if event.key == pygame.K_ESCAPE:
                return "quit"
        if event.type == pygame.QUIT:
            return "quit"

class GameHandler:
    def __init__(self):
        self.solver = WordHints()
        self.x = 40
        self.y = 650
        hints = ["kasti", "taksi", "ratki", "kausi", "kilta", "kitua", "kiusa", "rasti", "silta", "raksi"]
        self.vihjesanat = [hint.upper() for hint in hints]
        self.mahdolliset = []
        self.vihjeet = True
        self.last_typed_letter=""
        self.sanalista = return_wordlist()
        self.sana = choice(self.sanalista)
        self.sana = "halpa"
        self.cursor_index = 0
        self.rivi = 0
        self.havio = False
        self.voitto = False
        self.word_in_dictionary = True
        self.merkit="abcdefghijklmnopqrstuwvyzåäö"
        self.letter_handler = GuessWords()
        ekarivi="qwertyuiop".upper()
        tokarivi="asdfghjklöä".upper()
        kolmosrivi="zxcvbnm".upper()
        self.guess_box_handler = GuessWordBoxes()

        self.keyboard=[]
        for i in range(len(ekarivi)):
            self.keyboard.append(nappaimisto((22+i*36,440),ekarivi[i]))
        for i in range(len(tokarivi)):
            self.keyboard.append(nappaimisto((5+i*36,480),tokarivi[i]))
        for i in range(len(kolmosrivi)):
            self.keyboard.append(nappaimisto((72+i*36,520),kolmosrivi[i]))

    def move_cursor_right(self):
        if self.cursor_index<4:
            self.cursor_index+=1

    def move_cursor_left(self):
        if self.cursor_index>0:
            self.cursor_index-=1

    ### GET_ATTR_FUNCTIONS ###

    def open_or_close_hint_window(self):
        if not self.vihjeet:
            self.screen = pygame.display.set_mode((565, 700))
            self.vihjeet=True
        else:
            self.screen = pygame.display.set_mode((400, 700))
            self.vihjeet=False
        return "continue"
    
    def reset_game_with_same_solution(self):
        correct_word = self.sana
        screen = self.screen
        new_game = GameHandler()
        self.__dict__.update(new_game.__dict__)
        self.sana = correct_word
        self.screen = screen
        return "continue"

    def reset_game(self):
        screen = self.screen
        new_game = GameHandler()
        self.__dict__.update(new_game.__dict__)
        self.screen = screen
        return "continue"
    
    def remove_letter(self):
        self.word_in_dictionary = True
        last_letter = self.cursor_index == 4 and self.letter.on
        self.letter.resetoi()
        if not last_letter:
            self.move_cursor_left()
            self.letter.resetoi()

    def type_a_letter(self):
        self.letter_handler.add_letter_to_index(self.rivi, self.cursor_index, self.last_typed_letter)
        self.move_cursor_right()

    def check_answer(self):
        print("checking guess:", self.guess, "with row", self.rivi)
        self.word_in_dictionary=False
        if self.guess in self.sanalista:
            self.word_in_dictionary=True
            return "play_row"
        return "continue"
    
    def play_row(self):
        print("Playing row with guess:", self.guess)
        self.cursor_index = 0
        self.color_everything_based_on_the_guess()
        laske_parhaat(self)
        self.voitto = False not in [self.guess[i] == self.sana[i] for i in range(5)]
        self.rivi += 1
        if not self.voitto and self.rivi == 5:
            self.havio=True

    def quit(self):
        exit()

    ### DRAWING FUNCTIONS ###

    def draw_hint_box(self):
        if self.vihjeet:
            self.screen.blit(pygame.font.SysFont("Georgia", 40).render("Vihjeet:",True,(20,20,20)),(400,50))
            for i in range(len(self.vihjesanat)):
                self.screen.blit(pygame.font.SysFont("Georgia", 28).render(f"{i+1}. {self.vihjesanat[i]}",True,(20,20,20)),(415,150+i*40))

    def draw_buttons(self):
        for i in self.keyboard:
            pygame.draw.rect(self.screen, i.vari, i.posko)
            self.screen.blit(i.teksti, i.paikka)
    
    def draw_boxes(self):
        self.guess_box_handler.draw(self.screen)

    def draw_basics(self):
        self.screen.fill((150, 150, 150))
        pygame.draw.rect(self.screen,(80,80,80),((self.x-3,self.y-3),(136,44)))
        pygame.draw.rect(self.screen,(200,200,200),((self.x,self.y),(130,38)))
        self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Vihjeet (§)",True,(20,20,20)),(self.x+5,self.y+5))

    def draw_game_state(self):
        if not self.voitto:
            if self.rivi!=5:
                pointer=pointteri((45+(self.cursor_index*60), 45+(self.rivi*60),60,60))
                pygame.draw.rect(self.screen,pointer.vari,pointer.posko)
                del pointer
            if not self.word_in_dictionary and self.five_letters_typed:
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Sanaa ei löytynyt",True,(20,20,20)),(50,350))
            elif self.havio==True:
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Hävisit pelin, oikea sana oli:",True,(20,20,20)),(50,350))
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render(self.sana,True,(20,20,20)),(50,380))
                self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Paina enter pelataksesi uudestaan",True,(20,20,20)),(50,410))
        else:
            self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Voitit pelin!",True,(20,20,20)),(50,350))
            self.screen.blit(pygame.font.SysFont("Georgia", 20).render("Paina enteriä pelataksesi uudestaan!",True,(20,20,20)),(50,380))

    def draw(self):
        self.draw_basics()
        self.draw_game_state()
        self.draw_boxes()
        self.letter_handler.draw_letters(self.screen)
        self.draw_buttons()
        self.draw_hint_box()

    ### Coloring functions ###
        
    def color_everything_based_on_the_guess(self):
        self.color_guess_boxes_black()
        self.color_keyboard_letters_black()
        self.color_matching_guess_boxes_green()
        self.color_matching_keyboard_keys_green()
        self.color_partially_matching_guess_boxes_yellow()
        self.color_partially_matching_keyboard_keys_yellow()
        
    def color_guess_boxes_black(self):
        for i in range(5):
            self.guess_box_handler.color_box_with_color(self.rivi, i, "black")

    def color_keyboard_letters_black(self):
        for typed_letter in self.guess:
            for key in self.keyboard:
                if key.kirjain.lower() == typed_letter:
                    key.vaihda_musta()

    def color_matching_guess_boxes_green(self):
        for i in range(len(self.guess)):
            if self.guess[i] == self.sana[i]:
                self.guess_box_handler.color_box_with_color(self.rivi, i, "green")

    def color_matching_keyboard_keys_green(self):
        for i in range(5):
            for nappain in self.keyboard:
                if nappain.kirjain.lower() == self.sana[i]:
                    nappain.vaihda_vihrea()

    def color_partially_matching_guess_boxes_yellow(self):
        remaining_letters = [self.sana[i] for i in range(5) if self.sana[i] in self.guess and self.sana[i] != self.guess[i]]
        for remaining_letter in remaining_letters:
            for index in range(5):
                if self.guess[index] == remaining_letter and not self.guess_box_handler.get_box_row(self.rivi)[index].vihrea:
                    self.guess_box_handler.color_box_with_color(self.rivi, index, "yellow")
                    break

    def color_partially_matching_keyboard_keys_yellow(self):
        remaining_letters = [self.sana[i] for i in range(5) if self.sana[i] in self.guess and self.sana[i] != self.guess[i]]
        for remaining_letter in remaining_letters:
            for index in range(5):
                if self.guess[index] == remaining_letter and not self.guess_box_handler.get_box_row(self.rivi)[index].vihrea:
                    self.guess_box_handler.color_box_with_color(self.rivi, index, "yellow")
                    break

    ### UTILITY AND PROPERTY FUNCS ####

    @property
    def guess(self):
        return self.letter_handler.get_row_word(self.rivi)

    @property
    def letter(self):
        return self.letter_handler.get_letter(self.rivi, self.cursor_index)
    
    @property
    def five_letters_typed(self):
        return len(self.guess) == 5


def laske_parhaat(game_handler):
    game_handler.solver.solve_possible_words(game_handler.guess, game_handler.sana)
    game_handler.mahdolliset = game_handler.solver.get_possible_words_as_strings()
    jako=len(game_handler.mahdolliset)
    lista=[]
    takaraja=0
    poisto=False
    for i in game_handler.mahdolliset:
        skip=False
        pituus=0
        for j in game_handler.mahdolliset:
            pituus+=palauta_tulos(j,i,game_handler.mahdolliset)
            if takaraja!=0 and (pituus/jako)>takaraja:
                skip=True
                break
        if not skip:
            lista.append((i,pituus/jako))
            lista.sort(key = lambda x:x[1])
            if poisto:
                lista=lista[:-1]
        if len(lista)>9:
            takaraja=lista[-1][1]
            poisto=True
    game_handler.vihjesanat=[]
    for i in lista:
        game_handler.vihjesanat.append(i[0].upper())

def initialize_game():
    pygame.init()
    game_handler=GameHandler()
    game_handler.screen = pygame.display.set_mode((400, 700))
    game_handler.screen.fill((200, 200, 200))
    game_handler.vihjeet=False
    ec = EventChecker()
    return game_handler, ec

def run_game(game_handler:'GameHandler', ec:'EventChecker'):
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            event_type = ec.get_event_type(event, game_handler) # ["open_or_close_hint_window", "type_a_letter", "check_answer", "remove_letter", "reset_game_with_same_solution", "reset_game", "quit", None]
            if event_type:
                ret_val = getattr(game_handler, event_type)()
                if ret_val == "continue":
                    break
                elif ret_val == "play_row":
                    game_handler.play_row()
        game_handler.draw()
        pygame.display.flip()

def main():
    game_handler, ec = initialize_game()
    run_game(game_handler, ec)

if __name__=="__main__":
    # testaa()

    main()
 






