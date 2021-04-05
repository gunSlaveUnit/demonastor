"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2
File contains a description of Player class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import random
import math

import pygame


class Demon(pygame.sprite.Sprite):
    _DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self._image = pygame.image.load('resources/images/enemy/enemy_moving_down.png').convert()
        self._rect = self.rect = self._image.get_rect()
        self._rect.centerx = init_center_x
        self._rect.centery = init_center_y
        self._tile_set = [
            [
                pygame.image.load('resources/images/enemy/enemy_moving_left.png').convert()
            ],
            [
                pygame.image.load('resources/images/enemy/enemy_moving_right.png').convert()
            ],
            [
                pygame.image.load('resources/images/enemy/enemy_moving_up.png').convert()
            ],
            [
                pygame.image.load('resources/images/enemy/enemy_moving_down.png').convert()
            ]

        ]
        self._amount_images_in_animation = len(self._tile_set[0])
        self._current_number_image_in_animation = 0
        self._current_direction_moving = Demon._DIRECTIONS_MOVING['DOWN']

        self._name = 'Demon'

        self._speed_changing = 1
        self._speed_x = 0
        self._speed_y = 0

        self._amount_damage = random.randint(40, 50)
        self._amount_health = random.randint(80, 170)

    def update(self, surface):
        super().update()
        self._draw(surface)
        self._move()

        self._amount_damage = random.randint(40, 50)

    def _draw(self, surface):
        self._image = self._tile_set[self._current_direction_moving][
            self._current_number_image_in_animation]
        surface.blit(self._image, self._rect)

    def _move(self):
        random_direction = random.randint(0, 400)
        if random_direction in (0, 100):
            self._current_direction_moving = self._DIRECTIONS_MOVING['LEFT']
            self._speed_x = -self._speed_changing
        if random_direction in (100, 200):
            self._current_direction_moving = self._DIRECTIONS_MOVING['RIGHT']
            self._speed_x = self._speed_changing
        if random_direction in (200, 300):
            self._current_direction_moving = self._DIRECTIONS_MOVING['UP']
            self._speed_y = -self._speed_changing
        if random_direction in (300, 400):
            self._current_direction_moving = self._DIRECTIONS_MOVING['DOWN']
            self._speed_y = self._speed_changing

        self._rect.centerx += self._speed_x
        self._rect.centery += self._speed_y

    def attack(self, current_x_player, current_y_player):
        distance_reaction = random.randint(30, 150)
        current_distance_between_player_enemy = math.sqrt((current_x_player-self._rect.centerx)**2 +
                                                          (current_y_player-self._rect.centery)**2)
        if current_distance_between_player_enemy < distance_reaction:
            pass
        else:
            self._move()

    def get_rect(self):
        return self._rect

    def get_amount_damage(self):
        return self._amount_damage

    def get_amount_health(self):
        return self._amount_health

    def set_amount_health(self, new_value_health):
        self._amount_health = new_value_health

    def get_name(self):
        return self._name
