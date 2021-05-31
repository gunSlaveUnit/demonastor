"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describes the game class,
which contains all game objects and methods for starting,
loading and saving the game.
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import datetime
import math
import os
import pickle
import sys
import random

import pygame

import Textures
import Constants
from Neutral import Neutral
from Player import Player
from Camera import Camera
from Chest import Chest
from Drawer import Drawer
from Map import Map
from Tree import Tree


class Game:
    def __init__(self):
        pygame.init()
        self._main_game_window = pygame.display.set_mode((Constants.GAME_WINDOW_WIDTH,
                                                          Constants.GAME_WINDOW_HEIGHT))
        self._customize_window()
        self._player = None
        self._map = Map()
        self._neutrals = [Neutral(100, 100, Textures.NEUTRAL)]
        self._quests = []
        self._names_done_quests = []
        self._enemies = self._neutrals[0].quest.condition
        self._camera = Camera()
        self._shells = []
        self._things = []
        self._chests = self._create_chests()
        self._trees = [
            Tree(random.randint(-Constants.GAME_WINDOW_WIDTH, Constants.GAME_WINDOW_WIDTH),
                 random.randint(-Constants.GAME_WINDOW_HEIGHT, Constants.GAME_WINDOW_HEIGHT),
                 'resources/images/trees/tree.png'),
            Tree(random.randint(-Constants.GAME_WINDOW_WIDTH, Constants.GAME_WINDOW_WIDTH),
                 random.randint(-Constants.GAME_WINDOW_HEIGHT, Constants.GAME_WINDOW_HEIGHT),
                 'resources/images/trees/tree.png'),
        ]

    @staticmethod
    def _customize_window():
        # pygame.display.toggle_fullscreen()
        pygame.display.set_caption(Constants.GAME_WINDOW_TITLE)
        icon = pygame.image.load('resources/images/icons/icon.png')
        pygame.display.set_icon(icon)

    @staticmethod
    def _create_chests():
        chests = []
        for _ in range(random.randint(10, 20)):
            is_need_key = random.randint(0, 2)
            if is_need_key:
                chests.append(Chest(random.randint(-Constants.GAME_WINDOW_WIDTH, Constants.GAME_WINDOW_WIDTH),
                                    random.randint(-Constants.GAME_WINDOW_HEIGHT, Constants.GAME_WINDOW_HEIGHT),
                                    'resources/images/chests/chest_with_key.png',
                                    is_chest_need_key=True))
            else:
                chests.append(Chest(random.randint(-Constants.GAME_WINDOW_WIDTH, Constants.GAME_WINDOW_WIDTH),
                                    random.randint(-Constants.GAME_WINDOW_HEIGHT, Constants.GAME_WINDOW_HEIGHT),
                                    'resources/images/chests/closed_chest.png',
                                    is_chest_need_key=False))
        return chests

    def show_start_menu(self):
        # TODO: add mouse menu control
        def set_color_active_menu_item(index_active_menu_item, color, font_size):
            if index_active_menu_item == 0:
                menu_items['New Game'] = [color, font_size]
            if index_active_menu_item == 1:
                menu_items['Load Game'] = [color, font_size]
            if index_active_menu_item == 2:
                menu_items['Settings'] = [color, font_size]
            if index_active_menu_item == 3:
                menu_items['Exit'] = [color, font_size]

        menu_background = pygame.image.load(
            f'resources/images/backgrounds/background_{Constants.GAME_WINDOW_WIDTH}_{Constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {
            'New Game': [Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80],
            'Load Game': [Constants.WHITE_COLOR_TITLE_BLOCKS, 50],
            'Settings': [Constants.WHITE_COLOR_TITLE_BLOCKS, 50],
            'Exit': [Constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        }
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            title_size = 150
            Drawer.draw_text(self._main_game_window, Constants.GAME_WINDOW_TITLE, title_size,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             Constants.GAME_WINDOW_WIDTH // 2, 100)

            x_to_paste_menu_item = Constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 Constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += Constants.GAME_WINDOW_HEIGHT // 15

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item += 1
                        if index_selected_menu_item > 3:
                            index_selected_menu_item = 0
                            index_previous_selected_item = 3
                        set_color_active_menu_item(index_previous_selected_item, Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                                                   80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = 3
                        set_color_active_menu_item(index_previous_selected_item, Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                                                   80)
                    if event.key == pygame.K_RETURN:
                        if index_selected_menu_item == 0:
                            is_menu_show = False
                            self.run_game()
                        if index_selected_menu_item == 1:
                            self.show_game_loads()
                        if index_selected_menu_item == 2:
                            pass
                        if index_selected_menu_item == 3:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()
            self._main_game_window.blit(menu_background, (0, 0))
            clock.tick(Constants.FPS_LOCKING)

    def show_pause_menu(self):
        Drawer.draw_text(self._main_game_window, 'Pause. Press <Enter> To Continue', 30,
                         Constants.WHITE_COLOR_TITLE_BLOCKS,
                         Constants.GAME_WINDOW_WIDTH // 2, Constants.GAME_WINDOW_HEIGHT // 4)

        items = ['Загрузить', 'Выход']
        handlers = ['self.show_game_loads()', 'exit(0)']

        def set_color_active_menu_item(index_active_menu_item, color, font_size):
            filename_to_highlight = items[index_active_menu_item]
            menu_items[filename_to_highlight] = [color, font_size]

        menu_background = pygame.image.load(
            f'resources/images/backgrounds/background_{Constants.GAME_WINDOW_WIDTH}_{Constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {}
        for save_file_name in items:
            menu_items[save_file_name] = [Constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        menu_items[items[0]] = [Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80]

        amount_files = len(items)
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            x_to_paste_menu_item = Constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 Constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += Constants.GAME_WINDOW_HEIGHT // 15

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item += 1
                        if index_selected_menu_item > amount_files - 1:
                            index_selected_menu_item = 0
                            index_previous_selected_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item,
                                                   Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item,
                                                   Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_RETURN:
                        eval(handlers[index_selected_menu_item])
                    if event.key == pygame.K_ESCAPE:
                        is_menu_show = False
            pygame.display.flip()
            self._main_game_window.blit(menu_background, (0, 0))
            clock.tick(Constants.FPS_LOCKING)

    @staticmethod
    def save_game(objects_for_saving):
        save_time = datetime.datetime.today()
        with open(f'savings/{save_time.strftime("%Y-%m-%d-%H.%M.%S")}.pickle', 'wb') as save_file:
            for game_object in objects_for_saving:
                pickle.dump(game_object.params_for_saving, save_file)

    def load_game(self, file_name_for_loading=None):
        saves = os.listdir(Constants.DIRECTORY_WITH_SAVINGS)
        if not saves:
            self.run_game()
        else:
            filename = os.path.join(Constants.DIRECTORY_WITH_SAVINGS,
                                    os.listdir(Constants.DIRECTORY_WITH_SAVINGS)[-1]) if file_name_for_loading is None \
                else os.path.join(Constants.DIRECTORY_WITH_SAVINGS, file_name_for_loading)
            with open(filename, 'rb') as load_file:
                data = pickle.load(load_file)
                self.run_game(data)

    def show_game_loads(self):
        savings = os.listdir(Constants.DIRECTORY_WITH_SAVINGS)
        if not savings:
            self.run_game()

        def set_color_active_menu_item(index_active_menu_item, color, font_size):
            filename_to_highlight = savings[index_active_menu_item]
            menu_items[filename_to_highlight] = [color, font_size]

        menu_background = pygame.image.load(
            f'resources/images/backgrounds/background_{Constants.GAME_WINDOW_WIDTH}_{Constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {

        }
        for save_file_name in savings:
            menu_items[save_file_name] = [Constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        menu_items[savings[0]] = [Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80]

        amount_files = len(savings)
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            title_size = 150
            Drawer.draw_text(self._main_game_window, Constants.GAME_WINDOW_TITLE, title_size,
                             Constants.WHITE_COLOR_TITLE_BLOCKS,
                             Constants.GAME_WINDOW_WIDTH // 2, 100)

            x_to_paste_menu_item = Constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 Constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += Constants.GAME_WINDOW_HEIGHT // 15

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item += 1
                        if index_selected_menu_item > amount_files - 1:
                            index_selected_menu_item = 0
                            index_previous_selected_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item, Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                                                   80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item, Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                                                   80)
                    if event.key == pygame.K_RETURN:
                        self.load_game(savings[index_selected_menu_item])

            pygame.display.flip()
            self._main_game_window.blit(menu_background, (0, 0))
            clock.tick(Constants.FPS_LOCKING)

    def run_game(self, data=None):
        self._player = Player(
            Constants.GAME_WINDOW_WIDTH // 2,
            Constants.GAME_WINDOW_HEIGHT // 2,
            animation_images=Textures.PLAYER,
            saved_params=data
        )

        text = None
        test_cur = None
        test_max = None

        time_to_count_attack = 0
        clock = pygame.time.Clock()
        is_game_exit = False
        while not is_game_exit:
            delta = clock.tick(Constants.FPS_LOCKING)
            pygame.event.pump()
            enemy_attack_interval = random.randint(250, 1000)
            if time_to_count_attack < enemy_attack_interval:
                time_to_count_attack += delta

            for enemy in self._enemies:
                if pygame.sprite.collide_rect(self._player, enemy):
                    if time_to_count_attack >= enemy_attack_interval:
                        time_to_count_attack = 0
                        self._player.current_health = self._player.current_health - enemy.amount_damage
                        if self._player.current_health < 1:
                            return self.game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_pause_menu()
                    if event.key == pygame.K_F5:
                        self.save_game([self._player])
                    if event.key == pygame.K_F9:
                        self.load_game()
                    if event.key == pygame.K_SPACE:
                        shells = self._player.attack()
                        self._shells.extend(shells)
                    if event.key == pygame.K_i:
                        self._player.show_inventory(self._main_game_window)
                    if event.key == pygame.K_c:
                        self._player.change_weapon()

            self._main_game_window.fill(int())

            self._map.update(self._main_game_window)
            for tile in self._map.map_tiles:
                offset = self._camera.offset
                tile.rect.centerx -= offset[0]
                tile.rect.centery -= offset[1]

            for chest in self._chests:
                offset = self._camera.offset
                chest.rect.centerx -= offset[0]
                chest.rect.centery -= offset[1]
                chest.update(self._main_game_window)
                if pygame.sprite.collide_rect(self._player, chest) and pygame.key.get_pressed()[pygame.K_e]:
                    additional_potions = chest.open(self._player.is_key_in_inventory())
                    if additional_potions is not None:
                        for additional_thing in additional_potions:
                            if additional_thing != 0:
                                self._things.append(additional_thing)

            for potion in self._things:
                if potion:
                    potion.update(self._main_game_window)
                    offset = self._camera.offset
                    potion.rect.centerx -= offset[0]
                    potion.rect.centery -= offset[1]

                    if pygame.sprite.collide_rect(self._player, potion) and pygame.key.get_pressed()[pygame.K_e]:
                        self._player.append_thing_to_inventory(potion)
                        self._things.remove(potion)

            for neutral in self._neutrals:
                if pygame.sprite.collide_rect(self._player, neutral) and pygame.key.get_pressed()[pygame.K_e]:
                    self._quests.append(neutral.quest)
                    neutral.vision_quest_mark = False

            offset = self._camera.offset
            for neutral in self._neutrals:
                neutral.update(self._main_game_window)
                neutral.rect.centerx -= offset[0]
                neutral.rect.centery -= offset[1]

            for tree in self._trees:
                tree.update(self._main_game_window)
                offset = self._camera.offset
                tree.rect.centerx -= offset[0]
                tree.rect.centery -= offset[1]

            for shell in self._shells:
                if shell:
                    shell.update(self._main_game_window)
                    offset = self._camera.offset
                    shell.rect.centerx -= offset[0]
                    shell.rect.centery -= offset[1]

            for enemy in self._enemies:
                enemy.attack(self._player.rect.centerx, self._player.rect.centery)
                offset = self._camera.offset
                enemy.rect.centerx -= offset[0]
                enemy.rect.centery -= offset[1]
                enemy.update(self._main_game_window)
                enemy.attack(self._player.rect.centerx, self._player.rect.centery)

            for enemy in self._enemies:
                for shell in self._shells:
                    if shell:
                        if pygame.sprite.collide_rect(enemy, shell):
                            self._shells.remove(shell)
                            enemy.current_health -= self._player.amount_damage
                            enemy.current_health -= shell.amount_additional_damage

                            dx = float(self._player.rect.centerx - enemy.rect.centerx)
                            dy = float(self._player.rect.centery - enemy.rect.centery)
                            length = math.sqrt(dx ** 2 + dy ** 2)
                            enemy.is_enemy_angry = True
                            enemy.show_aggression_to_attack_player(dx, dy, length)

                            text = enemy.name
                            test_cur = enemy.current_health
                            test_max = enemy.max_amount_health
                            if enemy.current_health < 0:
                                self._player.current_experience += enemy.experience_for_killing

                                if enemy in self._enemies:
                                    self._enemies.remove(enemy)
                                text = None
                                test_cur = None
                                test_max = None

            self._camera.update(self._player)
            self._player.update(self._main_game_window)

            for quest in self._quests:
                if not self._enemies:
                    quest.completed = True
                    self._player.current_experience += quest.experience
                    if quest not in self._names_done_quests:
                        self._names_done_quests.append(quest.title)
                    self._quests.remove(quest)

            if text is not None:
                Drawer.draw_bar(self._main_game_window, Constants.GAME_WINDOW_WIDTH // 2, 10,
                                Constants.UNNAMED_COLOR_HEALTH_BAR,
                                test_cur, test_max, 150, 15)
                Drawer.draw_text(self._main_game_window, text, 25, Constants.WHITE_COLOR_TITLE_BLOCKS,
                                 Constants.GAME_WINDOW_WIDTH // 2,
                                 9)

            Drawer.draw_text(self._main_game_window, self._player.name, 15, Constants.WHITE_COLOR_TITLE_BLOCKS,
                             self._player.rect.centerx,
                             self._player.rect.centery + self._player.rect.height // 2 + 5)
            Drawer.draw_bar(self._main_game_window, Constants.GAME_WINDOW_WIDTH // 2,
                            Constants.GAME_WINDOW_HEIGHT * 0.86,
                            Constants.WHITE_COLOR_TITLE_BLOCKS,
                            self._player.current_experience, self._player.experience_up_level, 310, 5, True)
            Drawer.draw_bar(self._main_game_window, Constants.GAME_WINDOW_WIDTH // 2 - 70,
                            Constants.GAME_WINDOW_HEIGHT - 70,
                            Constants.STAMINA_BAR_COLOR, self._player.current_stamina,
                            self._player.max_stamina, 90, 14, True)

            pygame.display.flip()  # for double buffering
            clock.tick(Constants.FPS_LOCKING)
        pygame.quit()

    def game_over(self):
        items = ['Последнее сохранение', 'Загрузить', 'Выйти']
        handlers = ['load_game()', 'show_game_loads()', 'exit(0)']
        Drawer.draw_text(self._main_game_window, 'You died. Press <Enter> To Restart Or <Escape> To Exit', 30,
                         Constants.WHITE_COLOR_TITLE_BLOCKS,
                         Constants.GAME_WINDOW_WIDTH // 2, Constants.GAME_WINDOW_HEIGHT // 4)

        def set_color_active_menu_item(index_active_menu_item, color, font_size):
            filename_to_highlight = items[index_active_menu_item]
            menu_items[filename_to_highlight] = [color, font_size]

        menu_background = pygame.image.load(
            f'resources/images/backgrounds/background_{Constants.GAME_WINDOW_WIDTH}_{Constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {}
        for save_file_name in items:
            menu_items[save_file_name] = [Constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        menu_items[items[0]] = [Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80]

        amount_files = len(items)
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            x_to_paste_menu_item = Constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 Constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += Constants.GAME_WINDOW_HEIGHT // 15

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item += 1
                        if index_selected_menu_item > amount_files - 1:
                            index_selected_menu_item = 0
                            index_previous_selected_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item,
                                                   Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item,
                                                   Constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   Constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_RETURN:
                        eval(handlers[index_selected_menu_item])
            pygame.display.flip()
            self._main_game_window.blit(menu_background, (0, 0))
            clock.tick(Constants.FPS_LOCKING)
