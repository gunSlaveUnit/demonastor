"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

File contains a description of Demon class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import random
import math

import pygame


class Demon(pygame.sprite.Sprite):
    __DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, init_center_x, init_center_y, player_level):
        super().__init__()
        self.__image = pygame.image.load('resources/images/enemy/enemy_moving_down.png').convert()
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__tile_set = [
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
        self.__amount_images_in_animation = len(self.__tile_set[0])
        self.__current_number_image_in_animation = 0
        self.__current_direction_moving = self.__DIRECTIONS_MOVING['DOWN']

        self.__name = 'Demon'

        self.__speed_changing = 1
        self.__speed_x = 0
        self.__speed_y = 0

        self.__amount_damage = random.randint(40, 50)
        self.__max_amount_health = random.randint(80, 170)
        self.__current_amount_health = self.__max_amount_health

        self.__level = player_level
        self.__experience_for_killing = 100 * (10 + self.__level - player_level)/(10 + player_level)

        self.__is_angry = False

    def update(self, surface):
        self.__draw(surface)

        self.__amount_damage = random.randint(40, 50)

    def __draw(self, surface):
        self.__image = self.__tile_set[self.__current_direction_moving][
            self.__current_number_image_in_animation]
        surface.blit(self.__image, self.__rect)

    def __move(self):
        random_direction = random.randint(0, 400)
        if random_direction in (0, 100):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['LEFT']
            self.__speed_x = -self.__speed_changing
        if random_direction in (100, 200):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['RIGHT']
            self.__speed_x = self.__speed_changing
        if random_direction in (200, 300):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['UP']
            self.__speed_y = -self.__speed_changing
        if random_direction in (300, 400):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['DOWN']
            self.__speed_y = self.__speed_changing

        self.__rect.centerx += self.__speed_x
        self.__rect.centery += self.__speed_y

    def attack(self, current_x_player, current_y_player):
        distance_reaction = random.randint(100, 170)
        dx = float(current_x_player - self.__rect.centerx)
        dy = float(current_y_player - self.__rect.centery)
        length = math.sqrt(dx**2 + dy**2)
        if length == 0:
            length = 1
        if length <= distance_reaction or self.__is_angry:
            self.show_aggression_to_attack_player(dx, dy, length)
        else:
            self.__move()

    def show_aggression_to_attack_player(self, dx, dy, length):
        direction_to_player = (dx / length, dy / length)
        if direction_to_player[0] < 0.0:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['LEFT']
        if direction_to_player[0] > 0.0:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['RIGHT']
        if direction_to_player[1] < 0.0:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['UP']
        if direction_to_player[1] > 0.0:
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['DOWN']
        self.__rect.centerx += direction_to_player[0] * random.randint(2, 3)
        self.__rect.centery += direction_to_player[1] * random.randint(2, 3)

    def get_rect(self):
        return self.__rect

    def get_amount_damage(self):
        return self.__amount_damage

    def get_current_amount_health(self):
        return self.__current_amount_health

    def get_max_amount_health(self):
        return self.__max_amount_health

    def set_amount_health(self, new_value_health):
        self.__current_amount_health = new_value_health

    def get_name(self):
        return self.__name

    def get_experience_for_killing(self):
        return self.__experience_for_killing

    def set_is_enemy_angry(self, new_value):
        self.__is_angry = new_value
