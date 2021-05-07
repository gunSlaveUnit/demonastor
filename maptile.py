"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describe one tile in the map
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import pygame


class MapTile(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, file_path):
        super().__init__()
        self.__image = pygame.image.load(file_path).convert()
        self.__rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, self.__rect)

    @property
    def rect(self):
        return self.__rect
