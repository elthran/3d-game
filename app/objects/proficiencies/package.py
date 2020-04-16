from app.objects.proficiencies.health import Health
from app.objects.proficiencies.mana import Mana
from app.objects.proficiencies.melee_attack import MeleeAttack
from app.objects.proficiencies.movement import Movement


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