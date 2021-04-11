"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

File contains a description of Player class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import random

import pygame

import constants
import fireball


class Player(pygame.sprite.Sprite):
    __DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self.__image = pygame.image.load('resources/images/player/player_down_moving_0.png').convert()
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__tile_set = [
            [
                pygame.image.load('resources/images/player/player_left_moving_0.png').convert(),
                pygame.image.load('resources/images/player/player_left_moving_1.png').convert(),
                pygame.image.load('resources/images/player/player_left_moving_2.png').convert(),
                pygame.image.load('resources/images/player/player_left_moving_3.png').convert()
            ],
            [
                pygame.image.load('resources/images/player/player_right_moving_0.png').convert(),
                pygame.image.load('resources/images/player/player_right_moving_1.png').convert(),
                pygame.image.load('resources/images/player/player_right_moving_2.png').convert(),
                pygame.image.load('resources/images/player/player_right_moving_3.png').convert()
            ],
            [
                pygame.image.load('resources/images/player/player_up_moving_0.png').convert(),
                pygame.image.load('resources/images/player/player_up_moving_1.png').convert(),
                pygame.image.load('resources/images/player/player_up_moving_2.png').convert(),
                pygame.image.load('resources/images/player/player_up_moving_3.png').convert()
            ],
            [
                pygame.image.load('resources/images/player/player_down_moving_0.png').convert(),
                pygame.image.load('resources/images/player/player_down_moving_1.png').convert(),
                pygame.image.load('resources/images/Player/player_down_moving_2.png').convert(),
                pygame.image.load('resources/images/Player/player_down_moving_3.png').convert()
            ],

        ]
        self.__amount_images_in_animation = len(self.__tile_set[0])
        self.__current_number_image_in_animation = 0
        self.__current_direction_moving = self.__DIRECTIONS_MOVING['UP']
        self.__last_pressed_key = pygame.K_w

        self.__name = 'Bonobo'

        self.__speed_changing = 3
        self.__speed_x = 0
        self.__speed_y = 0

        self.__amount_damage = random.randint(10, 20)
        self.__amount_health = 100

    def update(self, surface):
        self.__draw(surface)
        self.__move()

        self.__amount_damage = random.randint(10, 20)

    def __draw(self, surface):
        multiplier_change_animation_speed = 15
        if self.__current_number_image_in_animation == self.__amount_images_in_animation * constants.FPS_LOCKING // \
                multiplier_change_animation_speed:
            self.__current_number_image_in_animation = 0

        self.__image = self.__tile_set[self.__current_direction_moving][
            self.__current_number_image_in_animation // (constants.FPS_LOCKING // multiplier_change_animation_speed)]
        surface.blit(self.__image, self.__rect)
        self.__current_number_image_in_animation += 1

    def __move(self):
        self.__speed_x = 0
        self.__speed_y = 0

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['LEFT']
            self.__speed_x = -self.__speed_changing
        if key_state[pygame.K_d]:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['RIGHT']
            self.__speed_x = self.__speed_changing
        if key_state[pygame.K_w]:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['UP']
            self.__speed_y = -self.__speed_changing
        if key_state[pygame.K_s]:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['DOWN']
            self.__speed_y = self.__speed_changing

        if self.__speed_x == 0 and self.__speed_y == 0:
            self.__current_number_image_in_animation = 0

        self.__rect.centerx += self.__speed_x
        self.__rect.centery += self.__speed_y

    def attack(self):
        shell = fireball.Fireball(self.__rect.centerx, self.__rect.centery,
                                  (float(pygame.mouse.get_pos()[0] - self.__rect.centerx),
                                   float(pygame.mouse.get_pos()[1] - self.__rect.centery)))
        return shell

    def get_rect(self):
        return self.__rect

    def get_amount_damage(self):
        return self.__amount_damage

    def get_amount_health(self):
        return self.__amount_health

    def set_amount_health(self, new_value_health):
        self.__amount_health = new_value_health

    def get_name(self):
        return self.__name
