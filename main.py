import pygame
from drawer import GameDrawer
from inputs import EventChecker
from game_handler import GameHandler


def initialize_game():
    game_handler = GameHandler()
    ec = EventChecker()
    game_drawer = GameDrawer()
    game_drawer.update_guess_related_values(game_handler.get_game_state())
    return game_handler, ec, game_drawer


def run_game(game_handler:'GameHandler', ec:'EventChecker', game_drawer:'GameDrawer'):
    while True:
        for event in pygame.event.get():
            event_data = ec.get_event_type(event)
            event_type = event_data["type"]
            char = event_data["char"]
            if event_type == "enter":
                if game_handler.winning or game_handler.losing:
                    reset_game(game_handler, "reset_game", game_drawer)
                elif game_handler.all_letters_typed:
                    ret_val = game_handler.check_answer()
                    if ret_val == "play_row":
                        game_handler.solve_clues()
                        game_handler.play_row()
                        game_drawer.update_guess_related_values(game_handler.get_game_state())
            elif event_type == "quit":
                exit()
            elif event_type in ["type_a_letter", "remove_letter"]:
                if char:
                    getattr(game_handler, event_type)(char)
                else:
                    getattr(game_handler, event_type)()
                game_drawer.update_guess_related_values(game_handler.get_game_state())
            elif event_type in ["open_or_close_hint_window"]:
                game_drawer.open_or_close_hint_window()
            elif event_type in ["reset_game_with_same_solution"]:
                reset_game(game_handler, event_type, game_drawer)
        game_drawer.draw()


def reset_game(game_handler:'GameHandler', game_handler_call, game_drawer:'GameDrawer'):
    print("Reseting game")
    game_drawer.reset()
    getattr(game_handler, game_handler_call)()
    game_drawer.update_guess_related_values(game_handler.get_game_state())


def main():
    game_handler, ec, game_drawer = initialize_game()
    run_game(game_handler, ec, game_drawer)


if __name__ == '__main__':
    main()
 