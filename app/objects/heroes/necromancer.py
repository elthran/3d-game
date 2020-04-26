from app import Keys
from ..base import Hero


class Necromancer(Hero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initialize()

    def initialize(self):
        self.add_abilities()

    def add_abilities(self):
        # Enable and add a key to toolbelt. Enable might not be needed now?
        self.abilities.frost_ray.enable()
        self.tool_belt.add_action(Keys.MOUSE_RIGHT, self.abilities.frost_ray, None)
