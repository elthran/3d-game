from .base import Ability
from app.objects.effects.mana_armour import ManaArmourEffect


class ManaArmour(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # health.add_observer(self)
        self.name = "Mana Armour"
        self.description = '25% chance to lose mana instead of health'
        self.mana_cost = 1
        self.duration = 10

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