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
        super().__init__(center_x, center_y, basic_image)

    def update(self, surface, *args, **kwargs):
        self._draw(surface, args[0], args[1])

    def _draw(self, surface, *args, **kwargs):
        how_much_cut = self._rect.height - self._rect.height * (
                    args[0] / args[1])
        if how_much_cut < 0:
            how_much_cut = 0
        surface.blit(self._image,
                     (self._rect.centerx, self._rect.centery + how_much_cut),
                     (0, how_much_cut, self._rect.width, self._rect.height))
