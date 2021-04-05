"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2
File contains a description of Fireball class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

# TODO: Do I need to rename amount_additional_damage?

import math
import random

import pygame

import constants


class Fireball(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, shooting_direction):
        super().__init__()
        self._image = pygame.image.load('resources/images/shells/fireball.png').convert()
        self._rect = self.rect = self._image.get_rect()
        self._rect.centerx = init_center_x
        self._rect.centery = init_center_y

        _length = math.sqrt(shooting_direction[0] ** 2 + shooting_direction[1] ** 2)
        self._direction = (shooting_direction[0] / _length, shooting_direction[1] / _length)

        self._speed_x = random.randint(3, 10)
        self._speed_y = random.randint(3, 10)

        self._amount_additional_damage = random.randint(1, 5)

    def update(self, surface):
        super().update()
        self._draw(surface)
        self._move()

        self._amount_additional_damage = random.randint(1, 5)

    def _draw(self, surface):
        surface.blit(self._image, (self._rect.centerx, self._rect.centery))

    def _move(self):
        self._speed_x = random.randint(3, 10)
        self._speed_y = random.randint(3, 10)

        self._rect.centerx += self._direction[0] * random.randint(5, 10)
        self._rect.centery += self._direction[1] * random.randint(5, 10)

        if self._rect.bottom < 0 or \
                self._rect.left < 0 or \
                self._rect.top > constants.GAME_WINDOW_HEIGHT or \
                self._rect.right > constants.GAME_WINDOW_WIDTH:
            self.kill()

    def get_amount_additional_damage(self):
        return self._amount_additional_damage
