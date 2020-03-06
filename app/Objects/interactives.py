from app.Objects.templates import GameObject


class Interactive(GameObject):
    def __init__(self, pos, model_name, model_animation, health_max, speed_max):
        GameObject.__init__(self, pos, model_name, model_animation, health_max, speed_max)

    def update(self, player, time_delta):
        """
        In short, update as a GameObject, then run whatever enemy-specific logic is to be done.
        The use of a separate "run_logic" method allows us to customise that specific logic to the enemy,
        without re-writing the rest.

        :param player:
        :param time_delta:
        :return:
        """
        GameObject.update_position(self, time_delta)


class CrateInteractive(Interactive):
    def __init__(self, pos):
        Interactive.__init__(self,
                             pos=pos,
                             model_name="Models/Misc/trap",
                             model_animation={"stand": "Models/Misc/trap-stand"},
                             health_max=100.0,
                             speed_max=0.0)

        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.actor.loop("stand")



