from GameObject import GameObject


class Key(GameObject):
    def __init__(self, center_x, center_y, basic_image):
        super().__init__(center_x, center_y, basic_image)
        self._resource_name = 'key'

    @property
    def resource_name(self):
        return self._resource_name
