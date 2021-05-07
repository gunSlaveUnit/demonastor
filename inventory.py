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
        self.__width = 480
        self.__height = 320
        self.__frame_thickness = 3
        self.__inventory_rect = pygame.Rect(constants.GAME_WINDOW_WIDTH//2-self.__width//2,
                                            constants.GAME_WINDOW_HEIGHT//2-self.__height//2,
                                            self.__width, self.__height)

        self.__resources = {
            'gold_coin': [coin.Coin(constants.GAME_WINDOW_WIDTH // 2 - self.__width // 2 + 20,
                                    constants.GAME_WINDOW_HEIGHT // 2 + self.__height // 2 - 20,
                                    game_enums.CoinTypes.GOLD), 0, None],
            'silver_coin': [coin.Coin(constants.GAME_WINDOW_WIDTH // 2 - 30,
                                      constants.GAME_WINDOW_HEIGHT // 2 + self.__height // 2 - 20,
                                      game_enums.CoinTypes.SILVER), 0, None],
            'bronze_coin': [coin.Coin(constants.GAME_WINDOW_WIDTH // 2 + self.__width // 2 - 70,
                                      constants.GAME_WINDOW_HEIGHT // 2 + self.__height // 2 - 20,
                                      game_enums.CoinTypes.BRONZE), 0, None]
        }
        self.__inventory_cells = list()
        self.__index_cell_to_add_new_resource = 0

    def append_resource(self, resource_to_add):
        if resource_to_add.resource_name in self.__resources:
            self.__resources[resource_to_add.resource_name][1] += 1
        else:
            self.__resources[resource_to_add.resource_name] = \
                [resource_to_add, 1, self.__index_cell_to_add_new_resource]
            self.__index_cell_to_add_new_resource += 1

    def draw_inventory(self, surface):
        pygame.draw.rect(surface, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                         self.__inventory_rect, self.__frame_thickness)

        for x in range(constants.GAME_WINDOW_WIDTH//2-self.__width//2,
                       constants.GAME_WINDOW_WIDTH//2-self.__width//2 + 12*40, 40):
            for y in range(constants.GAME_WINDOW_HEIGHT//2-self.__height//2,
                           constants.GAME_WINDOW_HEIGHT//2-self.__height//2 + 7*40, 40):
                cell = pygame.Rect(x, y, 40, 40)
                pygame.draw.rect(surface, constants.TEST_COLOR, (x, y, 40, 40), self.__frame_thickness)
                self.__inventory_cells.append(cell)

        self.__resources['gold_coin'][0].update(surface)
        self.__resources['silver_coin'][0].update(surface)
        self.__resources['bronze_coin'][0].update(surface)

        for name, resource in self.__resources.items():
            if name != 'gold_coin' and name != 'silver_coin' and name != 'bronze_coin':
                resource[0].rect.centerx = self.__inventory_cells[resource[2]].centerx
                resource[0].rect.centery = self.__inventory_cells[resource[2]].centery
                surface.blit(resource[0].image, resource[0].rect)

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

    def get_key_for_chest(self):
        return 'key' in self.__resources
