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

import Constants
import game_enums
import Coin
from Drawer import Drawer


class Inventory:
    def __init__(self):
        self.__width = 480
        self.__height = 320
        self.__frame_thickness = 3
        self.__inventory_rect = pygame.Rect(Constants.GAME_WINDOW_WIDTH // 2 - self.__width // 2,
                                            Constants.GAME_WINDOW_HEIGHT // 2 - self.__height // 2,
                                            self.__width, self.__height)

        self.__resources = {
            'gold_coin': [Coin.Coin(Constants.GAME_WINDOW_WIDTH // 2 - self.__width // 2 + 30,
                                    Constants.GAME_WINDOW_HEIGHT // 2 + self.__height // 2,
                                    'resources/images/coins/gold_coin.png',
                                    game_enums.CoinTypes.GOLD), 0, None],
            'silver_coin': [Coin.Coin(Constants.GAME_WINDOW_WIDTH // 2 - 20,
                                      Constants.GAME_WINDOW_HEIGHT // 2 + self.__height // 2,
                                      'resources/images/coins/silver_coin.png',
                                      game_enums.CoinTypes.SILVER), 0, None],
            'bronze_coin': [Coin.Coin(Constants.GAME_WINDOW_WIDTH // 2 + self.__width // 2 - 60,
                                      Constants.GAME_WINDOW_HEIGHT // 2 + self.__height // 2,
                                      'resources/images/coins/bronze_coin.png',
                                      game_enums.CoinTypes.BRONZE), 0, None]
        }
        self.__inventory_cells = list()
        self.__index_cell_to_add_new_resource = 0

        self.__start_cell_to_move_item = 0
        self.__end_cell_to_move_item = 0

        self.__create_inventory_cells()

    def __create_inventory_cells(self):
        for x in range(Constants.GAME_WINDOW_WIDTH // 2 - self.__width // 2,
                       Constants.GAME_WINDOW_WIDTH // 2 - self.__width // 2 + 12 * 40, 40):
            for y in range(Constants.GAME_WINDOW_HEIGHT // 2 - self.__height // 2,
                           Constants.GAME_WINDOW_HEIGHT // 2 - self.__height // 2 + 7 * 40, 40):
                cell = pygame.Rect(x, y, 40, 40)
                self.__inventory_cells.append(cell)

    def append_resource(self, resource_to_add):
        if resource_to_add.resource_name in self.__resources:
            self.__resources[resource_to_add.resource_name][1] += 1
        else:
            self.__resources[resource_to_add.resource_name] = \
                [resource_to_add, 1, self.__index_cell_to_add_new_resource]
            self.__index_cell_to_add_new_resource += 1

    def draw_inventory(self, surface):
        def draw_outer_frame():
            pygame.draw.rect(surface, Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                             self.__inventory_rect, self.__frame_thickness)

        def draw_inventory_cells():
            for cell in self.__inventory_cells:
                x, y = cell.left, cell.top
                pygame.draw.rect(surface, Constants.TEST_COLOR, (x, y, 40, 40))
                pygame.draw.rect(surface, (0, 0, 0), (x, y, 40, 40), self.__frame_thickness)

        draw_outer_frame()
        draw_inventory_cells()

        clock = pygame.time.Clock()
        is_inventory_showed = True
        is_left_mouse_button_hold = False
        while is_inventory_showed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        is_inventory_showed = False

            clicked = pygame.mouse.get_pressed(3)
            if clicked[0] and not is_left_mouse_button_hold:
                start_coordinates = pygame.mouse.get_pos()
                is_left_mouse_button_hold = True
                for i in range(len(self.__inventory_cells)):
                    if (self.__inventory_cells[i].left < start_coordinates[0] < self.__inventory_cells[i].right
                            and
                            self.__inventory_cells[i].top < start_coordinates[1] < self.__inventory_cells[i].bottom):
                        self.__start_cell_to_move_item = i
            if is_left_mouse_button_hold and not clicked[0]:
                end_coordinates = pygame.mouse.get_pos()
                is_left_mouse_button_hold = False
                for i in range(len(self.__inventory_cells)):
                    if (self.__inventory_cells[i].left < end_coordinates[0] < self.__inventory_cells[i].right
                            and
                            self.__inventory_cells[i].top < end_coordinates[1] < self.__inventory_cells[i].bottom):
                        self.__end_cell_to_move_item = i
                for resource in self.__resources.values():
                    if resource[2] == self.__start_cell_to_move_item:
                        pygame.draw.rect(surface, Constants.TEST_COLOR, (self.__inventory_cells[resource[2]].left + 3,
                                                                         self.__inventory_cells[resource[2]].top + 3,
                                                                         34, 34))
                        resource[2] = self.__end_cell_to_move_item

            self.__resources['gold_coin'][0].update(surface)
            self.__resources['silver_coin'][0].update(surface)
            self.__resources['bronze_coin'][0].update(surface)

            Drawer.draw_text(surface, str(self.__resources['gold_coin'][1]), 20,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             self.__resources['gold_coin'][0].rect.right + 10,
                             self.__resources['gold_coin'][0].rect.top + 10)
            Drawer.draw_text(surface, str(self.__resources['silver_coin'][1]), 20,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             self.__resources['silver_coin'][0].rect.right + 10,
                             self.__resources['silver_coin'][0].rect.top + 10)
            Drawer.draw_text(surface, str(self.__resources['bronze_coin'][1]), 20,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             self.__resources['bronze_coin'][0].rect.right + 10,
                             self.__resources['bronze_coin'][0].rect.top + 10)

            pygame.display.flip()
            for name, resource in self.__resources.items():
                if name != 'gold_coin' and name != 'silver_coin' and name != 'bronze_coin':
                    resource[0].rect.centerx = self.__inventory_cells[resource[2]].centerx
                    resource[0].rect.centery = self.__inventory_cells[resource[2]].centery
                    surface.blit(resource[0].image, resource[0].rect)
                    Drawer.draw_text(surface, str(resource[1]), 20,
                                     Constants.WHITE_COLOR_TITLE_BLOCKS,
                                     self.__inventory_cells[resource[2]].centerx + 10,
                                     self.__inventory_cells[resource[2]].centery + 5)
            pygame.display.flip()
            clock.tick(Constants.FPS_LOCKING)

    def get_key_for_chest(self):
        return 'key' in self.__resources
