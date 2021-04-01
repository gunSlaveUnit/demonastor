"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2
File contains a description of Potion class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

# TODO: pygame.sprite.Sprite -> Sprite in all files

import random
import os

import pygame


class Potion(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        determining_type_potion = random.randint(0, 101)
        if determining_type_potion in range(0, 36):
            self._image = pygame.image.load(os.path.realpath('Potions/Health/small_health_potion.png')).convert()
            self._name = 'Small\nHealth\nPotion'
            self._regen_amount = 5
        if determining_type_potion in range(36, 61):
            self._image = pygame.image.load(os.path.realpath('Potions/Health/lesser_health_potion.png')).convert()
            self._name = 'Lesser\nHealth\nPotion'
            self._regen_amount = 15
        if determining_type_potion in range(61, 81):
            self._image = pygame.image.load(os.path.realpath('Potions/Health/medium_health_potion.png')).convert()
            self._name = 'Medium\nHealth\nPotion'
            self._regen_amount = 20
        if determining_type_potion in range(81, 96):
            self._image = pygame.image.load(os.path.realpath('Potions/Health/greater_health_potion.png')).convert()
            self._name = 'Greater\nHealth\nPotion'
            self._regen_amount = 25
        if determining_type_potion in range(96, 101):
            self._image = pygame.image.load(os.path.realpath('Potions/Health/huge_health_potion.png')).convert()
            self._name = 'Huge\nHealth\nPotion'
            self._regen_amount = 35
        self._rect = self.rect = self._image.get_rect()
        self._rect.centerx = init_center_x
        self._rect.centery = init_center_y

    def update(self, surface):
        super().update()
        self._draw(surface)

    def _draw(self, surface):
        surface.blit(self._image, (self._rect.centerx, self._rect.centery))
