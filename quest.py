import random

import constants
import demon
import player


class Quest:
    def __init__(self, quest_objects=None, location_border=None):
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

    def __create_quest_objects(self):
        return [
            demon.Demon
        ]

    @property
    def completed(self):
        return self.__completed

    @completed.setter
    def completed(self, new_value):
        self.__completed = new_value
