class GameObject:
    """A basic game object. May have a model, an update, a clean-up, etc.
    """

    def __init__(self, *args, **kwargs):
        """
        Args:
            starting_position (Vec3): A 3d vector of where to initially position the model.
            model_name (str): The path to the art asset.
            model_animation (dict): Animation names and the path to their animation.
            damage_taken_model (str): The path to the art asset for when the model receives damage.
            character (CharacterObject): The character that possesses this.
        """
        self.collider = None
        self.actor = None

    def update(self, time_delta, *args, **kwargs):
        """
        If we're going faster than our maximum speed, set the velocity-vector's length to that maximum.
        If we're walking, don't worry about friction. Otherwise, use friction to slow us down.
        Args:
            time_delta (float): Time since the last frame?
        """
        pass

    def remove_object_from_world(self):
        """
        Remove the various nodes attaching the object to the world.
        """
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            base.cTrav.removeCollider(self.collider)
            base.pusher.removeCollider(self.collider)
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None
        self.collider = None
