from .base import Resistance


class Fire(Resistance):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Fire Resistance'
        self.description = 'Determines resistances to fire damage.'
        self.reduction = 0.0