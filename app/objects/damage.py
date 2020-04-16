class Damage:
    def __init__(self, source=None, physical=0, magical=0, frost=0):
        self.source = source
        self.physical = physical
        self.magical = magical
        self.frost = frost

    def time_normalized_damage(self, time_delta):
        return Damage(source=self.source,
                      physical=self.physical * time_delta,
                      magical=self.magical * time_delta,
                      frost=self.frost * time_delta)

    def __iter__(self):
        return iter([self.physical, self.magical, self.frost])