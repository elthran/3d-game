from .castable.war_cry import WarCry
from .castable.frost_ray import FrostRay
from .castable.mana_armour import ManaArmour
from .castable.melee_attack import MeleeAttack
from .permanent.regrowth import Regrowth
from .permanent.arcane_knowledge import ArcaneKnowledge
from .permanent.toughened import Toughened


class Abilities:
    def __init__(self, character=None, enemies=None, allies=None):
        assert character, 'Requires character keyword.'
        assert enemies, 'Requires enemies keyword.'
        assert allies, 'Requires allies keyword.'

        self.character = character
        self.enemies = enemies
        self.allies = allies

        self.melee_attack = MeleeAttack(character, enemies, allies)

        self.regrowth = None
        self.toughened = None
        self.war_cry = None
        self.frost_ray = None
        self.mana_armour = None
        self.arcane_knowledge = None

    @property
    def all_skills(self):
        return [self.melee_attack,
                self.regrowth,
                self.toughened,
                self.war_cry,
                self.frost_ray,
                self.mana_armour,
                self.arcane_knowledge]

    def refresh(self):
        pass

    def activate_brute_skills(self):
        self.regrowth = Regrowth(self.character, self.enemies, self.allies)
        self.toughened = Toughened(self.character, self.enemies, self.allies)
        self.war_cry = WarCry(self.character, self.enemies, self.allies)

    def activate_scholar_skills(self):
        self.frost_ray = FrostRay(self.character, self.enemies, self.allies)
        self.mana_armour = ManaArmour(self.character, self.enemies, self.allies)
        self.arcane_knowledge = ArcaneKnowledge(self.character, self.enemies, self.allies)

    def get_enabled(self):
        return [ability for ability in self if ability.is_equipped]

    def increase_skill_level_by_name(self, name, delta):
        getattr(self, name.lower().replace(" ", "_")).level += delta

    def __iter__(self):
        return iter([skill for skill in self.all_skills if skill is not None])
