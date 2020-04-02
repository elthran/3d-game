class CharacterAttribute:
    def __init__(self, character):
        self.character = character
        self.name = None
        self.description = None
        self.level = 1


class Agility(CharacterAttribute):
    def __init__(self, character):
        CharacterAttribute.__init__(self, character)
        self.name = 'Agility '
        self.description = 'How fast your character can walk.'


class Strength(CharacterAttribute):
    def __init__(self, character):
        CharacterAttribute.__init__(self, character)
        self.name = 'Strength'
        self.description = 'How much damage your character does.'


class Vitality(CharacterAttribute):
    def __init__(self, character):
        CharacterAttribute.__init__(self, character)
        self.name = 'Vitality'
        self.description = 'How much health the character has.'
