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


class HealthPotion(Sprite):
    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self.__amount_health_regen_yet = 0
        self.__type = 'health'
        self.__image, self.__name, self.__regen_amount, self.__max_amount_for_regeneration, self.__resource_name = \
            self.__get_potion_values_depend_on_type()

        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y

    def __get_potion_values_depend_on_type(self):
        determining_type_potion = random.randint(0, 101)
        if determining_type_potion in range(0, 36):
            return (image.load(os.path.realpath(
                'resources/images/potions/health/small_health_potion.png')).convert(), 'Small\nHealth\nPotion', 5, 5, 'small_health_potion')
        if determining_type_potion in range(36, 61):
            return (image.load(os.path.realpath(
                'resources/images/potions/health/lesser_health_potion.png')).convert(), 'Lesser\nHealth\nPotion', 10, 15, 'lesser_health_potion')
        if determining_type_potion in range(61, 81):
            return (image.load(os.path.realpath(
                'resources/images/potions/health/medium_health_potion.png')).convert(), 'Medium\nHealth\nPotion', 15, 20, 'medium_health_potion')
        if determining_type_potion in range(81, 96):
            return (image.load(os.path.realpath(
                'resources/images/potions/health/greater_health_potion.png')).convert(), 'Greater\nHealth\nPotion', 20, 25, 'greater_health_potion')
        if determining_type_potion in range(96, 101):
            return (image.load(os.path.realpath(
                'resources/images/potions/health/huge_health_potion.png')).convert(), 'Huge\nHealth\nPotion', 25, 35, 'huge_health_potion')

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, (self.__rect.centerx, self.__rect.centery))

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value

    @property
    def regen_amount(self):
        return self.__regen_amount

    @property
    def amount_health_regen_yet(self):
        return self.__amount_health_regen_yet

    @amount_health_regen_yet.setter
    def amount_health_regen_yet(self, new_value):
        self.__amount_health_regen_yet = new_value

    @property
    def max_amount_health_for_regen(self):
        return self.__max_amount_for_regeneration

    @property
    def type(self):
        return self.__type

    @property
    def resource_name(self):
        return self.__resource_name
