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

import game_enums
import constants
import fireball
import inventory
import bar


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

        self.__walking_speed = 3
        self.__running_speed = 4.5
        self.__speed_changing = self.__walking_speed
        self.__speed_x = 0
        self.__speed_y = 0

        self.__level = 1
        self.__experience_to_up_level = 1000 * pow(1.1, self.__level)
        self.__current_experience = 0

        self.__max_health = 100
        self.__current_health = 100
        self.__passive_amount_regeneration = 0.1
        self.__max_mana = 100
        self.__current_mana = 100
        self.__max_stamina = 100
        self.__current_stamina = self.__max_stamina

        self.__amount_damage = random.randint(10, 20)

        self.__inventory = inventory.Inventory()

        self.__active_effects = []

        self.__health_bar = bar.Bar(constants.GAME_WINDOW_WIDTH//2-constants.GAME_WINDOW_WIDTH//4,
                                    constants.GAME_WINDOW_HEIGHT - 96,
                                    game_enums.PlayerBarTypes.HEALTH.value)

        self.__mana_bar = bar.Bar(constants.GAME_WINDOW_WIDTH * 0.75-96,
                                  constants.GAME_WINDOW_HEIGHT - 96,
                                  game_enums.PlayerBarTypes.MANA.value)

    def update(self, surface):
        self.__draw(surface)
        self.__move()
        self.regeneration()

        self.__amount_damage = random.randint(10, 20)

        if self.__current_experience >= self.__experience_to_up_level:
            self.__level += 1
            self.__current_experience = self.__current_experience - self.__experience_to_up_level

    def __draw(self, surface):
        multiplier_change_animation_speed = 15
        if self.__current_number_image_in_animation == self.__amount_images_in_animation * constants.FPS_LOCKING // \
                multiplier_change_animation_speed:
            self.__current_number_image_in_animation = 0

        self.__image = self.__tile_set[self.__current_direction_moving][
            self.__current_number_image_in_animation // (constants.FPS_LOCKING // multiplier_change_animation_speed)]
        surface.blit(self.__image, self.__rect)
        self.__current_number_image_in_animation += 1

        self.__health_bar.update(surface, self.__current_health, self.__max_health)
        self.__mana_bar.update(surface, self.__current_mana, self.__max_mana)

    def __move(self):
        self.__speed_x = 0
        self.__speed_y = 0
        self.__speed_changing = self.__walking_speed

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LSHIFT] and self.__current_stamina >= 0:
            self.__speed_changing = self.__running_speed
            self.__current_stamina -= 0.5
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
        if self.__current_mana > 0:
            shell = fireball.Fireball(self.__rect.centerx, self.__rect.centery,
                                      (float(pygame.mouse.get_pos()[0] - self.__rect.centerx),
                                       float(pygame.mouse.get_pos()[1] - self.__rect.centery)))
            self.__current_mana -= 4
            return shell

    def regeneration(self, potion=None):
        if potion is None:
            self.__current_health += self.__passive_amount_regeneration
            self.__current_mana += self.__passive_amount_regeneration

            if self.__current_health > self.__max_health:
                self.__current_health = self.__max_health
            if self.__current_mana > self.__max_mana:
                self.__current_mana = self.__max_mana
        else:
            if potion.get_type() == 'health':
                self.__current_health += potion.get_regen_amount()
            elif potion.get_type() == 'mana':
                self.__current_mana += potion.get_regen_amount()
        if self.__current_stamina < 100:
            self.__current_stamina += 0.2
        if self.__current_stamina <= 0:
            self.__current_stamina = 0

    def append_thing_to_inventory(self, thing):
        self.__inventory.append_resource(thing)

    def show_inventory(self, surface):
        self.__inventory.draw_inventory(surface)

    def get_rect(self):
        return self.__rect

    def get_amount_mana(self):
        return self.__current_mana

    def get_amount_damage(self):
        return self.__amount_damage

    def get_amount_health(self):
        return self.__current_health

    def set_amount_health(self, new_value_health):
        self.__current_health = new_value_health

    def get_name(self):
        return self.__name

    def get_current_experience(self):
        return self.__current_experience

    def set_current_experience(self, new_value):
        self.__current_experience = new_value

    def get_experience_to_up_level(self):
        return self.__experience_to_up_level

    def get_level(self):
        return self.__level

    def get_current_stamina(self):
        return self.__current_stamina

    def get_max_stamina(self):
        return self.__max_stamina
