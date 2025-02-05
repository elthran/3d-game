from app.objects.skills.base import Ability
from app.objects.effects.mana_armour import ManaArmourEffect


class ManaArmour(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # health.add_observer(self)
        self.name = "Mana Armour"
        self.skill_tree = "Scholar"
        self.bonus = 0.1

    @property
    def description(self):
        return f"Have a {self.bonus * (self.level + 1) * 100}% chance\n" \
            f"to lose mana instead of health."

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