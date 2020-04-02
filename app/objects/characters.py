from app.Objects.character_attributes import Agility, Strength, Vitality
from app.Objects.character_proficiencies import BaseDamage, BaseHealth, MovementSpeed
from app.Objects.constants_physics import FRICTION
from app.Objects.physicals import PhysicalObject


class CharacterObject(PhysicalObject):
    def __init__(self, starting_position=None, model_name=None, model_animation=None):
        super().__init__(starting_position, model_name, model_animation)

        self.agility = Agility(self)
        self.strength = Strength(self)
        self.vitality = Vitality(self)

        self.base_damage = BaseDamage(self)
        self.base_health = BaseHealth(self)
        self.movement_speed = MovementSpeed(self)

        self.health_max = 10
        self.health = 10

        self.speed_max = 10

        self.walking = False

    def update_position(self, time_delta):
        """
        If we're going faster than our maximum speed, set the velocity-vector's length to that maximum.
        If we're walking, don't worry about friction.
        Otherwise, use friction to slow us down.
        :param time_delta:
        :return:
        """
        speed = self.velocity.length()
        if speed > self.speed_max:
            self.velocity.normalize()
            self.velocity *= self.speed_max
            speed = self.speed_max

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
        self.health += health_delta

        if self.health > self.health_max:
            self.health = self.health_max