from panda3d.core import CollisionNode, CollisionSphere, Vec3

from direct.actor.Actor import Actor


class PhysicalObject:
    def __init__(self, starting_position=None, model_name=None, model_animation=None):
        self.actor = self.create_actor(starting_position, model_name, model_animation)

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.collider_name = self.__class__.__name__
        # Note the "collider_name"--this will be used for collision-events, later...
        collider_node = CollisionNode(self.collider_name)
        collider_node.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(collider_node)
        self.collider.setPythonTag("owner", self)
        self.collider.show()

    def create_actor(self, starting_position, model_name, model_animation):
        self.actor = Actor(model_name, model_animation)
        self.actor.reparentTo(render)
        self.actor.setPos(starting_position)
        return self.actor

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