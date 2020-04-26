from ..base import Proficiency


class Resistance(Proficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Resistances'
        self.description = 'Determines resistances to different damage types.'
        self.reduction = 0