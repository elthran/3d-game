from app.objects.effects import Effect


class HealthMaximum(Effect):
    def __init__(self, source):
        super().__init__(source)
        self.name = "Health Maximum"
        self.description = "Your maximum health is larger."
        self.status_name = "Healing faster"
        self.amount = source.bonus
        self.duration = None

    def apply(self, target):
        super().apply(target)
        print(f"{self.source} is raising {target} maximum health by {self.amount}%")
        self.target.proficiencies.health.bonus_maximum_percentage += self.amount

    def update(self, time_delta):
        pass

    def end_effect(self):
        super().end_effect()

    def apply_effect(self):
        pass