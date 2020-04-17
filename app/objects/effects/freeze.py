from panda3d.core import Vec3

from app.objects.effects import Effect


class Freeze(Effect):
    def __init__(self, source):
        super().__init__(source)
        self.name = "Freeze!"
        self.description = "Freezes you"
        self.timer = 5
        self.status_name = "frozen"

        self.defender = None

    def apply(self, defender):
        super().apply(defender)
        print(f"{self.source} is freezing {defender}")
        self.defender.velocity = Vec3(0, 0, 0)
        self.defender.acceleration = 0

    def update(self, time_delta):
        self.timer -= time_delta
        if self.timer <= 0:
            self.end_effect()

    def end_effect(self):
        super().end_effect()
        self.defender.acceleration = 300


