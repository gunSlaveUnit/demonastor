class Quest:
    def __init__(self):
        self.__completed = False

    @property
    def completed(self):
        return self.__completed

    @completed.setter
    def completed(self, new_value):
        self.__completed = new_value
