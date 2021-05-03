import pygame


class Key(pygame.sprite.Sprite):
    def __init__(self, init_center_x, init_center_y):
        super().__init__()
        self.__image = pygame.image.load('resources/images/chests/key.png').convert()
        self.__rect = self.__image.get_rect()
        self.__rect.centerx = init_center_x
        self.__rect.centery = init_center_y
        self.__resource_name = 'key'

    def update(self, surface):
        self.__draw(surface)

    def __draw(self, surface):
        surface.blit(self.__image, self.__rect)

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, new_value):
        self.__rect = new_value

    @property
    def resource_name(self):
        return self.__resource_name
