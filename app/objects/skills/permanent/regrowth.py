from app.objects.skills.base import Ability
from app.objects.effects.health_regeneration_rate import HealthRegenerationRate


class Regrowth(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Regrowth"
        self.skill_tree = "Brute"
        self.is_permanent = True
        self.bonus = 1

    @property
    def description(self):
        return f"Recover {self.bonus * (self.level + 1) * 100}% more health per second."

    def tool_belt_update(self, game, operation, key, hero, time_delta):
        self.update_direct(hero, time_delta)

    def update_direct(self, hero, time_delta):
        super().update(time_delta)
        pass

    def apply(self):
        effect = HealthRegenerationRate(source=self)
        effect.apply(target=self.character)

