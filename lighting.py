import math
import random

import pygame

import constants


class Lighting(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, shooting_direction):
        super().__init__()
        self.__image = pygame.image.load('resources/images/shells/lighting/lightning_1.png').convert()
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__tile_set = [
                pygame.image.load('resources/images/shells/lighting/lightning_1.png').convert(),
                pygame.image.load('resources/images/shells/lighting/lightning_2.png').convert(),
                pygame.image.load('resources/images/shells/lighting/lightning_3.png').convert(),
                pygame.image.load('resources/images/shells/lighting/lightning_4.png').convert(),
                pygame.image.load('resources/images/shells/lighting/lightning_5.png').convert()
        ]
        self.__amount_images_in_animation = len(self.__tile_set)
        self.__current_number_image_in_animation = 0

        __length = math.sqrt(shooting_direction[0] ** 2 + shooting_direction[1] ** 2)
        if __length == 0:
            __length = 1
        self.__direction = (shooting_direction[0] / __length, shooting_direction[1] / __length)

        self.__speed_x = random.randint(5, 7)
        self.__speed_y = random.randint(5, 7)

        self.__amount_damage = random.randint(5, 10)

    def update(self, surface):
        self.__draw(surface)
        self.__move()

        self.__amount_damage = random.randint(5, 10)

    def __draw(self, surface):
        if self.__current_number_image_in_animation == self.__amount_images_in_animation:
            self.__current_number_image_in_animation = 0

        self.__image = self.__tile_set[self.__current_number_image_in_animation]
        surface.blit(self.__image, self.__rect)
        self.__current_number_image_in_animation += 1

    def __move(self):
        self._speed_x = random.randint(5, 7)
        self._speed_y = random.randint(5, 7)

        self.__rect.centerx += self.__direction[0] * self.__speed_x
        self.__rect.centery += self.__direction[1] * self.__speed_x

        if self.__rect.bottom < 0 or \
                self.__rect.left < 0 or \
                self.__rect.top > constants.GAME_WINDOW_HEIGHT or \
                self.__rect.right > constants.GAME_WINDOW_WIDTH:
            self.kill()

    @property
    def amount_additional_damage(self):
        return self.__amount_damage

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value