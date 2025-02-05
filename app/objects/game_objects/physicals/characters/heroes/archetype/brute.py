from app.objects.game_objects.physicals.characters.heroes.interfaces import MutationInterface


class Brute(MutationInterface):
    def __init__(self, hero):
        self.name = self.__class__.__name__
        self.hero = hero
        self.add_abilities()
        self.update_attributes()

    def add_abilities(self):
        self.hero.abilities.activate_brute_skills()

    def update_attributes(self):
        self.hero.attributes.strength.is_primary = True
        self.hero.attributes.agility.level = 3
        self.hero.attributes.intellect.level = 0
        self.hero.attributes.strength.level = 5
        self.hero.attributes.vitality.level = 3
        self.hero.refresh()

