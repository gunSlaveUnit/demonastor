# ! usr/bin/env python3
# -*- coding: utf8 -*-

import pygame


class Waterfall(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self.__image = pygame.image.load('resources/images/waterfall/waterfall_1.png')
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__tile_set = [
                pygame.image.load('resources/images/waterfall/waterfall_1.png'),
                pygame.image.load('resources/images/waterfall/waterfall_2.png'),
                pygame.image.load('resources/images/waterfall/waterfall_3.png'),
                pygame.image.load('resources/images/waterfall/waterfall_4.png')
        ]
        self.__amount_images_in_animation = len(self.__tile_set)
        self.__current_number_image_in_animation = 0

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        if self.__current_number_image_in_animation == self.__amount_images_in_animation*2:
            self.__current_number_image_in_animation = 0

        self.__image = self.__tile_set[self.__current_number_image_in_animation//2]
        surface.blit(self.__image, self.__rect)
        self.__current_number_image_in_animation += 1

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value
