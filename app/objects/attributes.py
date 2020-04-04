class Attributes:
    def __init__(self, character):
        self.character = character
        self.agility = Agility(character)
        self.strength = Strength(character)
        self.vitality = Vitality(character)

    def refresh(self):
        pass


class Attribute:
    def __init__(self, character):
        self.character = character
        self.name = None
        self.description = None
        self.level = 1


class Agility(Attribute):
    def __init__(self, character):
        super().__init__(character)
        self.name = 'Agility '
        self.description = 'How fast your character can walk.'


class Strength(Attribute):
    def __init__(self, character):
        super().__init__(character)
        self.name = 'Strength'
        self.description = 'How much damage your character does.'


class Vitality(Attribute):
    def __init__(self, character):
        super().__init__(character)
        self.name = 'Vitality'
        self.description = 'How much health the character has.'
