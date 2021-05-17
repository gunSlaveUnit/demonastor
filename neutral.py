import random

import pygame.sprite

import constants
import quest
import quest_mark


class Neutral(pygame.sprite.Sprite):
    __DIRECTIONS_MOVING = {'LEFT': 0, 'RIGHT': 1, 'UP': 2, 'DOWN': 3}

    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self.__image = pygame.image.load('resources/images/characters/neutral_down_0.png').convert()
        self.__rect = self.rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__tile_set = [
            [
                pygame.image.load('resources/images/characters/neutral_left_0.png').convert(),
                pygame.image.load('resources/images/characters/neutral_left_1.png').convert(),
                pygame.image.load('resources/images/characters/neutral_left_3.png').convert(),
                pygame.image.load('resources/images/characters/neutral_left_2.png').convert()
            ],
            [
                pygame.image.load('resources/images/characters/neutral_right_0.png').convert(),
                pygame.image.load('resources/images/characters/neutral_right_1.png').convert(),
                pygame.image.load('resources/images/characters/neutral_right_3.png').convert(),
                pygame.image.load('resources/images/characters/neutral_right_2.png').convert()
            ],
            [
                pygame.image.load('resources/images/characters/neutral_up_0.png').convert(),
                pygame.image.load('resources/images/characters/neutral_up_1.png').convert(),
                pygame.image.load('resources/images/characters/neutral_up_2.png').convert(),
                pygame.image.load('resources/images/characters/neutral_up_2.png').convert()
            ],
            [
                pygame.image.load('resources/images/characters/neutral_down_0.png').convert(),
                pygame.image.load('resources/images/characters/neutral_down_1.png').convert(),
                pygame.image.load('resources/images/characters/neutral_down_3.png').convert(),
                pygame.image.load('resources/images/characters/neutral_down_2.png').convert()
            ],

        ]
        self.__amount_images_in_animation = len(self.__tile_set[0])
        self.__current_number_image_in_animation = 0
        self.__current_direction_moving = self.__DIRECTIONS_MOVING['DOWN']

        self.__speed_changing = 1
        self.__speed_x = 0
        self.__speed_y = 0

        self.__is_has_quest = True
        if self.__is_has_quest:
            self.__quests = [quest.Quest()]
            self.__quest_mark = quest_mark.QuestMark(self.__rect.centerx, self.__rect.top - 10)

    def update(self, surface):
        self.__draw(surface)
        self.__move()

        self.__quest_mark.rect.centerx = self.__rect.centerx
        self.__quest_mark.rect.centery = self.__rect.top - 10
        if self.__quests:
            self.__quest_mark.update(surface)

    def __draw(self, surface):
        multiplier_change_animation_speed = 15
        if self.__current_number_image_in_animation == self.__amount_images_in_animation * constants.FPS_LOCKING // \
                multiplier_change_animation_speed:
            self.__current_number_image_in_animation = 0

        self.__image = self.__tile_set[self.__current_direction_moving][
            self.__current_number_image_in_animation // (constants.FPS_LOCKING // multiplier_change_animation_speed)]
        surface.blit(self.__image, self.__rect)
        self.__current_number_image_in_animation += 1

    def __move(self):
        random_direction = random.randint(0, 400)
        if random_direction in (0, 100):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['LEFT']
            self.__speed_x = -self.__speed_changing
        if random_direction in (100, 200):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['RIGHT']
            self.__speed_x = self.__speed_changing
        if random_direction in (200, 300):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['UP']
            self.__speed_y = -self.__speed_changing
        if random_direction in (300, 400):
            self.__current_direction_moving = self.__DIRECTIONS_MOVING['DOWN']
            self.__speed_y = self.__speed_changing

        if self.__speed_x == 0 and self.__speed_y == 0:
            self.__current_number_image_in_animation = 0

        self.__rect.centerx += self.__speed_x
        self.__rect.centery += self.__speed_y

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value

    @property
    def quest(self):
        if self.__quests:
            return self.__quests.pop(0)

    def quest_mark(self):
        return self.__quest_mark
