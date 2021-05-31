import random

import pygame

import Bar
import Constants
import Fireball
import GameEnums
import Inventory
import Lighting
import Textures
from Character import Character


class Player(Character):
    def __init__(self, center_x, center_y, animation_images, saved_params=None):
        super().__init__(center_x, center_y, animation_images)
        self._max_health = self._max_mana = self._max_stamina = 100
        self._speed_changing = 3
        self._amount_damage = random.randint(140, 200)
        self._passive_regeneration = 0.1
        self._regeneration_interval = 10
        self._last_attack_time = 250
        self._animation_interval = 150
        self._experience_up_level = 1000 * pow(1.1, self._level)
        self._selected_attack = GameEnums.AttackTypes.FIREBALL.value
        self._inventory = Inventory.Inventory()
        self._health_bar = Bar.Bar(Constants.GAME_WINDOW_WIDTH // 2 - 250,
                                   Constants.GAME_WINDOW_HEIGHT - 96, 'resources/images/bars/health_bar.png')
        self._mana_bar = Bar.Bar(Constants.GAME_WINDOW_WIDTH // 2 + 155,
                                 Constants.GAME_WINDOW_HEIGHT - 96, 'resources/images/bars/mana_bar.png')
        if saved_params is None:
            self._level = 1
            self._current_experience = 0
            self._current_health = 100
            self._current_stamina = self._max_stamina
            self._current_mana = self._max_mana
        else:
            self._level = saved_params['level']
            self._current_experience = saved_params['current_experience']
            self._current_health = saved_params['current_health']
            self._current_stamina = saved_params['current_stamina']
            self._current_mana = saved_params['current_mana']

    def update(self, surface, *args, **kwargs):
        self._regeneration()
        self._draw(surface)
        self._move()
        self._recount_experience_and_level()
        self._recount_damage()
        self._health_bar.update(surface, self._current_health, self._max_health)
        self._mana_bar.update(surface, self._current_mana, self._max_mana)

    def _recount_experience_and_level(self):
        if self._current_experience >= self._experience_up_level:
            self._level += 1
            self._current_experience = self._current_experience - self._experience_up_level
        self._experience_up_level = 1000 * pow(1.1, self._level)

    def _recount_damage(self):
        self._amount_damage = random.randint(140, 200)

    def _move(self, *args, **kwargs):
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

        if self._speed_x == 0 and self._speed_y == 0:
            self._current_number_image_in_animation = 0

        self._rect.centerx += self._speed_x
        self._rect.centery += self._speed_y

    def attack(self):
        now = pygame.time.get_ticks()
        if self._current_mana > 0 and now - self._last_attack_time > self._attack_interval:
            self._last_attack_time = now
            if self._selected_attack == GameEnums.AttackTypes.FIREBALL.value:
                shell = Fireball.Fireball(self._rect.centerx, self._rect.centery,
                                          'resources/images/shells/fireball.png',
                                          (float(pygame.mouse.get_pos()[0] - self._rect.centerx),
                                           float(pygame.mouse.get_pos()[1] - self._rect.centery)))
                self._current_mana -= 4
                return [shell]
            else:
                shell_1 = Lighting.Lighting(self._rect.centerx, self._rect.centery,
                                            animation_images=Textures.LIGHTING,
                                            shooting_direction=(
                                                float(pygame.mouse.get_pos()[0] - self._rect.centerx),
                                                float(pygame.mouse.get_pos()[1] - self._rect.centery))
                                            )
                shell_2 = Lighting.Lighting(self._rect.centerx, self._rect.centery,
                                            animation_images=Textures.LIGHTING,
                                            shooting_direction=(
                                                float(pygame.mouse.get_pos()[0] - 50 - self._rect.centerx),
                                                float(pygame.mouse.get_pos()[1] - 50 - self._rect.centery))
                                            )
                shell_3 = Lighting.Lighting(self._rect.centerx, self._rect.centery,
                                            animation_images=Textures.LIGHTING,
                                            shooting_direction=(
                                                float(pygame.mouse.get_pos()[0] - 50 - self._rect.centerx),
                                                float(pygame.mouse.get_pos()[1] + 50 - self._rect.centery))
                                            )
                shell_4 = Lighting.Lighting(self._rect.centerx, self._rect.centery,
                                            animation_images=Textures.LIGHTING,
                                            shooting_direction=(
                                                float(pygame.mouse.get_pos()[0] + 50 - self._rect.centerx),
                                                float(pygame.mouse.get_pos()[1] - 50 - self._rect.centery))
                                            )
                shell_5 = Lighting.Lighting(self._rect.centerx, self._rect.centery,
                                            animation_images=Textures.LIGHTING,
                                            shooting_direction=(
                                                float(pygame.mouse.get_pos()[0] + 50 - self._rect.centerx),
                                                float(pygame.mouse.get_pos()[1] + 50 - self._rect.centery))
                                            )
                self._current_mana -= 20
                return [shell_1, shell_2, shell_3, shell_4, shell_5]
        return []

    def append_thing_to_inventory(self, thing):
        self._inventory.append_resource(thing)

    def show_inventory(self, surface):
        self._inventory.draw_inventory(surface)

    def is_key_in_inventory(self):
        return self._inventory.get_key_for_chest()

    def change_weapon(self):
        self._selected_attack += 1
        if self._selected_attack > 1:
            self._selected_attack = 0

    @property
    def current_experience(self):
        return self._current_experience

    @current_experience.setter
    def current_experience(self, new_value):
        self._current_experience = new_value

    @property
    def experience_up_level(self):
        return self._experience_up_level

    @property
    def params_for_saving(self):
        return {
            'level': self._level,
            'current_experience': self._current_experience,
            'current_health': self._current_health,
            'current_mana': self._current_mana,
            'current_stamina': self._current_stamina
        }
