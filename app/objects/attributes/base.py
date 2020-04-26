class Attribute:
    def __init__(self, character, *args):
        self.character = character
        self.name = None
        self.description = None
        self.level = 1
        self.is_primary = False
