from app.objects.proficiencies import Proficiency


class Resistances(Proficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Resistances'
        self.description = 'Determines resistances to different damage types.'
        self.physical = 0
        self.magical = 0
        self.frost = 0