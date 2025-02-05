from app.objects.effects import Effect


class Stun(Effect):
    def __init__(self, source):
        super().__init__(source)
        self.name = "Stun!"
        self.description = "You can't move!"
        self.status_name = "stunned"
        self.duration = 5
        # Sets damage to 0

    def apply(self, target):
        super().apply(target)
        print(f"{self.source} is stunning {target}")

    def update(self, time_delta):
        self.target.proficiencies.melee_attack.override = 0
        self.duration -= time_delta
        if self.duration <= 0:
            self.end_effect()

    def end_effect(self):
        super().end_effect()
        self.target.proficiencies.melee_attack.override = None
