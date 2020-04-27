from app.objects.effects import Effect


class HealthRegenerationRate(Effect):
    def __init__(self, source):
        super().__init__(source)
        self.name = "Health Regeneration"
        self.description = "You heal faster"
        self.status_name = "Healing faster"
        self.amount = 0.01
        self.duration = None

    def apply(self, target):
        super().apply(target)
        print(f"{self.source} is heal {target} faster")
        self.target.proficiencies.health.regeneration_bonus_amount += self.amount

    def update(self, time_delta):
        pass

    def end_effect(self):
        super().end_effect()

    def apply_effect(self):
        pass