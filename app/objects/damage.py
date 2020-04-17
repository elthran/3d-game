class Damage:
    def __init__(self, source=None, physical=0, magical=0, frost=0, effects=None):
        self.source = source
        self.physical = physical
        self.magical = magical
        self.frost = frost
        self.effects = effects if effects else []

    def __iter__(self):
        return iter([self.physical, self.magical, self.frost])