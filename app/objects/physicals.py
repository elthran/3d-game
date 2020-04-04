from panda3d.core import CollisionNode, CollisionSphere, Vec3

from direct.actor.Actor import Actor


class PhysicalObject:
    def __init__(self, starting_position=None, model_name=None, model_animation=None, damage_taken_model=None):
        self.actor = self.create_actor(starting_position, model_name, model_animation)
        self.collider = self.create_collider()
        self.damage_taken_model = self.create_damage_taken_model(damage_taken_model)
        self.velocity = Vec3(0, 0, 0)  # Set starting velocity to 0
        self.acceleration = 300.0  # How quickly the model can accelerate

        self.damage_taken_model_timer = 0
        self.damage_taken_model_duration = 0.15

    @staticmethod
    def create_actor(starting_position, model_name, model_animation):
        actor = Actor(model_name, model_animation)
        actor.reparentTo(render)
        actor.setPos(starting_position)
        if model_animation.get('spawn'):
            actor.play("spawn")
        return actor

    def create_collider(self):
        collider_name = self.__class__.__name__
        collider_node = CollisionNode(collider_name)
        collider_node.addSolid(CollisionSphere(0, 0, 0, 0.3))
        collider = self.actor.attachNewNode(collider_node)
        collider.setPythonTag("owner", self)
        collider.show()  # So it's visible for debugging
        return collider

    def create_damage_taken_model(self, damage_taken_model):
        if not damage_taken_model:
            return None
        damage_taken_model = loader.loadModel(damage_taken_model)
        damage_taken_model.setLightOff()
        damage_taken_model.setZ(1.0)
        damage_taken_model.reparentTo(self.actor)
        damage_taken_model.hide()
        return damage_taken_model

    def remove_object_from_world(self):
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
