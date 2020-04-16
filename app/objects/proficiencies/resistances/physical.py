from app.objects.proficiencies.resistances import Resistance


class Physical(Resistance):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Physical Resistance'
        self.description = 'Determines resistances to physical damage.'
        self.reduction = 0.1