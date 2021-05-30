"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describes the class that is the parent for most of the game objects, represented on the screen as a sprite.
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-
import pygame.time
from pygame.sprite import Sprite
from pygame import image


class GameObject(Sprite):
    """
    The base class for most of the objects represented by the sprite.
    Can represent an object with or without animation.
    """

    _DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, center_x, center_y, basic_image=None, animation_images=None):
        """
        Creates a gaming object.
        :param center_x: the x coordinates of the rectangle.
        :param center_y: the y coordinates of the rectangle.
        :param basic_image: the name of the image if you want an object without animation.
        :param animation_images: contains a list of names of
        images required for animation movement in four directions. Format: [[LEFT],[RIGHT],[UP],[DOWN]].

        basic_image or animation_images only
        """
        if basic_image is None and animation_images is None:
            raise Exception("Object does not have an image or group of images specified.")
        elif basic_image and animation_images:
            raise Exception("Object has both one image and animation.")
        super().__init__()
        if basic_image:
            self._image = self._load_image(basic_image)
        elif animation_images:
            self._animation_images = self._load_images(animation_images)
            self._image = self._animation_images[0][0]
            self._amount_images_in_animation = len(self._animation_images[0])
            self._current_number_image_in_animation = 0
            self._current_direction_moving = self._DIRECTIONS_MOVING['DOWN']
            self._last_changing_image_time = 0
            self._animation_interval = 0
        self._rect = self._image.get_rect()
        self._rect.centerx = center_x
        self._rect.centery = center_y
        self._name = ''

    @staticmethod
    def _load_image(image_name):
        """
        Loads one image for an object.
        :param image_name: name of the image to load
        :return: loaded image object
        """
        return image.load(image_name)

    @staticmethod
    def _load_images(images):
        """
        The method loads images for animation.
        :param images: the names of the images to be loaded. Format: [[LEFT],[RIGHT],[UP],[DOWN]].
        :return: the list of lists of loaded images objects in [[LEFT],[RIGHT],[UP],[DOWN]] format.
        """
        loaded_images = []
        for one_direction_animation_images in images:
            loaded_one_direction_images = []
            for picture_name in one_direction_animation_images:
                picture = image.load(picture_name)
                loaded_one_direction_images.append(picture)
            loaded_images.extend([loaded_one_direction_images])
        return loaded_images

    def update(self, surface, *args, **kwargs):
        """
        This method is just a hook that can be called during the running of the game loop.
        Calls the _draw and _move methods by default.
        :param surface: window object
        :return: None
        """
        self._draw(surface)
        self._move()

    def _draw(self, surface, *args, **kwargs):
        """
        This method is just a hook in which to draw the animation of the object with interval or just the object.
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
