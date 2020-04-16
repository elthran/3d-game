from app.objects.attributes import Attribute


class Vitality(Attribute):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Vitality'
        self.description = 'How much health the character has.'