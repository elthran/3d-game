from panda3d.core import CollisionNode, CollisionSphere, Vec2, Vec3

from direct.actor.Actor import Actor

from app.objects.game_objects import GameObject


class PhysicalObject(GameObject):
    """A physical object. Something that exists physically in the game world. Like a wall, monster, hero, etc.

    Attributes:
        actor (Actor): A 3d model.
        collider (Collider): A Collision object.
        damage_taken_model (dict): The path to the art asset.
        damage_taken_model_timer (int): ???
        damage_taken_model_duration (float): How long the damage_taken_model will play for.
        invulnerable (bool): If the model can take damage.
        velocity (Vec3): The starting velocity of the object. Default is 0.
        acceleration (Float): How fast this object can accelerate.
    """

    def __init__(self,
                 *args,
                 starting_position=None,
                 model_name=None,
                 model_animation=None,
                 damage_taken_model=None,
                 sound_spawning=None,
                 sound_dying=None,
                 sound_take_damage=None,
                 sound_walking=None,
                 sound_walking_collision=None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        assert starting_position, 'Requires starting_position keyword.'

        # Physics and models
        self.actor = self.create_actor(starting_position, model_name, model_animation)
        self.collider = self.create_collider()
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.damage_taken_model = self.create_damage_taken_model(damage_taken_model)
        self.damage_taken_model_timer = 0
        self.damage_taken_model_duration = 0.15

        # A reference vector, used to determine which way to face the Actor.
        # Since the character faces along the y-direction, we use the y-axis.
        self.y_vector = Vec2(0, 1)

        self.invulnerable = False

        # Sound
        self.sound_spawning = loader.loadSfx(sound_spawning) if sound_spawning else None
        if self.sound_spawning is not None:
            self.sound_spawning.play()
        self.sound_dying = loader.loadSfx(sound_dying) if sound_dying else None
        self.sound_take_damage = loader.loadSfx(sound_take_damage) if sound_take_damage else None
        self.sound_walking = loader.loadSfx(sound_walking) if sound_walking else None
        if self.sound_walking:
            self.sound_walking.setLoop(True)
        self.sound_walking_collision = loader.loadSfx(sound_walking_collision) if sound_walking_collision else None

    @staticmethod
    def create_actor(starting_position, model_name, model_animation):
        """Create the actor. An actor is simply an animated model.

        Args:
            starting_position (Vec3): A 3d vector of where to initially position the model
            model_name (str): The path to the art asset
            model_animation (dict): Animation names and the path to their animation
        Returns:
            The actor model.
        """
        if not model_name:
            return None
        actor = Actor(model_name, model_animation)
        actor.reparentTo(render)
        actor.setPos(starting_position)
        if model_animation.get('spawn'):
            actor.play("spawn")
        return actor

    def create_collider(self):
        """Creates the collider and attaches it to its actor's node.

        Returns:
            The collider.
        """
        collider_name = self.__class__.__name__
        collider_node = CollisionNode(collider_name)
        collider_node.addSolid(CollisionSphere(0, 0, 0, 0.3))
        collider = self.actor.attachNewNode(collider_node)
        collider.setPythonTag("owner", self)
        collider.show()  # So it's visible for debugging
        return collider

    def create_damage_taken_model(self, damage_taken_model):
        """Creates the alternate model which is shown when this object takes damage.

        Args:
            damage_taken_model (str): The path to the art asset for when the model receives damage.

        Returns:
            The damage_taken_model.
        """
        if not damage_taken_model:
            return None
        damage_taken_model = loader.loadModel(damage_taken_model)
        damage_taken_model.setLightOff()
        damage_taken_model.setZ(1.0)
        damage_taken_model.reparentTo(self.actor)
        damage_taken_model.hide()
        return damage_taken_model

    def update(self, time_delta, *args, **kwargs):
        super().update(time_delta, *args, **kwargs)
