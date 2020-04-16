from app.objects.attributes import Attribute


class Intellect(Attribute):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Intellect '
        self.description = 'How much mana you have.'