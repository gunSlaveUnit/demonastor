import random

import Constants
from Enemy import Enemy


class Quest:
    def __init__(self, player_level, quest_objects=None, location_border=None):
        self._player_level = player_level
        if quest_objects is None:
            self._condition = self._create_quest_objects()
        else:
            self._condition = quest_objects
        if location_border is None:
            self._border = {
                'LEFT': 0,
                'RIGHT': Constants.GAME_WINDOW_WIDTH,
                'UP': 0,
                'DOWN': Constants.GAME_WINDOW_HEIGHT,
            }
        else:
            self._border = location_border
        self._completed = False
        self._experience_for_ending = 200

        self._title = 'Beginning Of Killing'

    @staticmethod
    def _create_quest_objects():
        return [
            Enemy(random.randint(0, Constants.GAME_WINDOW_WIDTH), random.randint(0, Constants.GAME_WINDOW_HEIGHT),
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
                  ),
            Enemy(random.randint(0, Constants.GAME_WINDOW_WIDTH), random.randint(0, Constants.GAME_WINDOW_HEIGHT),
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
                  ),
            Enemy(random.randint(0, Constants.GAME_WINDOW_WIDTH), random.randint(0, Constants.GAME_WINDOW_HEIGHT),
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
                  ),
            Enemy(random.randint(0, Constants.GAME_WINDOW_WIDTH), random.randint(0, Constants.GAME_WINDOW_HEIGHT),
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
                  ),
            Enemy(random.randint(0, Constants.GAME_WINDOW_WIDTH), random.randint(0, Constants.GAME_WINDOW_HEIGHT),
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
                  ),
            Enemy(random.randint(0, Constants.GAME_WINDOW_WIDTH), random.randint(0, Constants.GAME_WINDOW_HEIGHT),
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
                  ),
        ]

    @property
    def condition(self):
        return self._condition

    @property
    def experience(self):
        return self._experience_for_ending

    @property
    def title(self):
        return self._title

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, new_value):
        self._completed = new_value
