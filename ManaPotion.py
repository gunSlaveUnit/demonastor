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


class ManaPotion(GameObject):
    def __init__(self, center_x, center_y, basic_image, volume):
        super().__init__(center_x, center_y, basic_image)
        self._amount_mana_regen_yet = 0
        self._type = 'mana'
        self._name, self._regen_amount, self._max_amount_for_regeneration, self._resource_name = \
            self._get_potion_values_depend_on_volume(volume)

    @staticmethod
    def _get_potion_values_depend_on_volume(volume):
        if volume == GameEnums.PotionVolume.SMALL.value:
            return 'Small\nMana\nPotion', 5, 5, 'small_mana_potion'
        elif volume == GameEnums.PotionVolume.LESSER.value:
            return 'Lesser\nMana\nPotion', 10, 15, 'lesser_mana_potion'
        elif volume == GameEnums.PotionVolume.MEDIUM.value:
            return 'Medium\nMana\nPotion', 15, 20, 'medium_mana_potion'
        elif volume == GameEnums.PotionVolume.GREATER.value:
            return 'Greater\nMana\nPotion', 20, 25, 'greater_mana_potion'
        elif volume == GameEnums.PotionVolume.HUGE.value:
            return 'Huge\nMana\nPotion', 25, 35, 'huge_mana_potion'

    @property
    def regen_amount(self):
        return self._regen_amount

    @property
    def amount_mana_regen_yet(self):
        return self._amount_mana_regen_yet

    @amount_mana_regen_yet.setter
    def amount_mana_regen_yet(self, new_value):
        self._amount_mana_regen_yet = new_value

    @property
    def max_amount_mana_for_regen(self):
        return self._max_amount_for_regeneration

    @property
    def type(self):
        return self._type

    @property
    def resource_name(self):
        return self._resource_name
