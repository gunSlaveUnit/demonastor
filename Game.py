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

import constants
from Neutral import Neutral
from Player import Player
from camera import Camera
from chest import Chest
from drawer import Drawer
from key import Key
from map import Map
from tree import Tree


class Game:
    def __init__(self):
        pygame.init()
        self._main_game_window = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH,
                                                          constants.GAME_WINDOW_HEIGHT))
        self._customize_window()
        pygame.display.toggle_fullscreen()
        pygame.display.set_caption(constants.GAME_WINDOW_TITLE)
        icon = pygame.image.load('resources/images/icons/icon.png')
        pygame.display.set_icon(icon)

    @staticmethod
    def _customize_window():
        pygame.display.toggle_fullscreen()
        pygame.display.set_caption(constants.GAME_WINDOW_TITLE)
        icon = pygame.image.load('resources/images/icons/icon.png')
        pygame.display.set_icon(icon)

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
            f'resources/images/backgrounds/background_{constants.GAME_WINDOW_WIDTH}_{constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {
            'New Game': [constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80],
            'Load Game': [constants.WHITE_COLOR_TITLE_BLOCKS, 50],
            'Settings': [constants.WHITE_COLOR_TITLE_BLOCKS, 50],
            'Exit': [constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        }
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            title_size = 150
            Drawer.draw_text(self._main_game_window, constants.GAME_WINDOW_TITLE, title_size,
                             constants.WHITE_COLOR_TITLE_BLOCKS,
                             constants.GAME_WINDOW_WIDTH // 2, 100)

            x_to_paste_menu_item = constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += constants.GAME_WINDOW_HEIGHT // 15

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
                        set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                                                   80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = 3
                        set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
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
            clock.tick(constants.FPS_LOCKING)

    def show_pause_menu(self):
        Drawer.draw_text(self._main_game_window, 'Pause. Press <Enter> To Continue', 30, constants.WHITE_COLOR_TITLE_BLOCKS,
                         constants.GAME_WINDOW_WIDTH // 2, constants.GAME_WINDOW_HEIGHT // 4)

        items = ['Загрузить', 'Выход']
        handlers = ['show_game_loads()', 'exit(0)']

        def set_color_active_menu_item(index_active_menu_item, color, font_size):
            filename_to_highlight = items[index_active_menu_item]
            menu_items[filename_to_highlight] = [color, font_size]

        menu_background = pygame.image.load(
            f'resources/images/backgrounds/background_{constants.GAME_WINDOW_WIDTH}_{constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {}
        for save_file_name in items:
            menu_items[save_file_name] = [constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        menu_items[items[0]] = [constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80]

        amount_files = len(items)
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            x_to_paste_menu_item = constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += constants.GAME_WINDOW_HEIGHT // 15

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
                                                   constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item,
                                                   constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_RETURN:
                        eval(handlers[index_selected_menu_item])
                    if event.key == pygame.K_ESCAPE:
                        is_menu_show = False
            pygame.display.flip()
            self._main_game_window.blit(menu_background, (0, 0))
            clock.tick(constants.FPS_LOCKING)

    @staticmethod
    def save_game(objects_for_saving):
        save_time = datetime.datetime.today()
        with open(f'savings/{save_time.strftime("%Y-%m-%d-%H.%M.%S")}.pickle', 'wb') as save_file:
            for game_object in objects_for_saving:
                pickle.dump(game_object.params_for_saving, save_file)

    def load_game(self, file_name_for_loading=None):
        saves = os.listdir(constants.DIRECTORY_WITH_SAVINGS)
        if not saves:
            self.run_game()
        else:
            filename = os.path.join(constants.DIRECTORY_WITH_SAVINGS,
                                    os.listdir(constants.DIRECTORY_WITH_SAVINGS)[-1]) if file_name_for_loading is None \
                else os.path.join(constants.DIRECTORY_WITH_SAVINGS, file_name_for_loading)
            with open(filename, 'rb') as load_file:
                data = pickle.load(load_file)
                self.run_game(data)

    def show_game_loads(self):
        savings = os.listdir(constants.DIRECTORY_WITH_SAVINGS)
        if not savings:
            self.run_game()

        def set_color_active_menu_item(index_active_menu_item, color, font_size):
            filename_to_highlight = savings[index_active_menu_item]
            menu_items[filename_to_highlight] = [color, font_size]

        menu_background = pygame.image.load(
            f'resources/images/backgrounds/background_{constants.GAME_WINDOW_WIDTH}_{constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {

        }
        for save_file_name in savings:
            menu_items[save_file_name] = [constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        menu_items[savings[0]] = [constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80]

        amount_files = len(savings)
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            title_size = 150
            Drawer.draw_text(self._main_game_window, constants.GAME_WINDOW_TITLE, title_size,
                             constants.WHITE_COLOR_TITLE_BLOCKS,
                             constants.GAME_WINDOW_WIDTH // 2, 100)

            x_to_paste_menu_item = constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += constants.GAME_WINDOW_HEIGHT // 15

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
                        set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                                                   80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
                                                   80)
                    if event.key == pygame.K_RETURN:
                        self.load_game(savings[index_selected_menu_item])

            pygame.display.flip()
            self._main_game_window.blit(menu_background, (0, 0))
            clock.tick(constants.FPS_LOCKING)

    def run_game(self, data_for_loading=None):
        game_map = Map()
        player = Player(constants.GAME_WINDOW_WIDTH // 2,
                        constants.GAME_WINDOW_HEIGHT // 2,
                        animation_images=[
                            [
                                'resources/images/player/player_left_moving_0.png',
                                'resources/images/player/player_left_moving_1.png',
                                'resources/images/player/player_left_moving_2.png',
                                'resources/images/player/player_left_moving_3.png'
                            ],
                            [
                                'resources/images/player/player_right_moving_0.png',
                                'resources/images/player/player_right_moving_1.png',
                                'resources/images/player/player_right_moving_2.png',
                                'resources/images/player/player_right_moving_3.png'
                            ],
                            [
                                'resources/images/player/player_up_moving_0.png',
                                'resources/images/player/player_up_moving_1.png',
                                'resources/images/player/player_up_moving_2.png',
                                'resources/images/player/player_up_moving_3.png'
                            ],
                            [
                                'resources/images/player/player_down_moving_0.png',
                                'resources/images/player/player_down_moving_1.png',
                                'resources/images/Player/player_down_moving_2.png',
                                'resources/images/Player/player_down_moving_3.png'
                            ]],
                        saved_params=data_for_loading
                        )
        quests = []
        names_done_quests = []
        neutrals = [Neutral(100, 100, [
            [
                'resources/images/characters/neutral_left_0.png',
                'resources/images/characters/neutral_left_1.png',
                'resources/images/characters/neutral_left_3.png',
                'resources/images/characters/neutral_left_2.png'
            ],
            [
                'resources/images/characters/neutral_right_0.png',
                'resources/images/characters/neutral_right_1.png',
                'resources/images/characters/neutral_right_3.png',
                'resources/images/characters/neutral_right_2.png'
            ],
            [
                'resources/images/characters/neutral_up_0.png',
                'resources/images/characters/neutral_up_1.png',
                'resources/images/characters/neutral_up_2.png',
                'resources/images/characters/neutral_up_2.png'
            ],
            [
                'resources/images/characters/neutral_down_0.png',
                'resources/images/characters/neutral_down_1.png',
                'resources/images/characters/neutral_down_3.png',
                'resources/images/characters/neutral_down_2.png'
            ]
        ], player.level)]

        chests = [Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=False),
                  Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                        is_chest_need_key=True)]

        trees = []
        for _ in range(0, 5):
            tree = Tree(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                        random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT))
            trees.append(tree)

        camera = Camera()

        things = []

        key = Key(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                  random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT))
        things.append(key)

        shells_player = []
        enemies = neutrals[0].quest.condition

        text = None
        test_cur = None
        test_max = None

        time_to_count_attack = 0
        clock = pygame.time.Clock()
        is_game_exit = False
        while not is_game_exit:
            delta = clock.tick(constants.FPS_LOCKING)
            pygame.event.pump()
            enemy_attack_interval = random.randint(250, 1000)
            if time_to_count_attack < enemy_attack_interval:
                time_to_count_attack += delta

            for enemy in enemies:
                if pygame.sprite.collide_rect(player, enemy):
                    if time_to_count_attack >= enemy_attack_interval:
                        time_to_count_attack = 0
                        player.current_health = player.current_health - enemy.amount_damage
                        if player.current_health < 1:
                            return self.game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_pause_menu()
                    if event.key == pygame.K_F5:
                        self.save_game([player])
                    if event.key == pygame.K_F9:
                        self.load_game()
                    if event.key == pygame.K_SPACE:
                        shells = player.attack()
                        shells_player.extend(shells)
                    if event.key == pygame.K_i:
                        player.show_inventory(self._main_game_window)
                    if event.key == pygame.K_c:
                        player.change_weapon()

            self._main_game_window.fill(int())

            game_map.update(self._main_game_window)
            for tile in game_map.map_tiles:
                offset = camera.get_offset()
                tile.rect.centerx -= offset[0]
                tile.rect.centery -= offset[1]

            for chest in chests:
                offset = camera.get_offset()
                chest.rect.centerx -= offset[0]
                chest.rect.centery -= offset[1]
                chest.update(self._main_game_window)
                if pygame.sprite.collide_rect(player, chest) and pygame.key.get_pressed()[pygame.K_e]:
                    additional_potions = chest.open(player.is_key_in_inventory())
                    if additional_potions is not None:
                        for additional_thing in additional_potions:
                            if additional_thing != 0:
                                things.append(additional_thing)

            for potion in things:
                potion.update(self._main_game_window)
                offset = camera.get_offset()
                potion.rect.centerx -= offset[0]
                potion.rect.centery -= offset[1]

                if pygame.sprite.collide_rect(player, potion) and pygame.key.get_pressed()[pygame.K_e]:
                    player.append_thing_to_inventory(potion)
                    things.remove(potion)

            for neutral in neutrals:
                if pygame.sprite.collide_rect(player, neutral) and pygame.key.get_pressed()[pygame.K_e]:
                    quests.append(neutral.quest)
                    neutral.vision_quest_mark = False

            offset = camera.get_offset()
            for neutral in neutrals:
                neutral.update(self._main_game_window)
                neutral.rect.centerx -= offset[0]
                neutral.rect.centery -= offset[1]

            for tree in trees:
                tree.update(self._main_game_window)
                offset = camera.get_offset()
                tree.rect.centerx -= offset[0]
                tree.rect.centery -= offset[1]

            for shell in shells_player:
                if shell:
                    shell.update(self._main_game_window)
                    offset = camera.get_offset()
                    shell.rect.centerx -= offset[0]
                    shell.rect.centery -= offset[1]

            for enemy in enemies:
                enemy.attack(player.rect.centerx, player.rect.centery)
                offset = camera.get_offset()
                enemy.rect.centerx -= offset[0]
                enemy.rect.centery -= offset[1]
                enemy.update(self._main_game_window)
                enemy.attack(player.rect.centerx, player.rect.centery)

            for enemy in enemies:
                for shell in shells_player:
                    if shell:
                        if pygame.sprite.collide_rect(enemy, shell):
                            shells_player.remove(shell)
                            enemy.current_health -= player.amount_damage
                            enemy.current_health -= shell.amount_additional_damage

                            dx = float(player.rect.centerx - enemy.rect.centerx)
                            dy = float(player.rect.centery - enemy.rect.centery)
                            length = math.sqrt(dx ** 2 + dy ** 2)
                            enemy.is_enemy_angry = True
                            enemy.show_aggression_to_attack_player(dx, dy, length)

                            text = enemy.name
                            test_cur = enemy.current_health
                            test_max = enemy.max_amount_health
                            if enemy.current_health < 0:
                                player.current_experience += enemy.experience_for_killing

                                if enemy in enemies:
                                    enemies.remove(enemy)
                                text = None
                                test_cur = None
                                test_max = None

            camera.update(player)
            player.update(self._main_game_window)

            for quest in quests:
                if not enemies:
                    quest.completed = True
                    player.current_experience += quest.experience
                    if quest.title not in names_done_quests:
                        names_done_quests.append(quest.title)
                    quests.remove(quest)

            if text is not None:
                Drawer.draw_bar(self._main_game_window, constants.GAME_WINDOW_WIDTH // 2, 10,
                                constants.UNNAMED_COLOR_HEALTH_BAR,
                                test_cur, test_max, 150, 15)
                Drawer.draw_text(self._main_game_window, text, 25, constants.WHITE_COLOR_TITLE_BLOCKS,
                                 constants.GAME_WINDOW_WIDTH // 2,
                                 9)

            Drawer.draw_text(self._main_game_window, player.name, 15, constants.WHITE_COLOR_TITLE_BLOCKS,
                             player.rect.centerx,
                             player.rect.centery + player.rect.height // 2 + 5)
            Drawer.draw_bar(self._main_game_window, constants.GAME_WINDOW_WIDTH // 2, constants.GAME_WINDOW_HEIGHT * 0.86,
                            constants.WHITE_COLOR_TITLE_BLOCKS,
                            player.current_experience, player.experience_up_level, 310, 5, True)
            Drawer.draw_bar(self._main_game_window, constants.GAME_WINDOW_WIDTH // 2 - 70, constants.GAME_WINDOW_HEIGHT - 70,
                            constants.STAMINA_BAR_COLOR, player.current_stamina,
                            player.max_stamina, 90, 14, True)

            pygame.display.flip()  # for double buffering
            clock.tick(constants.FPS_LOCKING)
        pygame.quit()

    def game_over(self):
        items = ['Последнее сохранение', 'Загрузить', 'Выйти']
        handlers = ['load_game()', 'show_game_loads()', 'exit(0)']
        Drawer.draw_text(self._main_game_window, 'You died. Press <Enter> To Restart Or <Escape> To Exit', 30,
                         constants.WHITE_COLOR_TITLE_BLOCKS,
                         constants.GAME_WINDOW_WIDTH // 2, constants.GAME_WINDOW_HEIGHT // 4)

        def set_color_active_menu_item(index_active_menu_item, color, font_size):
            filename_to_highlight = items[index_active_menu_item]
            menu_items[filename_to_highlight] = [color, font_size]

        menu_background = pygame.image.load(
            f'resources/images/backgrounds/background_{constants.GAME_WINDOW_WIDTH}_{constants.GAME_WINDOW_HEIGHT}.jpg'
        )

        menu_items = {}
        for save_file_name in items:
            menu_items[save_file_name] = [constants.WHITE_COLOR_TITLE_BLOCKS, 50]
        menu_items[items[0]] = [constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80]

        amount_files = len(items)
        index_selected_menu_item = 0

        is_menu_show = True
        clock = pygame.time.Clock()
        while is_menu_show:
            x_to_paste_menu_item = constants.GAME_WINDOW_HEIGHT // 3
            for menu_item, color_and_size in menu_items.items():
                Drawer.draw_text(self._main_game_window, menu_item, color_and_size[1], color_and_size[0],
                                 constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
                x_to_paste_menu_item += constants.GAME_WINDOW_HEIGHT // 15

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
                                                   constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        index_previous_selected_item = index_selected_menu_item
                        index_selected_menu_item -= 1
                        if index_selected_menu_item < 0:
                            index_selected_menu_item = amount_files - 1
                        set_color_active_menu_item(index_previous_selected_item,
                                                   constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                        set_color_active_menu_item(index_selected_menu_item,
                                                   constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                    if event.key == pygame.K_RETURN:
                        eval(handlers[index_selected_menu_item])
            pygame.display.flip()
            self._main_game_window.blit(menu_background, (0, 0))
            clock.tick(constants.FPS_LOCKING)
