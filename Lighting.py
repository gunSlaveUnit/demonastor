import math
import random

import pygame

import Constants
from GameObject import GameObject


class Lighting(GameObject):
    def __init__(self, center_x, center_y, animation_images, shooting_direction):
        super().__init__(center_x, center_y, animation_images=animation_images)
        _length = math.sqrt(shooting_direction[0] ** 2 + shooting_direction[1] ** 2)
        if _length == 0:
            _length = 1
        self._direction = (shooting_direction[0] / _length, shooting_direction[1] / _length)

        self._speed_x = random.randint(5, 7)
        self._speed_y = random.randint(5, 7)

        self._amount_damage = random.randint(5, 10)

    def _draw(self, surface, *args, **kwargs):
        if self._current_number_image_in_animation == self._amount_images_in_animation:
            self._current_number_image_in_animation = 0
        self._image = self._animation_images[
            self._current_direction_moving][
            self._current_number_image_in_animation]
        surface.blit(self._image, self.rect)
        now = pygame.time.get_ticks()
        if now - self._last_changing_image_time > self._animation_interval:
            self._last_changing_image_time = now
            self._current_number_image_in_animation += 1

    def _move(self):
        self._speed_x = random.randint(5, 7)
        self._speed_y = random.randint(5, 7)

        self._rect.centerx += self._direction[0] * self._speed_x
        self._rect.centery += self._direction[1] * self._speed_x

        if self._rect.bottom < 0 or \
                self._rect.left < 0 or \
                self._rect.top > Constants.GAME_WINDOW_HEIGHT or \
                self._rect.right > Constants.GAME_WINDOW_WIDTH:
            self.kill()

    @property
    def amount_additional_damage(self):
        return self._amount_damage
