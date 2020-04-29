from app.objects.abilities.frost_ray import FrostRay
from app.objects.abilities.mana_armour import ManaArmour
from app.objects.abilities.melee_attack import MeleeAttack
from app.objects.abilities.regrowth import Regrowth


class Abilities:
    def __init__(self, character=None, enemies=None, allies=None):
        assert character, 'Requires character keyword.'
        assert enemies, 'Requires enemies keyword.'
        assert allies, 'Requires allies keyword.'

        self.character = character
        self.frost_ray = FrostRay(character, enemies, allies)
        self.melee_attack = MeleeAttack(character, enemies, allies)
        self.mana_armour = ManaArmour(character, enemies, allies)
        self.regrowth = Regrowth(character, enemies, allies)

    def refresh(self):
        pass

    def get_enabled(self):
        return [ability for ability in self if ability.is_equipped]

    def increase_skill_level_by_name(self, name, delta):
        getattr(self, name.lower().replace(" ", "_")).level += delta

    def __iter__(self):
        return iter([self.frost_ray,
                     self.melee_attack,
                     self.mana_armour,
                     self.regrowth])
