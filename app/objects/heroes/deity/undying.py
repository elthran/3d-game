from app import Keys
from ..base import Hero


class Undying(Hero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.religion = "Undying"

        self.initialize()

    def initialize(self):
        self.add_abilities()

    def add_abilities(self):
        pass
