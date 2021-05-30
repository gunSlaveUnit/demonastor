import random

import quest
import quest_mark
from Character import Character


class Neutral(Character):
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
        self._name = 'Beatrice'
        self._is_has_quest = True
        self._vision_quest_mark = True
        if self._is_has_quest:
            self._quest = quest.Quest(self._level)
            self._quest_mark = quest_mark.QuestMark(self._rect.centerx, self._rect.top - 10)

    def update(self, surface, *args, **kwargs):
        self._regeneration()
        self._draw(surface)
        self._move()
        self._recount_damage()
        self._update_quest_mark(surface)

    def _update_quest_mark(self, surface):
        self._quest_mark.rect.centerx = self._rect.centerx
        self._quest_mark.rect.centery = self._rect.top - 10
        if self._quest and self._vision_quest_mark:
            self._quest_mark.update(surface)

    def _recount_damage(self):
        self._amount_damage = random.randint(40, 50)

    @property
    def quest(self):
        if self._quest:
            return self._quest

    @property
    def quest_mark(self):
        return self._quest_mark

    @property
    def vision_quest_mark(self):
        return self._vision_quest_mark

    @vision_quest_mark.setter
    def vision_quest_mark(self, new_value):
        self._vision_quest_mark = new_value
