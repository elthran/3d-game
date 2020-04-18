from app.objects.effects import Effect


class ManaArmourEffect(Effect):
    def __init__(self, source):
        super().__init__(source)
        self.name = "Mana Armour"
        self.description = "25% you lose mana instead of health when taking damage"
        self.status_name = "mana armoured"
        self.duration = 2

    def apply(self, target):
        super().apply(target)
        print(f"{self.source} is protected by mana armour {target}")

    def update(self, time_delta):
        print("still frozen...")
        self.duration -= time_delta
        if self.duration <= 0:
            self.end_effect()

    def end_effect(self):
        super().end_effect()
        self.target.proficiencies.melee_attack.override = None


    def apply_effect(self):
        pass