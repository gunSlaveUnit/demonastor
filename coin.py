import pygame

from game_enums import CoinTypes


class Coin(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y, init_coin_type):
        """
        Create a coin.
        :param init_center_x:
        :param init_center_y:
        :param init_coin_type: 0 - gold, 1 - silver, 2 - bronze
        """
        super().__init__()
        if init_coin_type == CoinTypes.GOLD:
            self.__image = pygame.image.load('resources/images/coins/gold_coin.png').convert()
        elif init_coin_type == CoinTypes.SILVER:
            self.__image = pygame.image.load('resources/images/coins/silver_coin.png').convert()
        elif init_coin_type == CoinTypes.BRONZE:
            self.__image = pygame.image.load('resources/images/coins/bronze_coin.png').convert()

        self.__rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, self.__rect)
