import random

import pygame

from healthpotion import HealthPotion
from manapotion import ManaPotion
import constants


class Chest(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, is_chest_need_key):
        super().__init__()

        self.__image = pygame.image.load('resources/images/chests/closed_chest.png').convert()
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__amount_things_in_chest = random.randint(0, 3)
        self.__is_chest_opened = False
        self.__need_key = is_chest_need_key
        self.__sound_creaking = pygame.mixer.Sound('resources/sounds/chest_creak.wav')

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, self.__rect)

    def open(self):
        if not self.__is_chest_opened:
            if not self.__need_key:
                self.__image = pygame.image.load('resources/images/chests/opened_chest.png').convert()
                self.__sound_creaking.play()
                self.__is_chest_opened = True
                content = self.__create_random_content()
                return content
            else:
                pass

    def __create_random_content(self):
        content_local = []
        for _ in range(self.__amount_things_in_chest):
            random_thing = random.randint(0, 2)
            random_x = random.randint(self.__rect.centerx - 20, self.__rect.centerx + 20)
            random_y = random.randint(self.__rect.centery + 10, self.__rect.centery + 30)
            thing = 0
            if random_thing == 0:
                thing = HealthPotion(random_x, random_y)
            if random_thing == 1:
                thing = ManaPotion(random_x, random_y)
            content_local.append(thing)
        return content_local



    def get_rect(self):
        return self.__rect
