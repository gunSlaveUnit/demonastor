"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describes the class that is the parent for most of the game objects, represented on the screen as a sprite.
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

from pygame.sprite import Sprite
from pygame import image

from GameObject import GameObject


class Character(GameObject):
    """

    """

    _DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, center_x, center_y, animation_images):
        """
         Creates a gaming object.
        :param center_x: the x coordinates of the rectangle.
        :param center_y: the y coordinates of the rectangle.
        :param animation_images: contains a list of names of
        images required for animation movement in four directions. Format: [[LEFT],[RIGHT],[UP],[DOWN]].
        """
        super().__init__()


