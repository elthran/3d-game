class Proficiencies:
    def __init__(self, character):
        self.character = character
        self.attack_melee_distance = AttackMeleeDistance(character)
        self.damage_base = DamageBase(character)
        self.health = Health(character)
        self.movement_speed_base = MovementSpeedBase(character)


class CharacterProficiency:
    def __init__(self, character):
        self.character = character
        self.name = None  # Displayed to user
        self.description = None  # Displayed to user
        self.character_attribute = None  # If set, self.level increases when the attribute increases
        self.level = 0  # Used to determine the value
        self.hardcoded_value = None  # If this is defined on a character it overwrites the value

    @property
    def formula(self):
        raise ValueError("Must be defined.")  # The formula to calculate the value

    @property
    def value(self):
        if self.hardcoded_value:
            return self.hardcoded_value
        return self.formula

    @property
    def __str__(self):
        raise ValueError('Must be set in child class.')


class AttackMeleeDistance(CharacterProficiency):
    def __init__(self, character):
        super().__init__(character)
        self.name = 'AttackMeleeDistance '
        self.description = 'How far away you can reach enemies with an attack.'

    @property
    def formula(self):
        return self.level + 1


class DamageBase(CharacterProficiency):
    def __init__(self, character):
        super().__init__(character)
        self.name = 'BaseDamage '
        self.description = 'Determines physical damage.'
        self.character_attribute = character.attributes.strength

    @property
    def formula(self):
        return self.level * 1 + self.character_attribute.level * 1

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character_attribute.level} * 1'


class Health(CharacterProficiency):
    def __init__(self, character):
        super().__init__(character)
        self.name = 'Health'
        self.description = 'Determines maximum health.'
        self.character_attribute = character.attributes.vitality
        self._current = self.value

    @property
    def formula(self):
        return self.level * 1 + self.character_attribute.level * 5

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, new_value):
        self._current = max(min(self.value, new_value), 0)

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character_attribute.level} * 5'


class MovementSpeedBase(CharacterProficiency):
    def __init__(self, character):
        super().__init__(character)
        self.name = 'Speed'
        self.description = 'Determines movement speed.'
        self.character_attribute = character.attributes.agility

    @property
    def formula(self):
        return self.level * 1 + self.character_attribute.level * 5

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character_attribute.level} * 10'
