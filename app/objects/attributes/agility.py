from app.objects.attributes import Attribute


class Agility(Attribute):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Agility '
        self.description = 'How fast your character can walk.'