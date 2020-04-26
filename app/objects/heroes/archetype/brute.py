from app import Keys
from ..base import Hero


class Brute(Hero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes.strength.is_primary = True
        self.archetype = "Brute"

        self.attributes.agility.level = 2
        self.attributes.intellect.level = 0
        self.attributes.strength.level = 5
        self.attributes.vitality.level = 3
        # Now we should refresh the proficiencies. This might not be needed now?
        self.refresh()

        self.initialize()

    def initialize(self):
        self.add_abilities()

    def add_abilities(self):
        pass


