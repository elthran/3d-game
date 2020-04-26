from .base import Proficiency


class Movement(Proficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Speed'
        self.description = 'Determines movement speed.'
        self.base_speed = 7
        self.bonus_speed = 0
        self.base_acceleration = 300
        self.bonus_acceleration = 0
        self.override = None

    @property
    def acceleration(self):
        if self.override is not None:
            return float(self.override)
        return self.base_acceleration + self.bonus_acceleration

    @property
    def speed_maximum(self):
        return self.base_speed + self.bonus_speed + self.character.attributes.agility.level

