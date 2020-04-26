from .base import Attribute


class Strength(Attribute):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Strength'
        self.description = 'How much damage your character does.'