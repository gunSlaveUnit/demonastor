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


class GameObject(Sprite):
    """
    Base class for most objects represented by a sprite.
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
        self._animation_images = self._load_images(animation_images)
        self._image = self._animation_images[0][0]
        self._rect = self._image.get_rect()
        self._rect.centerx = center_x
        self._rect.centery = center_y
        self.__amount_images_in_animation = len(self._animation_images[0])
        self.__current_number_image_in_animation = 0
        self.__current_direction_moving = self._DIRECTIONS_MOVING['DOWN']

    @staticmethod
    def _load_images(images):
        """
        The method loads images for animation.
        :param images: the names of the images to be loaded. Format: [[LEFT],[RIGHT],[UP],[DOWN]]
        :return: the list of lists of loaded images in [[LEFT],[RIGHT],[UP],[DOWN]] format.
        """
        loaded_images = []
        for one_direction_animation_images in images:
            loaded_one_direction_images = []
            for picture_name in one_direction_animation_images:
                picture = image.load(picture_name)
                loaded_one_direction_images.append(picture)
            loaded_images.extend([loaded_one_direction_images])
        return loaded_images

    def update(self, *args, **kwargs):
        """
        This method is just a hook that can be called during the running of the game loop.
        Calls the _draw and _move methods by default.
        :return: None
        """
        self._draw()
        self._move()

    def _draw(self, *args, **kwargs):
        """
        This method is just a hook in which to draw the animation of the object.
        :return: None
        """
        pass

    def _move(self, *args, **kwargs):
        """
        This method is just a hook in which to move the object.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @property
    def rect(self):
        return self._rect
