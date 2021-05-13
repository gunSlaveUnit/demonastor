"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

File contains a description of Fireball class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import math
import random

import pygame

import constants


class Fireball(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, shooting_direction):
        super().__init__()
        self.__image = pygame.image.load('resources/images/shells/fireball.png').convert()
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y

        __length = math.sqrt(shooting_direction[0] ** 2 + shooting_direction[1] ** 2)
        self.__direction = (shooting_direction[0] / __length, shooting_direction[1] / __length)

        self.__speed_x = random.randint(3, 10)
        self.__speed_y = random.randint(3, 10)

        self.__amount_damage = random.randint(140, 250)

    def update(self, surface):
        self.__draw(surface)
        self.__move()

        self.__amount_damage = random.randint(1, 5)

    def __draw(self, surface):
        surface.blit(self.__image, (self.__rect.centerx, self.__rect.centery))

    def __move(self):
        self._speed_x = random.randint(3, 10)
        self._speed_y = random.randint(3, 10)

        self.__rect.centerx += self.__direction[0] * random.randint(1, 5)
        self.__rect.centery += self.__direction[1] * random.randint(1, 5)

        if self.__rect.bottom < 0 or \
                self.__rect.left < 0 or \
                self.__rect.top > constants.GAME_WINDOW_HEIGHT or \
                self.__rect.right > constants.GAME_WINDOW_WIDTH:
            self.kill()

    @property
    def amount_additional_damage(self):
        return self.__amount_damage

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value
