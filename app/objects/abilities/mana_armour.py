from app.objects.abilities import Ability


class ManaArmour(Ability):
    def __init__(self, health, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # health.add_observer(self)
        self.name = "Mana Armour"
        self.description = '25% chance to lose mana instead of health'