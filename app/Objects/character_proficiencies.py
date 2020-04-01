class CharacterProficiency:
    def __init__(self):
        self.name = None  # Displayed to user
        self.description = None  # Displayed to user
        self.character_attribute = None  # If set, self.level increases when the attribute increases
        self.level = 0  # Used to determine the value

    @property
    def value(self):
        raise ValueError('Must be set in child class.')


class BaseDamage(CharacterProficiency):
    def __init__(self):
        CharacterProficiency.__init__(self)
        self.name = 'BaseDamage '
        self.description = 'Determines physical damage.'
        self.character_attribute = 'Strength'

    @property
    def value(self):
        return self.level * 1


class BaseHealth(CharacterProficiency):
    def __init__(self):
        CharacterProficiency.__init__(self)
        self.name = 'BaseHealth'
        self.description = 'Determines maximum health.'
        self.character_attribute = 'Vitality'

    @property
    def value(self):
        return self.level * 5


class MovementSpeed(CharacterProficiency):
    def __init__(self):
        CharacterProficiency.__init__(self)
        self.name = 'Vitality'
        self.description = 'Determines movement speed.'
        self.character_attribute = 'Agility'

    @property
    def value(self):
        return self.level * 10
