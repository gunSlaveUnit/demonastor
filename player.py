"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2
File contains a description of Player class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

# TODO: It's necessary to link the player's movement speed and animation speed to the FPS limit
# TODO: stop animation when moving keys aren't pressed

import random

import pygame

import constants
import fireball


class Player(pygame.sprite.Sprite):
    _DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self._image = pygame.image.load('Player/PlayerDownMoving0.png').convert()
        self._rect = self.rect = self._image.get_rect()
        self._rect.centerx = init_center_x
        self._rect.centery = init_center_y
        self._tile_set = [
            [
                pygame.image.load('Player/PlayerLeftMoving0.png').convert(),
                pygame.image.load('Player/PlayerLeftMoving1.png').convert(),
                pygame.image.load('Player/PlayerLeftMoving2.png').convert(),
                pygame.image.load('Player/PlayerLeftMoving3.png').convert()
            ],
            [
                pygame.image.load('Player/PlayerRightMoving0.png').convert(),
                pygame.image.load('Player/PlayerRightMoving1.png').convert(),
                pygame.image.load('Player/PlayerRightMoving2.png').convert(),
                pygame.image.load('Player/PlayerRightMoving3.png').convert()
            ],
            [
                pygame.image.load('Player/PlayerUpMoving0.png').convert(),
                pygame.image.load('Player/PlayerUpMoving1.png').convert(),
                pygame.image.load('Player/PlayerUpMoving2.png').convert(),
                pygame.image.load('Player/PlayerUpMoving3.png').convert()
            ],
            [
                pygame.image.load('Player/PlayerDownMoving0.png').convert(),
                pygame.image.load('Player/PlayerDownMoving1.png').convert(),
                pygame.image.load('Player/PlayerDownMoving2.png').convert(),
                pygame.image.load('Player/PlayerDownMoving3.png').convert()
            ],

        ]
        self._amount_images_in_animation = len(self._tile_set[0])
        self._current_number_image_in_animation = 0
        self._current_direction_moving = Player._DIRECTIONS_MOVING['DOWN']

        self._name = 'Nickname'

        self._speed_changing = 2
        self._speed_x = 0
        self._speed_y = 0

        self._amount_damage = random.randint(10, 20)
        self._amount_health = 100

    def update(self, surface):
        super().update()
        self._draw(surface)
        self._move()

        self._amount_damage = random.randint(10, 20)

    def _draw(self, surface):
        if self._current_number_image_in_animation == constants.FPS_LOCKING:
            self._current_number_image_in_animation = 0

        self._image = self._tile_set[self._current_direction_moving][
            self._current_number_image_in_animation // (constants.FPS_LOCKING // self._amount_images_in_animation)]
        surface.blit(self._image, self._rect)
        self._current_number_image_in_animation += 1

    def _move(self):
        self._speed_x = 0
        self._speed_y = 0

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self._current_direction_moving = self._DIRECTIONS_MOVING['LEFT']
            self._speed_x = -self._speed_changing
        if key_state[pygame.K_d]:
            self._current_direction_moving = self._DIRECTIONS_MOVING['RIGHT']
            self._speed_x = self._speed_changing
        if key_state[pygame.K_w]:
            self._current_direction_moving = self._DIRECTIONS_MOVING['UP']
            self._speed_y = -self._speed_changing
        if key_state[pygame.K_s]:
            self._current_direction_moving = self._DIRECTIONS_MOVING['DOWN']
            self._speed_y = self._speed_changing

        self._rect.centerx += self._speed_x
        self._rect.centery += self._speed_y

    def attack(self):
        shell = fireball.Fireball(self._rect.centerx, self._rect.centery,
                                      (float(pygame.mouse.get_pos()[0] - self._rect.centerx),
                                       float(pygame.mouse.get_pos()[1] - self._rect.centery)))
        return shell

    def get_rect(self):
        return self._rect

    def get_amount_damage(self):
        return self._amount_damage

    def get_amount_health(self):
        return self._amount_health

    def set_amount_health(self, new_value_health):
        self._amount_health = new_value_health
