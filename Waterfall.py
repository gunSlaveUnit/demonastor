# ! usr/bin/env python3
# -*- coding: utf8 -*-

from GameObject import GameObject


class Waterfall(GameObject):
    def __init__(self, center_x, center_y, animation_images):
        super().__init__(center_x, center_y, animation_images=animation_images)

    def update(self, surface, *args, **kwargs):
        self._draw(surface)

    def _draw(self, surface, *args, **kwargs):
        if self._current_number_image_in_animation == self._amount_images_in_animation*2:
            self._current_number_image_in_animation = 0

        self._image = self._animation_images[self._current_number_image_in_animation//2]
        surface.blit(self._image, self._rect)
        self._current_number_image_in_animation += 1
