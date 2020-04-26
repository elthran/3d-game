from app import Keys
from app.objects.game_objects.physicals.characters.heroes.interfaces import MutationInterface


class Scholar(MutationInterface):
    def __init__(self, hero):
        self.hero = hero
        self.add_abilities()
        self.update_attributes()

    def add_abilities(self):
        self.hero.tool_belt.add_action(Keys.F, self.hero.abilities.mana_armour, None)

    def update_attributes(self):
        self.hero.attributes.intellect.is_primary = True
        self.hero.attributes.agility.level = 3
        self.hero.attributes.intellect.level = 6
        self.hero.attributes.strength.level = 1
        self.hero.attributes.vitality.level = 2
        self.hero.refresh()

