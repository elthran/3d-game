from app import Keys
from app.objects.heroes.interfaces import MutationInterface


class Necromancer(MutationInterface):
    def __init__(self, hero):
        self.hero = hero
        self.add_abilities()
        self.update_attributes()

    def add_abilities(self):
        pass

    def update_attributes(self):
        pass