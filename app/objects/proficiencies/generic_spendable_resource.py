from .base import Proficiency


class GenericSpendableResource(Proficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'GenericSpendableResource'
        self.description = 'GenericSpendableResource Description'
        self.base_maximum = 5
        self.bonus_maximum_amount = 0
        self.bonus_maximum_percentage = 1.00
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
        return (self.base_maximum + self.bonus_maximum_amount + self.hero_attribute_bonus) \
               * self.bonus_maximum_percentage

    @property
    def regeneration_amount(self):
        return self.regeneration_base_amount + self.regeneration_bonus_amount

    @property
    def hero_attribute_bonus(self):
        return 0
