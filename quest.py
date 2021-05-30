import random

import constants
from enemy import Enemy


class Quest:
    def __init__(self, player_level, quest_objects=None, location_border=None):
        self.__player_level = player_level
        if quest_objects is None:
            self.__condition = self.__create_quest_objects()
        else:
            self.__condition = quest_objects
        if location_border is None:
            self.__border = {
                'LEFT': 0,
                'RIGHT': constants.GAME_WINDOW_WIDTH,
                'UP': 0,
                'DOWN': constants.GAME_WINDOW_HEIGHT,
            }
        else:
            self.__border = location_border
        self.__completed = False
        self.__experience_for_ending = 200

        self.__title = 'Beginning Of Killing'

    def __create_quest_objects(self):
        return [
            Enemy(random.randint(0, constants.GAME_WINDOW_WIDTH), random.randint(0, constants.GAME_WINDOW_HEIGHT),
                  [[
                      'resources/images/enemy/enemy_moving_left.png'
                  ],
                  [
                      'resources/images/enemy/enemy_moving_right.png'
                  ],
                  [
                      'resources/images/enemy/enemy_moving_up.png'
                  ],
                  [
                       'resources/images/enemy/enemy_moving_down.png'
                  ]]
                  )
        ]

    @property
    def condition(self):
        return self.__condition

    @property
    def experience(self):
        return self.__experience_for_ending

    @property
    def title(self):
        return self.__title

    @property
    def completed(self):
        return self.__completed

    @completed.setter
    def completed(self, new_value):
        self.__completed = new_value
