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


class Inventory:
    def __init__(self):
        self.__resources = {
            'bronze_coin': 0,
            'silver_coin': 0,
            'gold_coin': 0
        }
        self.__width = 480
        self.__height = 320
        self.__frame_thickness = 3
        self.__inventory_rect = pygame.Rect(constants.GAME_WINDOW_WIDTH//2-self.__width//2,
                                            constants.GAME_WINDOW_HEIGHT//2-self.__height//2,
                                            self.__width, self.__height)

    def append_resource(self, resource_name):
        if resource_name in self.__resources:
            self.__resources[resource_name] += 1

    def draw_inventory(self, surface):
        pygame.draw.rect(surface, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                         self.__inventory_rect, self.__frame_thickness)

        pygame.draw.line(surface, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                         (constants.GAME_WINDOW_WIDTH//2-self.__width//2,
                          constants.GAME_WINDOW_HEIGHT//2+self.__height//2-self.__height//10),
                         (constants.GAME_WINDOW_WIDTH//2+self.__width//2,
                          constants.GAME_WINDOW_HEIGHT//2+self.__height//2-self.__height//10),
                         3)

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
