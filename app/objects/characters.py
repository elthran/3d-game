from app.Objects.physicals import PhysicalObject

FRICTION = 150.0


class CharacterObject(PhysicalObject):
    def __init__(self, pos, model_name, model_animation, health_max, speed_max):
        PhysicalObject.__init__(self, pos, model_name, model_animation)

        # self.character_skills = CharacterSkills()

        # self.character_attributes = CharacterAttributes()

        self.health_max = health_max
        self.health = health_max

        self.speed_max = speed_max

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