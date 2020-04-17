class Effect:
    def __init__(self, source):
        self.source = source
        self.name = None
        self.description = None
        self.defender = None
        self.status_name = None

    def apply(self, defender):
        self.defender = defender
        defender.active_effects.append(self)

    def update(self, time_delta):
        print(f"{self.defender} is still {self.status_name}!")

    def end_effect(self):
        self.defender.active_effects.remove(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(name="{self.name}", description="{self.description}")'
