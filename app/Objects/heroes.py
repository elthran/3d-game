from panda3d.core import Vec3

from app.Objects.templates import GameObject


class Hero(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                            pos=Vec3(0, 0, 0),
                            model_name="Models/PandaChan/act_p3d_chan",
                            model_animation={"stand": "Models/PandaChan/a_p3d_chan_idle",
                                             "walk": "Models/PandaChan/a_p3d_chan_run"},
                            health_max=5,
                            speed_max=10)

        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)

        # Since our "Game" object is the "ShowBase" object, we can access it via the global "base" variable.
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.actor.loop("stand")

    def update(self, keys, time_delta):
        GameObject.update_position(self, time_delta)

        self.walking = False

        # If we're  pushing a movement key, add a relevant amount to our velocity.
        if keys["up"]:
            self.walking = True
            self.velocity.addY(self.acceleration * time_delta)
        if keys["down"]:
            self.walking = True
            self.velocity.addY(-self.acceleration * time_delta)
        if keys["left"]:
            self.walking = True
            self.velocity.addX(-self.acceleration * time_delta)
        if keys["right"]:
            self.walking = True
            self.velocity.addX(self.acceleration * time_delta)

        # This can be improved. If the character is walking go through the two possibilites (was standing/ was walking)
        # Else set them to loop stand.
        if self.walking:
            stand_control = self.actor.getAnimControl("stand")
            if stand_control.isPlaying():
                stand_control.stop()

            walk_control = self.actor.getAnimControl("walk")
            if not walk_control.isPlaying():
                self.actor.loop("walk")
        else:
            stand_control = self.actor.getAnimControl("stand")
            if not stand_control.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")
