class Effect:
    def __init__(self, source):
        self.source = source
        self.name = None
        self.description = None
        self.target = None
        self.status_name = None

    def apply(self, target):
        self.target = target
        target.active_effects.append(self)

    def update(self, time_delta):
        pass
        # print(f"{self.target} is still {self.status_name}!")

    def end_effect(self):
        self.target.active_effects.remove(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(name="{self.name}", description="{self.description}")'
