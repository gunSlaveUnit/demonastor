"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describes a Map class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import pygame


class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__map_tiles = list()

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        for map_tile in self.__map_tiles:
            map_tile.update(surface)

    @property
    def map_tiles(self):
        return self.__map_tiles
