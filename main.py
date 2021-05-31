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

# TODO: make an additional panel with some resources, for example, with potions

# TODO: Several main tasks:
# Map
# Quests
# Locations
# New opponents
# Skills

# TODO: we need to get camera offset just only once, not so much


import Game


def main():
    game = Game.Game()
    game.show_start_menu()


if __name__ == '__main__':
    main()
