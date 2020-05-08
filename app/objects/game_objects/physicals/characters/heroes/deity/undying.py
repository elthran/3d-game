from app.objects.game_objects.physicals.characters.heroes.interfaces import MutationInterface


class Undying(MutationInterface):
    def __init__(self, hero):
        self.hero = hero
        self.add_abilities()
        self.update_attributes()
        hero.religion = "Acolyte of the Undying"
        self.add_abilities()
        self.update_attributes()
        self.update_proficiencies()

    def add_abilities(self):
        pass

    def update_attributes(self):
        pass

    def update_proficiencies(self):
        self.hero.proficiencies.resistances.frost.reduction += 0.1
