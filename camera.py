"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file contains the camera class.
The camera follows the player in such a way that he always stays in the center of the screen.
For all other game objects on the screen and beyond, the required displacement is
calculated so that there is an illusion that the player is approaching them.
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import constants


class Camera:
    def __init__(self, window_sizes):
        """
        Creates a camera following the player.
        :param window_sizes: a tuple of the width and height of the window in pixels.
        """
        self.__dx = 0
        self.__dy = 0
        self.__view_sizes = window_sizes

    def apply(self, game_object):
        """
        The method applies the calculated offset to the passed object.
        :param game_object: an object of the Sprite class or its descendants containing the rect attribute.
        :return: None
        """
        game_object.get_rect().centerx -= self.__dx
        game_object.get_rect().centery -= self.__dy

    def update(self, target):
        """
        The method calculates object displacements and keeps the player in the center at all times.
        :param target: player object with rect attribute. An object of the Sprite class.
        :return: None
        """
        self.__dx = target.get_rect().centerx - constants.GAME_WINDOW_WIDTH // 2
        self.__dy = target.get_rect().centery - constants.GAME_WINDOW_HEIGHT // 2
        target.get_rect().centerx = constants.GAME_WINDOW_WIDTH // 2
        target.get_rect().centery = constants.GAME_WINDOW_HEIGHT // 2
