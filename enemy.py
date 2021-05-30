import math
import random

import pygame

import bar
import constants
import fireball
import game_enums
import inventory
import lighting
from Character import Character


class Enemy(Character):
    def __init__(self, center_x, center_y, animation_images, player_level=1):
        super().__init__(center_x, center_y, animation_images)
        self._max_health = random.randint(200, 460)
        self._max_mana = self._max_stamina = 1000000
        self._level = player_level
        self._current_health = self._max_health
        self._current_stamina = self._max_stamina
        self._current_mana = self._max_mana
        self._speed_changing = 1
        self._amount_damage = random.randint(40, 50)
        self._passive_regeneration = 0.5
        self._last_regeneration_time = 300
        self._last_attack_time = 250
        self._last_changing_image_time = 250
        self._animation_interval = 150
        self._changing_direction_interval = 1000
        self._last_changing_direction_time = pygame.time.get_ticks()
        self._experience_for_killing = 100 * (10 + self._level - player_level) / (10 + player_level)
        self._is_angry = False
        self._name = 'Demon'

    def update(self, surface, *args, **kwargs):
        self._regeneration()
        self._draw(surface)
        self._move()
        self._recount_damage()

    def _recount_damage(self):
        self._amount_damage = random.randint(40, 50)

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

    def _move(self, *args, **kwargs):
        now = pygame.time.get_ticks()
        if now - self._last_changing_direction_time > self._changing_direction_interval:
            self._last_changing_direction_time = now
            random_direction = random.randint(0, 4)
            if random_direction == 0:
                self._current_direction_moving = self._DIRECTIONS_MOVING['LEFT']
                self._speed_x = -self._speed_changing
            elif random_direction == 1:
                self._current_direction_moving = self._DIRECTIONS_MOVING['RIGHT']
                self._speed_x = self._speed_changing
            elif random_direction == 2:
                self._current_direction_moving = self._DIRECTIONS_MOVING['UP']
                self._speed_y = -self._speed_changing
            elif random_direction == 3:
                self._current_direction_moving = self._DIRECTIONS_MOVING['DOWN']
                self._speed_y = self._speed_changing

        self._rect.centerx += self._speed_x
        self._rect.centery += self._speed_y

    def attack(self, current_x_player, current_y_player):
        distance_reaction = random.randint(100, 170)
        dx = float(current_x_player - self._rect.centerx)
        dy = float(current_y_player - self._rect.centery)
        length = math.sqrt(dx ** 2 + dy ** 2)
        if int(length) == 0:
            length = 1
        if length <= distance_reaction or self._is_angry:
            self.show_aggression_to_attack_player(dx, dy, length)
        else:
            self._move()

    def show_aggression_to_attack_player(self, dx, dy, length):
        direction_to_player = (dx / length, dy / length)
        if direction_to_player[0] < 0.0:
            self._current_direction_moving = self._DIRECTIONS_MOVING['LEFT']
        if direction_to_player[0] > 0.0:
            self._current_direction_moving = self._DIRECTIONS_MOVING['RIGHT']
        if direction_to_player[1] < 0.0:
            self._current_direction_moving = self._DIRECTIONS_MOVING['UP']
        if direction_to_player[1] > 0.0:
            self._current_direction_moving = self._DIRECTIONS_MOVING['DOWN']
        self._rect.centerx += direction_to_player[0] * random.randint(2, 3)
        self._rect.centery += direction_to_player[1] * random.randint(2, 3)

    @property
    def amount_damage(self):
        return self._amount_damage

    @property
    def current_amount_health(self):
        return self._current_health

    @property
    def max_amount_health(self):
        return self._max_health

    @current_amount_health.setter
    def current_amount_health(self, new_value):
        self._current_health = new_value

    @property
    def name(self):
        return self._name

    @property
    def experience_for_killing(self):
        return self._experience_for_killing

    @property
    def is_enemy_angry(self):
        return self._is_angry

    @is_enemy_angry.setter
    def is_enemy_angry(self, new_value):
        self._is_angry = new_value
