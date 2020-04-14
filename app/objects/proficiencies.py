class Proficiencies:
    def __init__(self, character=None):
        assert character, 'Requires character keyword.'

        self.character = character
        self.melee_attack = MeleeAttack(character)
        self.health = Health(character)
        self.mana = Mana(character)
        self.movement = Movement(character)

    def refresh(self):
        self.health.current = self.health.maximum
        self.mana.current = self.mana.maximum


class CharacterProficiency:
    def __init__(self, character, *args):
        self.character = character
        self.name = None  # Displayed to user
        self.description = None  # Displayed to user

    @property
    def __str__(self):
        raise ValueError('Must be set in child class.')


class GenericSpendableResource(CharacterProficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'GenericSpendableResource'
        self.description = 'GenericSpendableResource Description'
        self.base_maximum = 5
        self.bonus_maximum = 0
        self._current = self.base_maximum
        self.regeneration_base_amount = 0.01
        self.regeneration_bonus_amount = 0
        self.regeneration_cooldown_maximum = 100
        self._regeneration_cooldown_current = 0

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, new_value):
        if new_value < self.current:
            self.regeneration_cooldown_current = self.regeneration_cooldown_maximum
        self._current = max(min(self.maximum, new_value), 0)

    @property
    def regeneration_cooldown_current(self):
        return self._regeneration_cooldown_current

    @regeneration_cooldown_current.setter
    def regeneration_cooldown_current(self, new_value):
        self._regeneration_cooldown_current = max(min(self.regeneration_cooldown_maximum, new_value), 0)

    @property
    def maximum(self):
        return self.base_maximum + self.bonus_maximum

    @property
    def regeneration_amount(self):
        return self.regeneration_base_amount + self.regeneration_bonus_amount


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


class Health(GenericSpendableResource):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Health'
        self.description = 'Determines maximum health.'
        self.base_maximum = 5

    @property
    def maximum(self):
        return self.base_maximum + self.bonus_maximum + self.character.attributes.vitality.level * 1


class Mana(GenericSpendableResource):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Mana'
        self.description = 'Determines maximum mana.'
        self.base_maximum = 5

    @property
    def maximum(self):
        return self.base_maximum + self.bonus_maximum + self.character.attributes.intellect.level * 3


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
