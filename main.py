"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

In this file the program is started
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

# TODO: bind different characteristics to each other
# TODO: lots of numeric constants, we should to remove it
# TODO: use properties in classes
# TODO: make collisions
# TODO: change draw_text function. It need to paste a text into left down corner
# TODO: we need to add exceptions

# TODO: для сохранения мы можем просто пихать в качестве аргумента при создании объекта словарь
# TODO: можно добавить скриншоты и запись видео
# TODO: i don't like money icons in inventory

import sys
import random

import pygame

import map
import constants
from camera import Camera
from player import Player
import demon
from healthpotion import HealthPotion
from manapotion import ManaPotion
from coin import Coin
import game_enums
from chest import Chest


def run_game():
    global main_game_window

    game_map = map.Map()

    player = Player(constants.GAME_WINDOW_WIDTH // 2,
                    constants.GAME_WINDOW_HEIGHT // 2)

    coin = Coin(random.randint(0, constants.GAME_WINDOW_WIDTH), random.randint(0, constants.GAME_WINDOW_HEIGHT),
                game_enums.CoinTypes.GOLD)

    chest = Chest(random.randint(0, constants.GAME_WINDOW_WIDTH), random.randint(0, constants.GAME_WINDOW_HEIGHT),
                  is_chest_need_key=False)

    camera = Camera((800, 600))

    potions = []
    health_potions = [HealthPotion(random.randint(0, constants.GAME_WINDOW_WIDTH),
                                   random.randint(0, constants.GAME_WINDOW_HEIGHT)) for _ in
                      range(random.randint(5, 10))]

    mana_potions = [ManaPotion(random.randint(0, constants.GAME_WINDOW_WIDTH),
                               random.randint(0, constants.GAME_WINDOW_HEIGHT)) for _ in range(random.randint(5, 10))]

    potions.extend(health_potions)
    potions.extend(mana_potions)

    shells_player = []
    enemies = create_enemies(2, 10)

    text = None
    test_cur = None
    test_max = None

    time_to_count_attack = 0
    clock = pygame.time.Clock()
    is_game_exit = False
    while not is_game_exit:
        delta = clock.tick(constants.FPS_LOCKING)
        pygame.event.pump()
        if time_to_count_attack < 500:
            time_to_count_attack += delta

        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                if time_to_count_attack >= 500:
                    time_to_count_attack = 0
                    player.set_amount_health(player.get_amount_health() - enemy.get_amount_damage())
                if player.get_amount_health() < 1:
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
        for tile in game_map.get_map_tiles():
            camera.apply(tile)

        camera.apply(chest)
        chest.update(main_game_window)
        if pygame.sprite.collide_rect(player, chest) and pygame.key.get_pressed()[pygame.K_e]:
            chest.open()

        camera.update(player)
        player.update(main_game_window)

        camera.apply(coin)
        coin.update(main_game_window)

        for potion in potions:
            potion.update(main_game_window)
            camera.apply(potion)

            if pygame.sprite.collide_rect(player, potion) and pygame.key.get_pressed()[pygame.K_e]:
                player.append_thing_to_inventory(potion)
                potions.remove(potion)

        for shell in shells_player:
            if shell:
                camera.apply(shell)
                shell.update(main_game_window)

        for enemy in enemies:
            enemy.attack(player.get_rect().centerx, player.get_rect().centery)
            camera.apply(enemy)
            enemy.update(main_game_window)
            enemy.attack(player.get_rect().centerx, player.get_rect().centery)

        for enemy in enemies:
            for shell in shells_player:
                if shell:
                    if pygame.sprite.collide_rect(enemy, shell):
                        shells_player.remove(shell)
                        enemy.set_amount_health(enemy.get_current_amount_health() - player.get_amount_damage()
                                                - shell.get_amount_additional_damage())
                        text = enemy.get_name()
                        test_cur = enemy.get_current_amount_health()
                        test_max = enemy.get_max_amount_health()
                        if enemy.get_current_amount_health() < 0:
                            enemies.remove(enemy)
                            text = None
                            test_cur = None
                            test_max = None

        if text is not None:
            draw_bar(main_game_window, constants.GAME_WINDOW_WIDTH // 2, 10,
                     constants.UNNAMED_COLOR_HEALTH_BAR,
                     test_cur, test_max)
            draw_text(main_game_window, text, 25, constants.WHITE_COLOR_TITLE_BLOCKS, constants.GAME_WINDOW_WIDTH//2, 9)

        draw_text(main_game_window, player.get_name(), 15, constants.WHITE_COLOR_TITLE_BLOCKS,
                  player.get_rect().centerx,
                  player.get_rect().centery + player.get_rect().height // 2 + 5)

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

    menu_background = pygame.image.load('resources/images/backgrounds/menu_background.png')

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
                  constants.GAME_WINDOW_WIDTH // 2, 30)

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


def create_enemies(min_number_enemies, max_number_enemies):
    """
    Function creates enemies within the visible part of the screen
    :param min_number_enemies: lower limit of the number of enemies
    :param max_number_enemies: upper limit of the number of enemies
    :return: list of enemies
    """
    enemies_local = list()
    for i in range(min_number_enemies, max_number_enemies):
        x_for_appear_demon = random.randint(0, constants.GAME_WINDOW_WIDTH)
        y_for_appear_demon = random.randint(0, constants.GAME_WINDOW_HEIGHT)
        enemy_local = demon.Demon(x_for_appear_demon, y_for_appear_demon)
        enemies_local.append(enemy_local)
    return enemies_local


def draw_text(surface, text, size, color, x, y):
    font_name = pygame.font.match_font('resources/fonts/samson_font.ttf')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_bar(surface, center_x, center_y, color, current_value, max_value):
    if current_value < 0:
        current_value = 0

    bar_length = 150
    bar_height = 15

    fill = (current_value * bar_length) // max_value
    if fill > bar_length:
        fill = bar_length
    fill_rect = pygame.Rect(center_x-bar_length//2, center_y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)


main_game_window = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH,
                                            constants.GAME_WINDOW_HEIGHT))


def main():
    pygame.init()

    global main_game_window

    pygame.display.set_caption(constants.GAME_WINDOW_TITLE)
    icon = pygame.image.load('resources/images/icons/icon.png')
    pygame.display.set_icon(icon)

    show_start_menu()

    while run_game():
        pass


if __name__ == '__main__':
    main()
