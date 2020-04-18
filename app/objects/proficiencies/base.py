class Proficiency:
    def __init__(self, character, *args):
        self.character = character
        self.name = None  # Displayed to user
        self.description = None  # Displayed to user
        self.override = None

    @property
    def __str__(self):
        raise ValueError('Must be set in child class.')