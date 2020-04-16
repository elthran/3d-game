from app.objects.proficiencies import Proficiency


class Movement(Proficiency):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Speed'
        self.description = 'Determines movement speed.'
        self.base_speed = 7
        self.bonus_speed = 0

    @property
    def speed(self):
        return self.base_speed + self.bonus_speed + self.character.attributes.agility.level * 1