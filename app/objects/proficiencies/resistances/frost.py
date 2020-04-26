from .base import Resistance


class Frost(Resistance):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Frost Resistance'
        self.description = 'Determines resistances to frost damage.'
        self.reduction = 0.0