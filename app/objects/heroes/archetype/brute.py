from app import Keys
from app.objects.heroes.interfaces import MutationInterface


class Brute(MutationInterface):
    def __init__(self, hero):
        self.hero = hero
        self.add_abilities()
        self.update_attributes()

    def add_abilities(self):
        pass

    def update_attributes(self):
        self.hero.attributes.strength.is_primary = True
        self.hero.attributes.agility.level = 2
        self.hero.attributes.intellect.level = 0
        self.hero.attributes.strength.level = 5
        self.hero.attributes.vitality.level = 3
        self.hero.refresh()

