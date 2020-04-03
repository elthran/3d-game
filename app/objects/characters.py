from app.Objects.abilities import Abilities
from app.Objects.attributes import Attributes
from app.Objects.proficiencies import Proficiencies
from app.Objects.constants_physics import FRICTION
from app.Objects.physicals import PhysicalObject


class CharacterObject(PhysicalObject):
    def __init__(self, starting_position=None, model_name=None, model_animation=None):
        super().__init__(starting_position, model_name, model_animation)

        self.attributes = Attributes(self)
        self.proficiencies = Proficiencies(self)
        self.abilities = Abilities(self)
        self.walking = False
        self.invulnerable = False

    def update(self, time_delta):
        """
        If we're going faster than our maximum speed, set the velocity-vector's length to that maximum.
        If we're walking, don't worry about friction.
        Otherwise, use friction to slow us down.
        :param time_delta:
        :return:
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
        if self.invulnerable:
            pass
        else:
            self.proficiencies.health.current += health_delta
            if self.proficiencies.health.current > self.proficiencies.health.value:
                self.proficiencies.health.current = self.proficiencies.health.value
        print(f"{self.__class__.__name__} health: "
              f"{self.proficiencies.health.current}/{self.proficiencies.health.value}")
        self.update_health_visual()

    def update_health_visual(self):
        pass
