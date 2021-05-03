import random

import pygame

from healthpotion import HealthPotion
from manapotion import ManaPotion
import coin
import game_enums


class Chest(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, is_chest_need_key):
        super().__init__()
        self.__need_key = is_chest_need_key
        self.__image = self.__get_image()
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__amount_things_in_chest = random.randint(0, 10)
        self.__is_chest_opened = False
        self.__sound_creaking = pygame.mixer.Sound('resources/sounds/chest_creak.wav')

    def __get_image(self):
        if self.__need_key:
            return pygame.image.load('resources/images/chests/chest_with_key.png')
        else:
            return pygame.image.load('resources/images/chests/closed_chest.png').convert()

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, self.__rect)

    def open(self, is_player_has_key):
        if not self.__is_chest_opened:
            if not self.__need_key:
                self.__image = pygame.image.load('resources/images/chests/opened_chest.png').convert()
                self.__sound_creaking.play()
                self.__is_chest_opened = True
                content = self.__create_random_content()
                return content
            else:
                if is_player_has_key:
                    self.__image = pygame.image.load('resources/images/chests/opened_chest_with_key.png').convert()
                    self.__sound_creaking.play()
                    self.__is_chest_opened = True
                    content = self.__create_random_content()
                    return content

    def __create_random_content(self):
        content_local = []
        for _ in range(self.__amount_things_in_chest):
            random_thing = random.randint(1, 20)
            random_x = random.randint(self.__rect.centerx - 20, self.__rect.centerx + 20)
            random_y = random.randint(self.__rect.centery + 10, self.__rect.centery + 30)
            thing = 0
            if random_thing == 0:
                thing = HealthPotion(random_x, random_y)
            if random_thing == 1:
                thing = ManaPotion(random_x, random_y)
            if random_thing == 3:
                thing = coin.Coin(random_x, random_y, game_enums.CoinTypes.GOLD)
            if random_thing == 4:
                thing = coin.Coin(random_x, random_y, game_enums.CoinTypes.SILVER)
            if random_thing == 5:
                thing = coin.Coin(random_x, random_y, game_enums.CoinTypes.BRONZE)
            content_local.append(thing)
        return content_local

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value
