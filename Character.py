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
        if now - self._last_regeneration_time > self._regeneration_interval:
            self._last_regeneration_time = now
            self._current_health += self._passive_regeneration
            self._current_mana += self._passive_regeneration
            self._current_stamina += self._passive_regeneration

            if self._current_health > self._max_health:
                self._current_health = self._max_health
            if self._current_mana > self._max_mana:
                self._current_mana = self._max_mana
            if self._current_stamina > self._max_stamina:
                self._current_stamina = self._max_stamina

    def _draw(self, surface, *args, **kwargs):
        if self._current_number_image_in_animation == self._amount_images_in_animation:
            self._current_number_image_in_animation = 0
        self._image = self._animation_images[
            self._current_direction_moving][
            self._current_number_image_in_animation]
        surface.blit(self._image, self.rect)
        now = pygame.time.get_ticks()
        if now - self._last_changing_image_time > self._animation_interval:
            self._last_changing_image_time = now
            self._current_number_image_in_animation += 1

    @property
    def amount_damage(self):
        return self._amount_damage

    @property
    def current_health(self):
        return self._current_health

    @property
    def max_amount_health(self):
        return self._max_health

    @current_health.setter
    def current_health(self, new_value):
        self._current_health = new_value

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def current_stamina(self):
        return self._current_stamina

    @property
    def max_stamina(self):
        return self._max_stamina
