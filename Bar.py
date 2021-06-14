"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

File contains a description of Bar class (health or mana circle)
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

from GameObject import GameObject


class Bar(GameObject):
    def __init__(self, center_x, center_y, basic_image):
        """
        Creates a sprite of health or mana bar.
        :param center_x: the x coordinates of the rectangle.
        :param center_y: the y coordinates of the rectangle.
        :param basic_image: the name of the image if you want an object without animation.
        """
        super().__init__(center_x, center_y, basic_image)

    def update(self, surface, *args, **kwargs):
        """
        A handler called during the game loop. Also handles rendering of the object.
        :param surface: where to draw (pygame window)
        :param args: here pass two values - current and maximum values of some characteristic
        :param kwargs:
        :return: None
        """
        self._draw(surface, args[0], args[1])

    def _draw(self, surface, *args, **kwargs):
        """
        Draws a part of a circle depending on the current value of some characteristic
        :param surface: where to draw (pygame window)
        :param args: here pass two values - current and maximum values of some characteristic
        :param kwargs:
        :return: None
        """
        how_much_cut = self._rect.height - self._rect.height * (args[0] / args[1])
        if how_much_cut < 0:
            how_much_cut = 0
        surface.blit(self._image,
                     (self._rect.centerx, self._rect.centery + how_much_cut),
                     (0, how_much_cut, self._rect.width, self._rect.height))
