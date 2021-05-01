"""
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

File contains a description of Inventory class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import sys

import pygame

import constants
import game_enums
import coin


class Inventory:
    def __init__(self):
        self.__resources = {
            'gold_coin': 0,
            'silver_coin': 0,
            'bronze_coin': 0
        }
        self.__width = 480
        self.__height = 320
        self.__frame_thickness = 3
        self.__inventory_rect = pygame.Rect(constants.GAME_WINDOW_WIDTH//2-self.__width//2,
                                            constants.GAME_WINDOW_HEIGHT//2-self.__height//2,
                                            self.__width, self.__height)

        self.__player_money = [
            [
                coin.Coin(constants.GAME_WINDOW_WIDTH//2-self.__width//2+20,
                          constants.GAME_WINDOW_HEIGHT//2+self.__height//2-20,
                          game_enums.CoinTypes.GOLD)
            ],
            [
                coin.Coin(constants.GAME_WINDOW_WIDTH//2 - 30,
                          constants.GAME_WINDOW_HEIGHT//2+self.__height//2-20,
                          game_enums.CoinTypes.SILVER)
            ],
            [
                coin.Coin(constants.GAME_WINDOW_WIDTH//2+self.__width//2-70,
                          constants.GAME_WINDOW_HEIGHT//2+self.__height//2-20,
                          game_enums.CoinTypes.BRONZE)
            ]
        ]

    def append_resource(self, resource_to_add):
        if resource_to_add.get_resource_name() in self.__resources:
            self.__resources[resource_to_add.get_resource_name()] += 1
        else:
            self.__resources[resource_to_add.get_resource_name()] = 1
        print(self.__resources)

    def draw_inventory(self, surface):
        pygame.draw.rect(surface, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                         self.__inventory_rect, self.__frame_thickness)

        pygame.draw.line(surface, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                         (constants.GAME_WINDOW_WIDTH//2-self.__width//2,
                          constants.GAME_WINDOW_HEIGHT//2+self.__height//2-self.__height//10-7),
                         (constants.GAME_WINDOW_WIDTH//2+self.__width//2,
                          constants.GAME_WINDOW_HEIGHT//2+self.__height//2-self.__height//10-7),
                         3)

        x_up, y_up, x_down, y_down = (constants.GAME_WINDOW_WIDTH//2-self.__width//2+20,
                                      constants.GAME_WINDOW_HEIGHT//2-self.__height//2+2,
                                      constants.GAME_WINDOW_WIDTH//2-self.__width//2+20,
                                      constants.GAME_WINDOW_HEIGHT//2+self.__height//2-42)

        for _ in range(0, 23):
            pygame.draw.line(surface, constants.TEST_COLOR,
                             (x_up, y_up),
                             (x_down, y_down), 1)
            x_up += 20
            x_down += 20

        x_left, y_left, x_right, y_right = (
            constants.GAME_WINDOW_WIDTH // 2 - self.__width // 2+2,
            constants.GAME_WINDOW_HEIGHT//2-self.__height//2+20,
            constants.GAME_WINDOW_WIDTH // 2 + self.__width // 2-4,
            constants.GAME_WINDOW_HEIGHT // 2 - self.__height // 2+20
        )

        for _ in range(0, 13):
            pygame.draw.line(surface, constants.TEST_COLOR,
                             (x_left, y_left),
                             (x_right, y_right), 1)
            y_left += 20
            y_right += 20

        for coins in self.__player_money:
            coins[0].update(surface)

        clock = pygame.time.Clock()
        is_inventory_showed = True
        while is_inventory_showed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        is_inventory_showed = False

            pygame.display.update()
            clock.tick(constants.FPS_LOCKING)
