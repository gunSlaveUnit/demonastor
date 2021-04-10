"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

File contains a description of Camera class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import constants


class Camera:
    def __init__(self, window_sizes):
        self.__dx = 0
        self.__dy = 0
        self.__view_sizes = window_sizes

    def apply(self, game_object):
        game_object.get_rect().centerx -= self.__dx
        game_object.get_rect().centery -= self.__dy

    def update(self, target):
        self.__dx = target.get_rect().centerx - constants.GAME_WINDOW_WIDTH // 2
        self.__dy = target.get_rect().centery - constants.GAME_WINDOW_HEIGHT // 2
        target.get_rect().centerx = constants.GAME_WINDOW_WIDTH // 2
        target.get_rect().centery = constants.GAME_WINDOW_HEIGHT // 2
