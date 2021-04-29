"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file contains a class description for all playable potions that enhance or weaken,
decrease or increase any characteristics/.
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import random
import os

from pygame.sprite import Sprite
from pygame import image


class ManaPotion(Sprite):
    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self.__amount_health_regen_yet = 0
        self.__type = 'mana'
        self.__image, self.__name, self.__regen_amount, self.__max_amount_for_regeneration = \
            self.__get_potion_values_depend_on_type()

        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y

    def __get_potion_values_depend_on_type(self):
        determining_type_potion = random.randint(0, 101)
        if determining_type_potion in range(0, 36):
            return (image.load(os.path.realpath(
                'resources/images/potions/mana/small_mana_potion.png')).convert(), 'Small\nMana\nPotion', 5, 5)
        if determining_type_potion in range(36, 61):
            return (image.load(os.path.realpath(
                'resources/images/potions/mana/lesser_mana_potion.png')).convert(), 'Lesser\nMana\nPotion', 10, 15)
        if determining_type_potion in range(61, 81):
            return (image.load(os.path.realpath(
                'resources/images/potions/mana/medium_mana_potion.png')).convert(), 'Medium\nMana\nPotion', 15, 20)
        if determining_type_potion in range(81, 96):
            return (image.load(os.path.realpath(
                'resources/images/potions/mana/greater_mana_potion.png')).convert(), 'Greater\nMana\nPotion', 20, 25)
        if determining_type_potion in range(96, 101):
            return (image.load(os.path.realpath(
                'resources/images/potions/mana/huge_mana_potion.png')).convert(), 'Huge\nMana\nPotion', 25, 35)

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, (self.__rect.centerx, self.__rect.centery))

    def get_rect(self):
        return self.__rect

    def get_regen_amount(self):
        return self.__regen_amount

    def get_amount_health_regen_yet(self):
        return self.__amount_health_regen_yet

    def set_amount_health_regen_yet(self, new_value):
        self.__amount_health_regen_yet = new_value

    def get_max_amount_health_for_regen(self):
        return self.__max_amount_for_regeneration

    def get_type(self):
        return self.__type
