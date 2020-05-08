from app.objects.skills.base import Ability


class WarCry(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # health.add_observer(self)
        self.name = "War Cry"
        self.skill_tree = "Brute"
        self.bonus = 1.0
        self.mana_cost = 5
        self.duration = 5.0

    @property
    def description(self):
        return f"Gain {self.bonus * (self.level + 1) * 100}% melee damage for {self.duration} seconds."

    def tool_belt_update(self, game, operation, key, hero, time_delta):
        active = key.on
        self.update_direct(active, hero, time_delta)

    def update_direct(self, active, hero, time_delta):
        super().update(time_delta)

        if not active:
            return

        if self.character.proficiencies.mana.current >= self.mana_cost:
            self.character.proficiencies.mana.current -= self.mana_cost
            print("YOU PRESSED F. CASTING MANA ARMOUR")
            effect = ManaArmourEffect(source=self)
            effect.apply(target=self.character)
        else:
            print("Out of mana")