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

import sys
import random

import pygame

import constants
from player import Player
import demon
from potion import Potion


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


def draw_text(surface, text, size, x, y):
    font_name = pygame.font.match_font('samson_font.ttf')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_bar(surface, x, y, color, value):
    if value < 0:
        value = 0

    bar_length = 70
    bar_height = 6

    fill = (value / 100) * bar_length
    if fill > bar_length:
        fill = bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)


def main():
    pygame.init()

    main_game_window = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH,
                                                constants.GAME_WINDOW_HEIGHT))
    pygame.display.set_caption(constants.GAME_WINDOW_TITLE)
    icon = pygame.image.load('Icon.png')
    pygame.display.set_icon(icon)

    player = Player(constants.GAME_WINDOW_WIDTH // 2,
                    constants.GAME_WINDOW_HEIGHT // 2)

    shells_player = []
    enemies = create_enemies(2, 10)

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
                    is_game_exit = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_game_exit = True
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shell = player.attack()
                    shells_player.append(shell)

        main_game_window.fill(int())

        player.update(main_game_window)

        for shell in shells_player:
            shell.update(main_game_window)

        for enemy in enemies:
            enemy.update(main_game_window)
            enemy.attack(player.get_rect().centerx, player.get_rect().centery)

        for enemy in enemies:
            for shell in shells_player:
                if pygame.sprite.collide_rect(enemy, shell):
                    shells_player.remove(shell)
                    enemy.set_amount_health(enemy.get_amount_health() - player.get_amount_damage()
                                            - shell.get_amount_additional_damage())
                    if enemy.get_amount_health() < 0:
                        enemies.remove(enemy)

        for enemy in enemies:
            draw_bar(main_game_window, enemy.get_rect().centerx - 35,
                     enemy.get_rect().centery - enemy.get_rect().height // 2 - 7,
                     (255, 0, 0),
                     enemy.get_amount_health())
            draw_text(main_game_window, enemy.get_name(), 15,
                      enemy.get_rect().centerx,
                      enemy.get_rect().centery - enemy.get_rect().height // 2 - 18)

        draw_bar(main_game_window, player.get_rect().centerx - 35,
                 player.get_rect().centery + player.get_rect().height // 2 + 15,
                 (255, 0, 0), player.get_amount_health())
        draw_text(main_game_window, player.get_name(), 15,
                  player.get_rect().centerx,
                  player.get_rect().centery + player.get_rect().height // 2 + 5)

        pygame.display.flip()  # for double buffering
        clock.tick(constants.FPS_LOCKING)
    pygame.quit()


if __name__ == '__main__':
    main()
