"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

In this file the program is started
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

# TODO: use properties in classes
# TODO: make collisions
# TODO: we need to add exceptions

# TODO: для сохранения мы можем просто пихать в качестве аргумента при создании объекта словарь
# TODO: можно добавить скриншоты и запись видео

# TODO: Several main tasks:
# Map
# Quests
# Locations
# New opponents
# Inventory
# Skills

import sys
import random
import math

import pygame

import map
import constants
from camera import Camera
from player import Player
import demon
from chest import Chest
from key import Key


def run_game():
    global main_game_window

    game_map = map.Map()

    player = Player(constants.GAME_WINDOW_WIDTH // 2,
                    constants.GAME_WINDOW_HEIGHT // 2)

    chests = [Chest(random.randint(-constants.GAME_WINDOW_WIDTH*2, constants.GAME_WINDOW_WIDTH*2),
                    random.randint(-constants.GAME_WINDOW_HEIGHT*2, constants.GAME_WINDOW_HEIGHT*2),
                    is_chest_need_key=False),
              Chest(random.randint(-constants.GAME_WINDOW_WIDTH*2, constants.GAME_WINDOW_WIDTH*2),
                    random.randint(-constants.GAME_WINDOW_HEIGHT*2, constants.GAME_WINDOW_HEIGHT*2),
                    is_chest_need_key=False),
              Chest(random.randint(-constants.GAME_WINDOW_WIDTH*2, constants.GAME_WINDOW_WIDTH*2),
                    random.randint(-constants.GAME_WINDOW_HEIGHT*2, constants.GAME_WINDOW_HEIGHT*2),
                    is_chest_need_key=False),
              Chest(random.randint(-constants.GAME_WINDOW_WIDTH*2, constants.GAME_WINDOW_WIDTH*2),
                    random.randint(-constants.GAME_WINDOW_HEIGHT*2, constants.GAME_WINDOW_HEIGHT*2),
                    is_chest_need_key=False),
              Chest(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
                    random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT),
                    is_chest_need_key=True)]

    camera = Camera((constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_HEIGHT))

    things = []

    key = Key(random.randint(-constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_WIDTH),
              random.randint(-constants.GAME_WINDOW_HEIGHT, constants.GAME_WINDOW_HEIGHT))
    things.append(key)

    shells_player = []
    min_enemies_amount = 10
    max_enemies_amount = 40
    enemies = create_enemies(min_enemies_amount, max_enemies_amount, player.level)

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
                if event.key == pygame.K_SPACE:
                    shell = player.attack()
                    shells_player.append(shell)
                if event.key == pygame.K_i:
                    player.show_inventory(main_game_window)

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
                        enemy.current_amount_health -= player.amount_damage - shell.amount_additional_damage

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

                            enemies.remove(enemy)
                            text = None
                            test_cur = None
                            test_max = None

        camera.update(player)
        player.update(main_game_window)

        if text is not None:
            draw_bar(main_game_window, constants.GAME_WINDOW_WIDTH // 2, 10,
                     constants.UNNAMED_COLOR_HEALTH_BAR,
                     test_cur, test_max, 150, 15)
            draw_text(main_game_window, text, 25, constants.WHITE_COLOR_TITLE_BLOCKS, constants.GAME_WINDOW_WIDTH // 2,
                      9)

        draw_text(main_game_window, player.name, 15, constants.WHITE_COLOR_TITLE_BLOCKS,
                  player.rect.centerx,
                  player.rect.centery + player.rect.height // 2 + 5)
        draw_bar(main_game_window, constants.GAME_WINDOW_WIDTH // 2, constants.GAME_WINDOW_HEIGHT // 2 + 220,
                 constants.WHITE_COLOR_TITLE_BLOCKS,
                 player.current_experience, player.experience_to_up_level, 204, 5)
        draw_bar(main_game_window, constants.GAME_WINDOW_WIDTH // 2 - 52, constants.GAME_WINDOW_HEIGHT - 70,
                 constants.STAMINA_BAR_COLOR, player.current_stamina,
                 player.max_stamina, 50, 10)

        pygame.display.flip()  # for double buffering
        clock.tick(constants.FPS_LOCKING)
    pygame.quit()


def show_pause_menu():
    draw_text(main_game_window, 'Pause. Press <Escape> To Continue', 30, constants.WHITE_COLOR_TITLE_BLOCKS,
              constants.GAME_WINDOW_WIDTH // 2, constants.GAME_WINDOW_HEIGHT // 2)

    clock = pygame.time.Clock()
    is_pause_over = False
    while not is_pause_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_pause_over = True

        pygame.display.update()
        clock.tick(constants.FPS_LOCKING)


def show_start_menu():
    # TODO: add mouse menu control
    def set_color_active_menu_item(index_active_menu_item, color):
        if index_active_menu_item == 0:
            menu_items['New Game'] = color
        if index_active_menu_item == 1:
            menu_items['Load Game'] = color
        if index_active_menu_item == 2:
            menu_items['Settings'] = color
        if index_active_menu_item == 3:
            menu_items['Exit'] = color

    menu_background = pygame.image.load(
        f'resources/images/backgrounds/background_{constants.GAME_WINDOW_WIDTH}_{constants.GAME_WINDOW_HEIGHT}.jpg'
    )

    menu_items = {
        'New Game': constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM,
        'Load Game': constants.WHITE_COLOR_TITLE_BLOCKS,
        'Settings': constants.WHITE_COLOR_TITLE_BLOCKS,
        'Exit': constants.WHITE_COLOR_TITLE_BLOCKS
    }
    index_selected_menu_item = 0

    is_menu_show = True
    clock = pygame.time.Clock()
    while is_menu_show:
        draw_text(main_game_window, constants.GAME_WINDOW_TITLE, 80, constants.WHITE_COLOR_TITLE_BLOCKS,
                  constants.GAME_WINDOW_WIDTH // 2, 80)

        x_to_paste_menu_item = 200
        for menu_item in menu_items.keys():
            draw_text(main_game_window, menu_item, 50, menu_items[menu_item],
                      constants.GAME_WINDOW_WIDTH // 2, x_to_paste_menu_item)
            x_to_paste_menu_item += 60

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
                    set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS)
                    set_color_active_menu_item(index_selected_menu_item, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    index_previous_selected_item = index_selected_menu_item
                    index_selected_menu_item -= 1
                    if index_selected_menu_item < 0:
                        index_selected_menu_item = 3
                    set_color_active_menu_item(index_previous_selected_item, constants.WHITE_COLOR_TITLE_BLOCKS)
                    set_color_active_menu_item(index_selected_menu_item, constants.DARK_ORANGE_HIGHLIGHTED_MENU_ITEM)
                if event.key == pygame.K_RETURN:
                    if index_selected_menu_item == 0:
                        is_menu_show = False
                    if index_selected_menu_item == 1:
                        pass
                    if index_selected_menu_item == 2:
                        pass
                    if index_selected_menu_item == 3:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        main_game_window.blit(menu_background, (0, 0))
        clock.tick(constants.FPS_LOCKING)


def game_over():
    draw_text(main_game_window, 'You died. Press <Enter> To Restart Or <Escape> To Exit', 30,
              constants.WHITE_COLOR_TITLE_BLOCKS,
              constants.GAME_WINDOW_WIDTH // 2, constants.GAME_WINDOW_HEIGHT // 2)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.update()
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
        x_for_appear_demon = random.randint(-constants.GAME_WINDOW_WIDTH * 2, constants.GAME_WINDOW_WIDTH * 2)
        y_for_appear_demon = random.randint(-constants.GAME_WINDOW_HEIGHT * 2, constants.GAME_WINDOW_HEIGHT * 2)
        enemy_local = demon.Demon(x_for_appear_demon, y_for_appear_demon, player_level)
        enemies_local.append(enemy_local)
    return enemies_local


def draw_text(surface, text, size, color, x, y):
    font_name = pygame.font.match_font('resources/fonts/samson_font.ttf')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_bar(surface, center_x, center_y, color, current_value, max_value, bar_length, bar_height):
    if current_value < 0:
        current_value = 0

    fill = (current_value * bar_length) // max_value
    if fill > bar_length:
        fill = bar_length
    outline_rect = pygame.Rect(center_x - bar_length // 2, center_y, bar_length, bar_height)
    fill_rect = pygame.Rect(center_x - bar_length // 2, center_y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, constants.WHITE_COLOR_TITLE_BLOCKS, outline_rect, 1)


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
