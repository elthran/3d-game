from app.objects.game_objects.physicals.characters.heroes.interfaces import MutationInterface


class Undying(MutationInterface):
    def __init__(self, hero):
        self.hero = hero
        self.add_abilities()
        self.update_attributes()

    def add_abilities(self):
        pass

    def update_attributes(self):
        pass