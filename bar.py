"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

File contains a description of Bar class (health of mana circle)
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import pygame

import game_enums


class Bar(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, bar_type):
        super().__init__()

        if bar_type == game_enums.PlayerBarTypes.HEALTH.value:
            self.__image = pygame.image.load('resources/images/bars/health_bar.png')
        elif bar_type == game_enums.PlayerBarTypes.MANA.value:
            self.__image = pygame.image.load('resources/images/bars/mana_bar.png').convert()

        self.__rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y

    def update(self, surface, player_current_characteristic, player_max_characteristic):
        self.__draw(surface, player_current_characteristic, player_max_characteristic)

    def __draw(self, surface, player_current_characteristic, player_max_characteristic):
        how_much_cut = self.__rect.height - self.__rect.height * (
                    player_current_characteristic / player_max_characteristic)
        if how_much_cut < 0:
            how_much_cut = 0
        surface.blit(self.__image,
                     (self.__rect.centerx, self.__rect.centery + how_much_cut),
                     (0, how_much_cut, self.__rect.width, self.__rect.height))
