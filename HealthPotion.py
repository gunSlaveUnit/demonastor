"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file contains a class description for all playable potions that enhance or weaken,
decrease or increase any characteristics/.
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import GameEnums
from GameObject import GameObject


class HealthPotion(GameObject):
    def __init__(self, center_x, center_y, basic_image, volume):
        super().__init__(center_x, center_y, basic_image)
        self._amount_health_regen_yet = 0
        self._type = 'health'
        self._name, self._regen_amount, self._max_amount_for_regeneration, self._resource_name = \
            self._get_potion_values_depend_on_volume(volume)

    @staticmethod
    def _get_potion_values_depend_on_volume(volume):
        if volume == GameEnums.PotionVolume.SMALL.value:
            return 'Small\nHealth\nPotion', 5, 5, 'small_health_potion'
        elif volume == GameEnums.PotionVolume.LESSER.value:
            return 'Lesser\nHealth\nPotion', 10, 15, 'lesser_health_potion'
        elif volume == GameEnums.PotionVolume.MEDIUM.value:
            return 'Medium\nHealth\nPotion', 15, 20, 'medium_health_potion'
        elif volume == GameEnums.PotionVolume.GREATER.value:
            return 'Greater\nHealth\nPotion', 20, 25, 'greater_health_potion'
        elif volume == GameEnums.PotionVolume.HUGE.value:
            return 'Huge\nHealth\nPotion', 25, 35, 'huge_health_potion'

    @property
    def regen_amount(self):
        return self._regen_amount

    @property
    def amount_health_regen_yet(self):
        return self._amount_health_regen_yet

    @amount_health_regen_yet.setter
    def amount_health_regen_yet(self, new_value):
        self._amount_health_regen_yet = new_value

    @property
    def max_amount_health_for_regen(self):
        return self._max_amount_for_regeneration

    @property
    def type(self):
        return self._type

    @property
    def resource_name(self):
        return self._resource_name
