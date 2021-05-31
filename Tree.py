from GameObject import GameObject


class Tree(GameObject):
    def __init__(self, center_x, center_y, basic_image):
        super().__init__(center_x, center_y, basic_image=basic_image)

    def update(self, surface, *args, **kwargs):
        self._draw(surface)

    def _draw(self, surface, *args, **kwargs):
        surface.blit(self._image, self._rect)
