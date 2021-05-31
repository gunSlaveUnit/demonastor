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

import Constants
from GameObject import GameObject


class Fireball(GameObject):
    def __init__(self, center_x, center_y, basic_image, shooting_direction):
        super().__init__(center_x, center_y, basic_image)

        _length = math.sqrt(shooting_direction[0] ** 2 + shooting_direction[1] ** 2)
        if _length == 0:
            _length = 1
        self._direction = (shooting_direction[0] / _length, shooting_direction[1] / _length)

        self._speed_x = random.randint(5, 10)
        self._speed_y = random.randint(5, 10)

        self._amount_damage = random.randint(1, 5)

    def update(self, surface, *args, **kwargs):
        self._draw(surface)
        self._move()

        self._amount_damage = random.randint(1, 5)

    def _draw(self, surface, *args, **kwargs):
        surface.blit(self._image, (self._rect.centerx, self._rect.centery))

    def _move(self):
        self._speed_x = random.randint(5, 10)
        self._speed_y = random.randint(5, 10)

        self._rect.centerx += self._direction[0] * self._speed_x
        self._rect.centery += self._direction[1] * self._speed_x

        if self._rect.bottom < 0 or \
                self._rect.left < 0 or \
                self._rect.top > Constants.GAME_WINDOW_HEIGHT or \
                self._rect.right > Constants.GAME_WINDOW_WIDTH:
            self.kill()

    @property
    def amount_additional_damage(self):
        return self._amount_damage
