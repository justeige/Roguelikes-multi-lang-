import pygame
import color

pygame.font.init()
DEBUG_FONT = pygame.font.Font(None, 30)
DEFAULT_FONT = DEBUG_FONT 

class Console:
    def __init__(self, background_color = None):
        self.background_color = background_color
        self.game_messages = []

    def create_text_object(self, text, color):
        text_surface = DEBUG_FONT.render(text, False, color, self.background_color)
        return (text_surface, text_surface.get_rect())

    def calc_text_height(self, font):
        font_obj = font.render('a', False, (0,0,0))
        font_rect = font_obj.get_rect()
        return font_rect.height

    def message(self, msg, color = color.WHITE):
        self.game_messages.append((msg, color))

    def draw_messages(self, heigth, surface):
        MAX_MESSAGES = 4
        to_draw = self.game_messages[-MAX_MESSAGES:] # TODO make this changeable!

        text_height = self.calc_text_height(DEFAULT_FONT)
        start_y = heigth - (MAX_MESSAGES * text_height)

        i = 0
        for msg, col in to_draw:            
            self.draw_text(surface, msg, (0, start_y + (i * text_height)), col)
            i += 1
    
    def draw_text(self, display_surface, text, coords, text_color):
        text_surface, text_rect = self.create_text_object(text, text_color)
        text_rect.topleft = coords 

        display_surface.blit(text_surface, text_rect)
    
    def draw_debug_text(self, surface):
        self.draw_text(surface, "test", (20, 20), color.RED)