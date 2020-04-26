from panda3d.core import Vec3

from app.objects.effects import Effect


class Freeze(Effect):
    def __init__(self, source):
        super().__init__(source)
        self.name = "Freeze!"
        self.description = "Freezes you"
        self.duration = 2
        self.status_name = "frozen"

        self.target = None

    def apply(self, target):
        super().apply(target)
        print(f"{self.source} is freezing {target}")

    def update(self, time_delta):
        self.target.proficiencies.movement.override = 0
        self.target.velocity = Vec3(0, 0, 0)

        self.duration -= time_delta
        if self.duration <= 0:
            self.end_effect()

    def end_effect(self):
        super().end_effect()
        self.target.proficiencies.movement.override = None


