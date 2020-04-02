class CharacterProficiency:
    def __init__(self, character):
        self.character = character
        self.name = None  # Displayed to user
        self.description = None  # Displayed to user
        self.character_attribute = None  # If set, self.level increases when the attribute increases
        self.level = 0  # Used to determine the value

    @property
    def value(self):
        raise ValueError('Must be set in child class.')

    @property
    def __str__(self):
        raise ValueError('Must be set in child class.')


class BaseDamage(CharacterProficiency):
    def __init__(self, character):
        CharacterProficiency.__init__(self, character)
        self.name = 'BaseDamage '
        self.description = 'Determines physical damage.'
        self.character_attribute = 'Strength'

    @property
    def value(self):
        return self.level * 1 + self.character.strength.level * 1

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character.strength.level} * 1'


class BaseHealth(CharacterProficiency):
    def __init__(self, character):
        CharacterProficiency.__init__(self, character)
        self.name = 'BaseHealth'
        self.description = 'Determines maximum health.'
        self.character_attribute = 'Vitality'

    @property
    def value(self):
        return self.level * 1 + self.character.vitality.level * 5

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character.vitality.level} * 5'


class MovementSpeed(CharacterProficiency):
    def __init__(self, character):
        CharacterProficiency.__init__(self, character)
        self.name = 'Speed'
        self.description = 'Determines movement speed.'
        self.character_attribute = 'Agility'

    @property
    def value(self):
        return self.level * 1 + self.character.agility.level * 10

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character.agility.level} * 10'
