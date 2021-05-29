"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

In this file the program is started
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

# TODO: make collisions
# TODO: we need to add exceptions

# TODO: для сохранения мы можем просто пихать в качестве аргумента при создании объекта словарь
# TODO: можно добавить скриншоты и запись видео

# TODO: make an additional panel with some resources, for example, with potions

# TODO: Several main tasks:
# Map
# Quests
# Locations
# New opponents
# Skills

#TODO: we need to get camera offset just only once, not so much

import sys
import random
import math
import os
import pickle
from datetime import datetime

import pygame

import map
import constants
from camera import Camera
from player import Player
import demon
from chest import Chest
from key import Key
from tree import Tree
from drawer import Drawer
from waterfall import Waterfall
from neutral import Neutral


def run_game(data_for_loading=None):
    global main_game_window
    game_map = map.Map()
    if data_for_loading:
        print(data_for_loading)
        for key in data_for_loading.keys():
            print(key)
        player = Player(constants.GAME_WINDOW_WIDTH // 2,
                        constants.GAME_WINDOW_HEIGHT // 2,
                        data_for_loading)
    else:
        player = Player(constants.GAME_WINDOW_WIDTH // 2,
                        constants.GAME_WINDOW_HEIGHT // 2)

    waterfall = Waterfall(100, 100)
    quests = []
    names_done_quests = []
    neutrals = [Neutral(100, 100, player.level)]

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

    camera = Camera((constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_HEIGHT))

    things = []

    key = Key(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
              random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT))
    things.append(key)

    shells_player = []
    min_enemies_amount = 40
    max_enemies_amount = 50
    # enemies = create_enemies(min_enemies_amount, max_enemies_amount, player.level)
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
                    player.amount_health = player.amount_health - enemy.amount_damage
                    if player.amount_health < 1:
                        return game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_pause_menu()
                if event.key == pygame.K_F5:
                    save_game([player])
                if event.key == pygame.K_F9:
                    load_game()
                if event.key == pygame.K_SPACE:
                    shells = player.attack()
                    shells_player.extend(shells)
                if event.key == pygame.K_i:
                    player.show_inventory(main_game_window)
                if event.key == pygame.K_c:
                    player.change_weapon()

        main_game_window.fill(int())

        game_map.update(main_game_window)
        for tile in game_map.map_tiles:
            offset = camera.get_offset()
            tile.rect.centerx -= offset[0]
            tile.rect.centery -= offset[1]

        for chest in chests:
            offset = camera.get_offset()
            chest.rect.centerx -= offset[0]
            chest.rect.centery -= offset[1]
            chest.update(main_game_window)
            if pygame.sprite.collide_rect(player, chest) and pygame.key.get_pressed()[pygame.K_e]:
                additional_potions = chest.open(player.is_key_in_inventory())
                if additional_potions is not None:
                    for additional_thing in additional_potions:
                        if additional_thing != 0:
                            things.append(additional_thing)

        for potion in things:
            potion.update(main_game_window)
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

        waterfall.update(main_game_window)
        offset = camera.get_offset()
        waterfall.rect.centerx -= offset[0]
        waterfall.rect.centery -= offset[1]
        for neutral in neutrals:
            neutral.update(main_game_window)
            neutral.rect.centerx -= offset[0]
            neutral.rect.centery -= offset[1]

        for tree in trees:
            tree.update(main_game_window)
            offset = camera.get_offset()
            tree.rect.centerx -= offset[0]
            tree.rect.centery -= offset[1]

        for shell in shells_player:
            if shell:
                shell.update(main_game_window)
                offset = camera.get_offset()
                shell.rect.centerx -= offset[0]
                shell.rect.centery -= offset[1]

        for enemy in enemies:
            enemy.attack(player.rect.centerx, player.rect.centery)
            offset = camera.get_offset()
            enemy.rect.centerx -= offset[0]
            enemy.rect.centery -= offset[1]
            enemy.update(main_game_window)
            enemy.attack(player.rect.centerx, player.rect.centery)

        for enemy in enemies:
            for shell in shells_player:
                if shell:
                    if pygame.sprite.collide_rect(enemy, shell):
                        shells_player.remove(shell)
                        enemy.current_amount_health -= player.amount_damage
                        enemy.current_amount_health -= shell.amount_additional_damage

                        dx = float(player.rect.centerx - enemy.rect.centerx)
                        dy = float(player.rect.centery - enemy.rect.centery)
                        length = math.sqrt(dx ** 2 + dy ** 2)
                        enemy.is_enemy_angry = True
                        enemy.show_aggression_to_attack_player(dx, dy, length)

                        text = enemy.name
                        test_cur = enemy.current_amount_health
                        test_max = enemy.max_amount_health
                        if enemy.current_amount_health < 0:
                            player.current_experience += enemy.experience_for_killing

                            if enemy in enemies:
                                enemies.remove(enemy)
                            text = None
                            test_cur = None
                            test_max = None

        camera.update(player)
        player.update(main_game_window)

        for quest in quests:
            if not enemies:
                quest.completed = True
                player.current_experience += quest.experience
                if quest.title not in names_done_quests:
                    names_done_quests.append(quest.title)
                quests.remove(quest)

        if text is not None:
            Drawer.draw_bar(main_game_window, constants.GAME_WINDOW_WIDTH // 2, 10,
                            constants.UNNAMED_COLOR_HEALTH_BAR,
                            test_cur, test_max, 150, 15)
            Drawer.draw_text(main_game_window, text, 25, constants.WHITE_COLOR_TITLE_BLOCKS, constants.GAME_WINDOW_WIDTH // 2,
                             9)

        Drawer.draw_text(main_game_window, player.name, 15, constants.WHITE_COLOR_TITLE_BLOCKS,
                        player.rect.centerx,
                        player.rect.centery + player.rect.height // 2 + 5)
        Drawer.draw_bar(main_game_window, constants.GAME_WINDOW_WIDTH // 2, constants.GAME_WINDOW_HEIGHT*0.92,
                        constants.WHITE_COLOR_TITLE_BLOCKS,
                        player.current_experience, player.experience_to_up_level, constants.GAME_WINDOW_WIDTH//3, 5, True)
        Drawer.draw_bar(main_game_window, constants.GAME_WINDOW_WIDTH // 2 - 200, constants.GAME_WINDOW_HEIGHT - 70,
                        constants.STAMINA_BAR_COLOR, player.current_stamina,
                        player.max_stamina, constants.GAME_WINDOW_WIDTH//22, 14, True)

        pygame.display.flip()  # for double buffering
        clock.tick(constants.FPS_LOCKING)
    pygame.quit()


def show_pause_menu():
    Drawer.draw_text(main_game_window, 'Pause. Press <Enter> To Continue', 30, constants.WHITE_COLOR_TITLE_BLOCKS,
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
            Drawer.draw_text(main_game_window, menu_item, color_and_size[1], color_and_size[0],
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
        main_game_window.blit(menu_background, (0, 0))
        clock.tick(constants.FPS_LOCKING)


def show_start_menu():
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
        Drawer.draw_text(main_game_window, constants.GAME_WINDOW_TITLE, title_size, constants.WHITE_COLOR_TITLE_BLOCKS,
                         constants.GAME_WINDOW_WIDTH // 2, 100)

        x_to_paste_menu_item = constants.GAME_WINDOW_HEIGHT//3
        for menu_item, color_and_size in menu_items.items():
            Drawer.draw_text(main_game_window, menu_item, color_and_size[1], color_and_size[0],
                             constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
            x_to_paste_menu_item += constants.GAME_WINDOW_HEIGHT//15

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
                    set_color_active_menu_item(index_selected_menu_item, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    index_previous_selected_item = index_selected_menu_item
                    index_selected_menu_item -= 1
                    if index_selected_menu_item < 0:
                        index_selected_menu_item = 3
                    set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                    set_color_active_menu_item(index_selected_menu_item, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                if event.key == pygame.K_RETURN:
                    if index_selected_menu_item == 0:
                        is_menu_show = False
                    if index_selected_menu_item == 1:
                        show_game_loads()
                    if index_selected_menu_item == 2:
                        pass
                    if index_selected_menu_item == 3:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        main_game_window.blit(menu_background, (0, 0))
        clock.tick(constants.FPS_LOCKING)


def game_over():
    items = ['Последнее сохранение', 'Загрузить', 'Выйти']
    handlers = ['load_game()', 'show_game_loads()', 'exit(0)']
    Drawer.draw_text(main_game_window, 'You died. Press <Enter> To Restart Or <Escape> To Exit', 30,
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
            Drawer.draw_text(main_game_window, menu_item, color_and_size[1], color_and_size[0],
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
        main_game_window.blit(menu_background, (0, 0))
        clock.tick(constants.FPS_LOCKING)


def create_enemies(min_number_enemies, max_number_enemies, player_level):
    """
    Function creates enemies within the visible part of the screen
    :param min_number_enemies: lower limit of the number of enemies
    :param max_number_enemies: upper limit of the number of enemies
    :param player_level: need to set amount experience for killing
    :return: list of enemies
    """
    enemies_local = list()
    for i in range(min_number_enemies, max_number_enemies):
        x_for_appear_demon = random.randint(-constants.GAME_WINDOW_WIDTH*2, constants.GAME_WINDOW_WIDTH*2)
        y_for_appear_demon = random.randint(-constants.GAME_WINDOW_HEIGHT*2, constants.GAME_WINDOW_HEIGHT*2)
        enemy_local = demon.Demon(x_for_appear_demon, y_for_appear_demon, player_level)
        enemies_local.append(enemy_local)
    return enemies_local


def show_game_loads():
    savings = os.listdir(constants.DIRECTORY_WITH_SAVINGS)
    if not savings:
        run_game()

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
        Drawer.draw_text(main_game_window, constants.GAME_WINDOW_TITLE, title_size, constants.WHITE_COLOR_TITLE_BLOCKS,
                         constants.GAME_WINDOW_WIDTH // 2, 100)

        x_to_paste_menu_item = constants.GAME_WINDOW_HEIGHT//3
        for menu_item, color_and_size in menu_items.items():
            Drawer.draw_text(main_game_window, menu_item, color_and_size[1], color_and_size[0],
                             constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
            x_to_paste_menu_item += constants.GAME_WINDOW_HEIGHT//15

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    index_previous_selected_item = index_selected_menu_item
                    index_selected_menu_item += 1
                    if index_selected_menu_item > amount_files-1:
                        index_selected_menu_item = 0
                        index_previous_selected_item = amount_files-1
                    set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                    set_color_active_menu_item(index_selected_menu_item, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    index_previous_selected_item = index_selected_menu_item
                    index_selected_menu_item -= 1
                    if index_selected_menu_item < 0:
                        index_selected_menu_item = amount_files-1
                    set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS, 50)
                    set_color_active_menu_item(index_selected_menu_item, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM, 80)
                if event.key == pygame.K_RETURN:
                    load_game(savings[index_selected_menu_item])

        pygame.display.flip()
        main_game_window.blit(menu_background, (0, 0))
        clock.tick(constants.FPS_LOCKING)


def save_game(objects_for_saving):
    save_time = datetime.today()
    with open(f'savings/{save_time.strftime("%Y-%m-%d-%H.%M.%S")}.pickle', 'wb') as save_file:
        for game_object in objects_for_saving:
            pickle.dump(game_object.params_for_saving, save_file)


def load_game(file_name_for_loading=None):
    objects = []
    saves = os.listdir(constants.DIRECTORY_WITH_SAVINGS)
    if not saves:
        run_game()
    else:
        filename = os.path.join(constants.DIRECTORY_WITH_SAVINGS, os.listdir(constants.DIRECTORY_WITH_SAVINGS)[-1]) if file_name_for_loading is None \
            else os.path.join(constants.DIRECTORY_WITH_SAVINGS, file_name_for_loading)
        with open(filename, 'rb') as load_file:
            data = pickle.load(load_file)
            run_game(data)


main_game_window = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH,
                                            constants.GAME_WINDOW_HEIGHT))


def main():
    pygame.init()

    pygame.display.toggle_fullscreen()

    global main_game_window

    pygame.display.set_caption(constants.GAME_WINDOW_TITLE)
    icon = pygame.image.load('resources/images/icons/icon.png')
    pygame.display.set_icon(icon)

    show_start_menu()

    while run_game():
        pass


if __name__ == '__main__':
    main()
