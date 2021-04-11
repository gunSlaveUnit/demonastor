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


class Potion(Sprite):
    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        determining_type_potion = random.randint(0, 101)
        if determining_type_potion in range(0, 36):
            self.__image = image.load(os.path.realpath(
                'resources/images/potions/health/small_health_potion.png')).convert()
            self.__name = 'Small\nHealth\nPotion'
            self.__regen_amount = 5
        if determining_type_potion in range(36, 61):
            self.__image = image.load(os.path.realpath(
                'resources/images/potions/health/lesser_health_potion.png')).convert()
            self.__name = 'Lesser\nHealth\nPotion'
            self.__regen_amount = 15
        if determining_type_potion in range(61, 81):
            self.__image = image.load(os.path.realpath(
                'resources/images/potions/health/medium_health_potion.png')).convert()
            self.__name = 'Medium\nHealth\nPotion'
            self.__regen_amount = 20
        if determining_type_potion in range(81, 96):
            self.__image = image.load(os.path.realpath(
                'resources/images/potions/health/greater_health_potion.png')).convert()
            self.__name = 'Greater\nHealth\nPotion'
            self.__regen_amount = 25
        if determining_type_potion in range(96, 101):
            self.__image = image.load(os.path.realpath(
                'resources/images/potions/health/huge_health_potion.png')).convert()
            self.__name = 'Huge\nHealth\nPotion'
            self.__regen_amount = 35
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, (self.__rect.centerx, self.__rect.centery))

    def get_rect(self):
        return self.__rect
