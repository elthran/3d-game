from app.objects.proficiencies import Proficiency


class MeleeAttack(Proficiency):
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