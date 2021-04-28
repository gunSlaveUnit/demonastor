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

    def get_rect(self):
        return self.__rect
