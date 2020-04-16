from app.objects.attributes.agility import Agility
from app.objects.attributes.intellect import Intellect
from app.objects.attributes.strength import Strength
from app.objects.attributes.vitality import Vitality


class Attributes:
    def __init__(self, character=None):
        assert character, 'Requires character keyword.'

        self.character = character
        self.agility = Agility(character)
        self.intellect = Intellect(character)
        self.strength = Strength(character)
        self.vitality = Vitality(character)

    def refresh(self):
        pass