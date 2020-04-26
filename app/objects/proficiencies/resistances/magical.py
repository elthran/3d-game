from .base import Resistance


class Magical(Resistance):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Magical Resistance'
        self.description = 'Determines resistances to magical damage.'
        self.reduction = 0.1