import pygame
class EventChecker:
    def __init__(self) -> None:
        self.hint_box_x = 40
        self.hint_box_y = 650
        self.characters = "abcdefghijklmnopqrstuwvyzåäö"

    def selected_hints(self, event):
        # Press hintbox or § key
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            return (self.hint_box_x < mouse_x < self.hint_box_x + 130 and 
                self.hint_box_y < mouse_y < self.hint_box_y + 40)
        elif event.type == pygame.KEYDOWN:
            return event.unicode=="§" 
        return False

    def get_event_type(self, event):
        data = {"type": None, "char": None}
        if self.selected_hints(event):
            data["type"]  = "open_or_close_hint_window"
            return data
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            data["type"]  = "quit"
            return data
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                data["type"] = "enter"  
            elif event.key == pygame.K_x:
                data["type"]  = "reset_game_with_same_solution"
            elif event.key == pygame.K_BACKSPACE:
                data["type"]  = "remove_letter"
            elif event.unicode in self.characters and event.unicode !="":
                data["char"] = event.unicode
                data["type"]  = "type_a_letter"
            return data
        return data