import math
import random

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
        self._passive_regeneration = 1
        self._regeneration_interval = 0.5
        self._attack_interval = 500
        self._animation_interval = 150
        self._changing_direction_interval = 1000
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
        if length == 0:
            length = 1
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
    def experience_for_killing(self):
        return self._experience_for_killing

    @property
    def is_enemy_angry(self):
        return self._is_angry

    @is_enemy_angry.setter
    def is_enemy_angry(self, new_value):
        self._is_angry = new_value
