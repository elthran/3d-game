from app.objects.effects.health_maximum import HealthMaximum
from app.objects.skills.base import Ability


class ArcaneKnowledge(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Arcane Knowledge"
        self.skill_tree = "Scholar"
        self.is_permanent = True
        self.bonus = 5

    @property
    def description(self):
        return f"Gain {self.bonus * (self.level + 1)}% maximum mana."

    def tool_belt_update(self, game, operation, key, hero, time_delta):
        self.update_direct(hero, time_delta)

    def update_direct(self, hero, time_delta):
        super().update(time_delta)
        pass

    def apply(self):
        effect = HealthMaximum(source=self)
        effect.apply(target=self.character)

