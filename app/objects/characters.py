from app.objects.abilities import Abilities
from app.objects.attributes import Attributes
from app.objects.proficiencies import Proficiencies
from app.objects.constants_physics import FRICTION
from app.objects.physicals import PhysicalObject


class CharacterObject(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes = Attributes(self)
        self.proficiencies = Proficiencies(self)
        self.abilities = Abilities(self)
        self.walking = False
        self.invulnerable = False

        self.actor.loop("stand")

    def refresh(self):
        self.attributes.refresh()
        self.proficiencies.refresh()
        self.abilities.refresh()

    def update(self, time_delta):
        """
        If we're going faster than our maximum speed, set the velocity-vector's length to that maximum.
        If we're walking, don't worry about friction. Otherwise, use friction to slow us down.
        """
        speed = self.velocity.length()
        if speed > self.proficiencies.movement_speed_base.value:
            self.velocity.normalize()
            self.velocity *= self.proficiencies.movement_speed_base.value
            speed = self.proficiencies.movement_speed_base.value

        if not self.walking:
            friction_value = FRICTION * time_delta
            if friction_value > speed:
                self.velocity.set(0, 0, 0)
            else:
                friction_vector = -self.velocity
                friction_vector.normalize()
                friction_vector *= friction_value
                self.velocity += friction_vector

        # Move the character, using our velocity and the time since the last update.
        self.actor.setPos(self.actor.getPos() + self.velocity * time_delta)

    def update_health(self, health_delta):
        # if self.invulnerable:
        #     pass
        # else:
        previous_health = self.proficiencies.health.current

        self.proficiencies.health.current += health_delta
        if self.proficiencies.health.current > self.proficiencies.health.value:
            self.proficiencies.health.current = self.proficiencies.health.value
        if previous_health > 0 >= self.proficiencies.health.current:
            print("You died.")
        print(f"{self.__class__.__name__} health: "
              f"{self.proficiencies.health.current}/{self.proficiencies.health.value}")

    def update_health_visual(self):
        pass
