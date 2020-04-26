from app import Keys
from ..base import Hero


class Scholar(Hero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes.intellect.is_primary = True

        self.attributes.agility.level = 2
        self.attributes.intellect.level = 6
        self.attributes.strength.level = 1
        self.attributes.vitality.level = 2
        self.refresh()

        self.initialize()

    def initialize(self):
        self.add_abilities()

    def add_abilities(self):
        self.tool_belt.add_action(Keys.F, self.abilities.mana_armour, None)
