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
    def __init__(self):
        """
        Creates a camera following the player.
        """
        self._dx = 0
        self._dy = 0

    def update(self, target):
        """
        The method calculates object displacements and keeps the player in the center at all times.
        :param target: player object with rect attribute. An object of the Sprite class.
        :return: None
        """
        self._dx = target.rect.centerx - constants.GAME_WINDOW_WIDTH // 2
        self._dy = target.rect.centery - constants.GAME_WINDOW_HEIGHT // 2
        target.rect.centerx = constants.GAME_WINDOW_WIDTH // 2
        target.rect.centery = constants.GAME_WINDOW_HEIGHT // 2

    @property
    def offset(self):
        return self._dx, self._dy
