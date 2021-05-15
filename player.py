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
import lighting


class Player(pygame.sprite.Sprite):
    __DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, init_center_x, init_center_y, saved_params=None):
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

        self.__max_stamina = 100
        self.__max_mana = 100
        if saved_params is None:
            self.__level = 1
            self.__current_experience = 0
            self.__current_health = 100
            self.__current_stamina = self.__max_stamina
            self.__current_mana = self.__max_mana
        else:
            self.__level = saved_params['level']
            self.__current_experience = saved_params['current_experience']
            self.__current_health = saved_params['current_health']
            self.__current_stamina = saved_params['current_stamina']
            self.__current_mana = saved_params['current_mana']

        self.__experience_to_up_level = 1000 * pow(1.1, self.__level)

        self.__max_health = 100

        self.__passive_amount_regeneration = 0.1

        self.__amount_damage = random.randint(140, 200)

        self.__inventory = inventory.Inventory()

        self.__active_effects = []

        self.__health_bar = bar.Bar(constants.GAME_WINDOW_WIDTH//2-constants.GAME_WINDOW_WIDTH//4,
                                    constants.GAME_WINDOW_HEIGHT - 96,
                                    game_enums.PlayerBarTypes.HEALTH.value)

        self.__mana_bar = bar.Bar(constants.GAME_WINDOW_WIDTH * 0.75-96,
                                  constants.GAME_WINDOW_HEIGHT - 96,
                                  game_enums.PlayerBarTypes.MANA.value)

        self.__selected_weapon = 0

    def update(self, surface):
        self.__draw(surface)
        self.__move()
        self.regeneration()

        self.__amount_damage = random.randint(140, 200)
        self.__experience_to_up_level = 1000 * pow(1.1, self.__level)

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
            if self.__selected_weapon == 0:
                shell = fireball.Fireball(self.__rect.centerx, self.__rect.centery,
                                          (float(pygame.mouse.get_pos()[0] - self.__rect.centerx),
                                           float(pygame.mouse.get_pos()[1] - self.__rect.centery)))
                self.__current_mana -= 4
                return [shell]
            else:
                shell_1 = lighting.Lighting(self.__rect.centerx, self.__rect.centery,
                                          (float(pygame.mouse.get_pos()[0] - self.__rect.centerx),
                                           float(pygame.mouse.get_pos()[1] - self.__rect.centery)))
                shell_2 = lighting.Lighting(self.__rect.centerx, self.__rect.centery,
                                            (float(pygame.mouse.get_pos()[0]-50 - self.__rect.centerx),
                                             float(pygame.mouse.get_pos()[1]-50 - self.__rect.centery)))
                shell_3 = lighting.Lighting(self.__rect.centerx, self.__rect.centery,
                                            (float(pygame.mouse.get_pos()[0]-50 - self.__rect.centerx),
                                             float(pygame.mouse.get_pos()[1]+50 - self.__rect.centery)))
                shell_4 = lighting.Lighting(self.__rect.centerx, self.__rect.centery,
                                            (float(pygame.mouse.get_pos()[0]+50 - self.__rect.centerx),
                                             float(pygame.mouse.get_pos()[1]-50 - self.__rect.centery)))
                shell_5 = lighting.Lighting(self.__rect.centerx, self.__rect.centery,
                                            (float(pygame.mouse.get_pos()[0]+50 - self.__rect.centerx),
                                             float(pygame.mouse.get_pos()[1]+50 - self.__rect.centery)))
                self.__current_mana -= 20
                return [shell_1, shell_2, shell_3, shell_4, shell_5]
        return []

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

    def is_key_in_inventory(self):
        return self.__inventory.get_key_for_chest()

    def change_weapon(self):
        self.__selected_weapon += 1
        if self.__selected_weapon > 1:
            self.__selected_weapon = 0

    @property
    def params_for_saving(self):
        return {
            'level': self.__level,
            'current_experience': self.__current_experience,
            'current_health': self.__current_health,
            'current_mana': self.__current_mana,
            'current_stamina': self.__current_stamina
        }

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value

    @property
    def amount_mana(self):
        return self.__current_mana

    @property
    def amount_damage(self):
        return self.__amount_damage

    @property
    def amount_health(self):
        return self.__current_health

    @amount_health.setter
    def amount_health(self, new_value_health):
        self.__current_health = new_value_health

    @property
    def name(self):
        return self.__name

    @property
    def current_experience(self):
        return self.__current_experience

    @current_experience.setter
    def current_experience(self, new_value):
        self.__current_experience = new_value

    @property
    def experience_to_up_level(self):
        return self.__experience_to_up_level

    @property
    def level(self):
        return self.__level

    @property
    def current_stamina(self):
        return self.__current_stamina

    @property
    def max_stamina(self):
        return self.__max_stamina
