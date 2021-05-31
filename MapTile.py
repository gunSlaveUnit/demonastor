"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describe one tile in the map
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

from GameObject import GameObject


class MapTile(GameObject):
    def __init__(self, center_x, center_y, basic_image):
        super().__init__(center_x, center_y, basic_image)
