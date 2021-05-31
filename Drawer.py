import pygame

import Constants


class Drawer:
    @staticmethod
    def draw_text(surface, text, size, color, x, y):
        font_name = pygame.font.match_font('resources/fonts/samson_font.ttf')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    @staticmethod
    def draw_bar(surface, center_x, center_y, color, current_value, max_value, bar_length, bar_height,
                 is_frame_need=False):
        if current_value < 0:
            current_value = 0

        fill = (current_value * bar_length) // max_value
        if fill > bar_length:
            fill = bar_length
        outline_rect = pygame.Rect(center_x - bar_length // 2, center_y, bar_length, bar_height)
        fill_rect = pygame.Rect(center_x - bar_length // 2, center_y, fill, bar_height)
        pygame.draw.rect(surface, color, fill_rect)
        if is_frame_need:
            pygame.draw.rect(surface, Constants.WHITE_COLOR_TITLE_BLOCKS, outline_rect, 1)
