class Proficiencies:
    def __init__(self, character=None):
        assert character, 'Requires character keyword.'

        self.character = character
        self.attack_melee_distance = AttackMeleeDistance(character)
        self.attack_delay = AttackDelay(character)
        self.damage_base = DamageBase(character)
        self.health = Health(character)
        self.movement_speed_base = MovementSpeedBase(character)

    def refresh(self):
        self.health.current = self.health.value


class CharacterProficiency:
    def __init__(self, character, *args):
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
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'AttackMeleeDistance '
        self.description = 'How far away you can reach enemies with an attack.'

    @property
    def formula(self):
        return self.level + 1


class AttackDelay(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'AttackDelay '
        self.description = 'How long until you can attack again.'
        self.hit_landing_delay = 0  # How long from start of swing to hitting an enemy

    @property
    def formula(self):
        return self.level + 0.3


class DamageBase(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'BaseDamage '
        self.description = 'Determines physical damage.'
        self.character_attribute = self.character.attributes.strength

    @property
    def formula(self):
        return self.level * 1 + self.character_attribute.level * 1

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character_attribute.level} * 1'


class Health(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Health'
        self.description = 'Determines maximum health.'
        self.character_attribute = self.character.attributes.vitality
        self._current = self.value

    @property
    def formula(self):
        return self.level * 1 + self.character_attribute.level * 5

    @property
    def current(self):
        return self._current

    # @value.setter
    # def value(self, new_value):
    #     # If you lower max health, also lower current health
    #     self._current = min(self._current, new_value)

    @current.setter
    def current(self, new_value):
        self._current = max(min(self.value, new_value), 0)

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character_attribute.level} * 5'


class MovementSpeedBase(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Speed'
        self.description = 'Determines movement speed.'
        self.character_attribute = self.character.attributes.agility

    @property
    def formula(self):
        return self.level * 1 + self.character_attribute.level * 5

    @property
    def __str__(self):
        return f'{self.level} * 1 + {self.character_attribute.level} * 10'
