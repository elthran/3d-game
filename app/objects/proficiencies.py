class Proficiencies:
    def __init__(self, character=None):
        assert character, 'Requires character keyword.'

        self.character = character
        self.melee_attack = MeleeAttack(character)
        self.health = Health(character)
        self.movement = Movement(character)

    def refresh(self):
        self.health.current = self.health.maximum


class CharacterProficiency:
    def __init__(self, character, *args):
        self.character = character
        self.name = None  # Displayed to user
        self.description = None  # Displayed to user

    @property
    def __str__(self):
        raise ValueError('Must be set in child class.')


class MeleeAttack(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'AttackMeleeDistance '
        self.description = 'How far away you can reach enemies with an attack.'
        self.base_damage = 1
        self.bonus_damage = 0
        self.base_range = 1
        self.bonus_range = 0

    @property
    def damage(self):
        return self.base_damage + self.bonus_damage + self.character.attributes.strength.level * 1

    @property
    def distance(self):
        return self.base_range + self.bonus_range


class Health(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Health'
        self.description = 'Determines maximum health.'
        self.base_maximum = 5
        self.bonus_maximum = 0
        self._current = self.base_maximum
        self.base_regeneration = 0.1
        self.bonus_regeneration = 0

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, new_value):
        self._current = max(min(self.maximum, new_value), 0)

    @property
    def maximum(self):
        return self.base_maximum + self.bonus_maximum + self.character.attributes.vitality.level * 1


class Movement(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Speed'
        self.description = 'Determines movement speed.'
        self.base_speed = 7
        self.bonus_speed = 0

    @property
    def speed(self):
        return self.base_speed + self.bonus_speed + self.character.attributes.agility.level * 1
