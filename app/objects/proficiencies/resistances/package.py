from app.objects.proficiencies.resistances.frost import Frost
from app.objects.proficiencies.resistances.magical import Magical
from app.objects.proficiencies.resistances.physical import Physical


class Resistances:
    def __init__(self, character=None):
        assert character, 'Requires character keyword.'

        self.character = character
        self.physical = Physical(character)
        self.magical = Magical(character)
        self.frost = Frost(character)