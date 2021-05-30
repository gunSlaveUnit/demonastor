"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describes the base class for the player, enemy and neutral units.
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import pygame.time

from GameObject import GameObject


class Character(GameObject):
    def __init__(self, center_x, center_y, animation_images):
        """
        Creates an object to represent the player, enemies, and neutrals.
        :param center_x: the x coordinates of the rectangle.
        :param center_y: the y coordinates of the rectangle.
        :param animation_images: contains a list of names of
        images required for animation movement in four directions. Format: [[LEFT],[RIGHT],[UP],[DOWN]].
        """
        super().__init__(center_x, center_y, animation_images=animation_images)
        self._max_health = 0
        self._max_mana = 0
        self._max_stamina = 0
        self._current_health = 0
        self._current_mana = 0
        self._current_stamina = 0
        self._passive_regeneration = 0
        self._attack_interval = 0
        self._regeneration_interval = 0
        self._changing_direction_interval = 0
        self._last_attack_time = pygame.time.get_ticks()
        self._last_regeneration_time = pygame.time.get_ticks()
        self._last_changing_direction_time = pygame.time.get_ticks()
        self._last_changing_image_time = pygame.time.get_ticks()
        self._amount_damage = 0
        self._speed_changing = 0
        self._speed_x = 0
        self._speed_y = 0
        self._level = 1

    def _regeneration(self):
        now = pygame.time.get_ticks()
        if now - self._last_attack_time > self._attack_interval:
            self._last_attack_time = now
            self._current_health += self._passive_regeneration
            self._current_mana += self._passive_regeneration
            self._current_stamina += self._passive_regeneration

            if self._current_health > self._max_health:
                self._current_health = self._max_health
            if self._current_mana > self._max_mana:
                self._current_mana = self._max_mana
            if self._current_stamina > self._max_stamina:
                self._current_stamina = self._max_stamina
