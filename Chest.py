import random

import pygame

from HealthPotion import HealthPotion
from Key import Key
from ManaPotion import ManaPotion
import Coin
import GameEnums
from GameObject import GameObject


class Chest(GameObject):
    def __init__(self, center_x, center_y, basic_image, is_chest_need_key):
        super().__init__(center_x, center_y, basic_image)
        self._need_key = is_chest_need_key
        self._amount_things_in_chest = random.randint(5, 10)
        self._is_chest_opened = False
        self._sound_creaking = pygame.mixer.Sound('resources/sounds/chest_creak.wav')

    def update(self, surface, *args, **kwargs):
        self._draw(surface)

    def _draw(self, surface, *args, **kwargs):
        surface.blit(self._image, self._rect)

    def open(self, is_player_has_key):
        if not self._is_chest_opened:
            if not self._need_key:
                self._image = pygame.image.load('resources/images/chests/opened_chest.png').convert()
                self._sound_creaking.play()
                self._is_chest_opened = True
                content = self._create_random_content()
                return content
            else:
                if is_player_has_key:
                    self._image = pygame.image.load('resources/images/chests/opened_chest_with_key.png').convert()
                    self._sound_creaking.play()
                    self._is_chest_opened = True
                    content = self._create_random_content()
                    return content

    def _create_random_content(self):
        def create_random_health_potion():
            volume = random.randint(0, 6)
            if volume == 0:
                return HealthPotion(random_x, random_y,
                                    'resources/images/potions/health/small_health_potion.png',
                                    GameEnums.PotionVolume.SMALL.value)
            elif volume == 1:
                return HealthPotion(random_x, random_y,
                                    'resources/images/potions/health/lesser_health_potion.png',
                                    GameEnums.PotionVolume.LESSER.value)
            elif volume == 2:
                return HealthPotion(random_x, random_y,
                                    'resources/images/potions/health/medium_health_potion.png',
                                    GameEnums.PotionVolume.MEDIUM.value)
            elif volume == 3:
                return HealthPotion(random_x, random_y,
                                    'resources/images/potions/health/greater_health_potion.png',
                                    GameEnums.PotionVolume.GREATER.value)
            elif volume == 4:
                return HealthPotion(random_x, random_y,
                                    'resources/images/potions/health/huge_health_potion.png',
                                    GameEnums.PotionVolume.HUGE.value)

        def create_random_mana_potion():
            volume = random.randint(0, 6)
            if volume == 0:
                return ManaPotion(random_x, random_y,
                                  'resources/images/potions/mana/small_mana_potion.png',
                                  GameEnums.PotionVolume.SMALL.value)
            elif volume == 1:
                return ManaPotion(random_x, random_y,
                                  'resources/images/potions/mana/lesser_mana_potion.png',
                                  GameEnums.PotionVolume.LESSER.value)
            elif volume == 2:
                return ManaPotion(random_x, random_y,
                                  'resources/images/potions/mana/medium_mana_potion.png',
                                  GameEnums.PotionVolume.MEDIUM.value)
            elif volume == 3:
                return ManaPotion(random_x, random_y,
                                  'resources/images/potions/mana/greater_mana_potion.png',
                                  GameEnums.PotionVolume.GREATER.value)
            elif volume == 4:
                return ManaPotion(random_x, random_y,
                                  'resources/images/potions/mana/huge_mana_potion.png',
                                  GameEnums.PotionVolume.HUGE.value)

        content_local = []
        for _ in range(self._amount_things_in_chest):
            random_thing = random.randint(0, 7)
            random_x = random.randint(self._rect.centerx - 20, self._rect.centerx + 20)
            random_y = random.randint(self._rect.centery + 10, self._rect.centery + 30)
            thing = 0
            if random_thing == 0:
                thing = create_random_health_potion()
            if random_thing == 1:
                thing = create_random_health_potion()
            if random_thing == 3:
                thing = Coin.Coin(random_x, random_y,
                                  'resources/images/coins/gold_coin.png',
                                  GameEnums.CoinTypes.GOLD)
            if random_thing == 4:
                thing = Coin.Coin(random_x, random_y,
                                  'resources/images/coins/silver_coin.png',
                                  GameEnums.CoinTypes.SILVER)
            if random_thing == 5:
                thing = Coin.Coin(random_x, random_y,
                                  'resources/images/coins/bronze_coin.png',
                                  GameEnums.CoinTypes.BRONZE)
            if random_thing == 6:
                thing = Key(random_x, random_y, basic_image='resources/images/chests/key.png')
            content_local.append(thing)
        return content_local
