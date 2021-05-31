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
import GameEnums
import Coin
from Drawer import Drawer


class Inventory:
    def __init__(self):
        self._width = 480
        self._height = 320
        self._frame_thickness = 3
        self._inventory_rect = pygame.Rect(Constants.GAME_WINDOW_WIDTH // 2 - self._width // 2,
                                           Constants.GAME_WINDOW_HEIGHT // 2 - self._height // 2,
                                           self._width, self._height)

        self._resources = {
            'gold_coin': [Coin.Coin(Constants.GAME_WINDOW_WIDTH // 2 - self._width // 2 + 30,
                                    Constants.GAME_WINDOW_HEIGHT // 2 + self._height // 2,
                                    'resources/images/coins/gold_coin.png',
                                    GameEnums.CoinTypes.GOLD), 0, None],
            'silver_coin': [Coin.Coin(Constants.GAME_WINDOW_WIDTH // 2 - 20,
                                      Constants.GAME_WINDOW_HEIGHT // 2 + self._height // 2,
                                      'resources/images/coins/silver_coin.png',
                                      GameEnums.CoinTypes.SILVER), 0, None],
            'bronze_coin': [Coin.Coin(Constants.GAME_WINDOW_WIDTH // 2 + self._width // 2 - 60,
                                      Constants.GAME_WINDOW_HEIGHT // 2 + self._height // 2,
                                      'resources/images/coins/bronze_coin.png',
                                      GameEnums.CoinTypes.BRONZE), 0, None]
        }
        self._cells = list()
        self._index_cell_to_add_new_resource = 0

        self._start_cell_to_move_item = 0
        self._end_cell_to_move_item = 0

        self._create_inventory_cells()

    def _create_inventory_cells(self):
        for x in range(Constants.GAME_WINDOW_WIDTH // 2 - self._width // 2,
                       Constants.GAME_WINDOW_WIDTH // 2 - self._width // 2 + 12 * 40, 40):
            for y in range(Constants.GAME_WINDOW_HEIGHT // 2 - self._height // 2,
                           Constants.GAME_WINDOW_HEIGHT // 2 - self._height // 2 + 7 * 40, 40):
                cell = pygame.Rect(x, y, 40, 40)
                self._cells.append(cell)

    def append_resource(self, resource_to_add):
        if resource_to_add.resource_name in self._resources:
            self._resources[resource_to_add.resource_name][1] += 1
        else:
            self._resources[resource_to_add.resource_name] = \
                [resource_to_add, 1, self._index_cell_to_add_new_resource]
            self._index_cell_to_add_new_resource += 1

    def draw_inventory(self, surface):
        def draw_outer_frame():
            pygame.draw.rect(surface, Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                             self._inventory_rect, self._frame_thickness)

        def draw_inventory_cells():
            for cell in self._cells:
                x, y = cell.left, cell.top
                pygame.draw.rect(surface, Constants.TEST_COLOR, (x, y, 40, 40))
                pygame.draw.rect(surface, (0, 0, 0), (x, y, 40, 40), self._frame_thickness)

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
                for i in range(len(self._cells)):
                    if (self._cells[i].left < start_coordinates[0] < self._cells[i].right
                            and
                            self._cells[i].top < start_coordinates[1] < self._cells[i].bottom):
                        self._start_cell_to_move_item = i
            if is_left_mouse_button_hold and not clicked[0]:
                end_coordinates = pygame.mouse.get_pos()
                is_left_mouse_button_hold = False
                for i in range(len(self._cells)):
                    if (self._cells[i].left < end_coordinates[0] < self._cells[i].right
                            and
                            self._cells[i].top < end_coordinates[1] < self._cells[i].bottom):
                        self._end_cell_to_move_item = i
                for resource in self._resources.values():
                    if resource[2] == self._start_cell_to_move_item:
                        pygame.draw.rect(surface, Constants.TEST_COLOR, (self._cells[resource[2]].left + 3,
                                                                         self._cells[resource[2]].top + 3,
                                                                         34, 34))
                        resource[2] = self._end_cell_to_move_item

            self._resources['gold_coin'][0].update(surface)
            self._resources['silver_coin'][0].update(surface)
            self._resources['bronze_coin'][0].update(surface)

            Drawer.draw_text(surface, str(self._resources['gold_coin'][1]), 20,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             self._resources['gold_coin'][0].rect.right + 10,
                             self._resources['gold_coin'][0].rect.top + 10)
            Drawer.draw_text(surface, str(self._resources['silver_coin'][1]), 20,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             self._resources['silver_coin'][0].rect.right + 10,
                             self._resources['silver_coin'][0].rect.top + 10)
            Drawer.draw_text(surface, str(self._resources['bronze_coin'][1]), 20,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             self._resources['bronze_coin'][0].rect.right + 10,
                             self._resources['bronze_coin'][0].rect.top + 10)

            pygame.display.flip()
            for name, resource in self._resources.items():
                if name != 'gold_coin' and name != 'silver_coin' and name != 'bronze_coin':
                    resource[0].rect.centerx = self._cells[resource[2]].centerx
                    resource[0].rect.centery = self._cells[resource[2]].centery
                    surface.blit(resource[0].image, resource[0].rect)
                    Drawer.draw_text(surface, str(resource[1]), 20,
                                     Constants.WHITE_COLOR_TITLE_BLOCKS,
                                     self._cells[resource[2]].centerx + 10,
                                     self._cells[resource[2]].centery + 5)
            pygame.display.flip()
            clock.tick(Constants.FPS_LOCKING)

    def get_key_for_chest(self):
        return 'key' in self._resources
