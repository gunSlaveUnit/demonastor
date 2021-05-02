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

from maptile import MapTile


class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__map_tiles = list()
        start_coordinates_to_generate_map = [0, 0]
        for _ in range(0, 50):
            for _ in range(0, 50):
                self.__map_tiles.append(MapTile(start_coordinates_to_generate_map[0],
                                                start_coordinates_to_generate_map[1]))
                start_coordinates_to_generate_map[0] += 256
            start_coordinates_to_generate_map[1] += 128
            start_coordinates_to_generate_map[0] = 0

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        for map_tile in self.__map_tiles:
            map_tile.update(surface)

    @property
    def map_tiles(self):
        return self.__map_tiles
