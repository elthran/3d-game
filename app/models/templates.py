FRICTION = 150.0


class GameObject:
    def __init__(self, pos, model_name, model_animation, health_max, speed_max):
        self.actor = Actor(model_name, model_animation)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

        self.health_max = health_max
        self.health = health_max

        self.speed_max = speed_max

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.walking = False

        self.collider_name = self.__class__.__name__
        # Note the "collider_name"--this will be used for collision-events, later...
        collider_node = CollisionNode(self.collider_name)
        collider_node.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(collider_node)
        self.collider.setPythonTag("owner", self)
        self.collider.show()

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

    def cleanup(self):
        # Remove various nodes, and clear the Python-tag--see below!
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            base.cTrav.removeCollider(self.collider)
            base.pusher.removeCollider(self.collider)

        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None
