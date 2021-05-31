"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describes a Map class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-
import random

import pygame

import Constants
import maptile


class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__map_tiles = list()
        for init_x in range(-Constants.GAME_WINDOW_WIDTH * 2, Constants.GAME_WINDOW_WIDTH * 2,
                            random.randint(500, 524)):
            for init_y in range(-Constants.GAME_WINDOW_HEIGHT * 2, Constants.GAME_WINDOW_HEIGHT * 2,
                                random.randint(300, 340)):
                map_tile = maptile.MapTile(init_x, init_y, 'resources/images/map/grass.png')
                self.__map_tiles.append(map_tile)

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        for map_tile in self.__map_tiles:
            map_tile.update(surface)

    @property
    def map_tiles(self):
        return self.__map_tiles
