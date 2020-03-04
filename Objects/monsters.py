from math import copysign

from panda3d.core import Vec2

from Objects.templates import GameObject


class Monster(GameObject):
    def __init__(self, pos, model_name, model_animation, health_max, speed_max, collider_name):
        GameObject.__init__(self, pos, model_name, model_animation, health_max, speed_max, collider_name)

        self.experience_rewarded = 1

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

        self.run_logic(player, time_delta)

        # Play the appropriate animation. Can be improved? State-machine?
        if self.walking:
            walking_control = self.actor.getAnimControl("walk")
            if not walking_control.isPlaying():
                self.actor.loop("walk")
        else:
            spawn_control = self.actor.getAnimControl("spawn")
            if spawn_control is None or not spawn_control.isPlaying():
                attack_control = self.actor.getAnimControl("attack")
                if attack_control is None or not attack_control.isPlaying():
                    stand_control = self.actor.getAnimControl("stand")
                    if not stand_control.isPlaying():
                        self.actor.loop("stand")

    def run_logic(self, player, time_delta):
        """
        Needs to be implemented for each sub-class.

        :param player:
        :param time_delta:
        :return:
        """
        pass


class TrainingDummyMonster(Monster):
    def __init__(self, pos):
        Monster.__init__(self,
                         pos=pos,
                         model_name="Models/Misc/simpleEnemy",
                         model_animation={"stand" : "Models/Misc/simpleEnemy-stand",
                                          "walk" : "Models/Misc/simpleEnemy-walk",
                                          "attack" : "Models/Misc/simpleEnemy-attack",
                                          "die" : "Models/Misc/simpleEnemy-die",
                                          "spawn" : "Models/Misc/simpleEnemy-spawn"},
                         health_max=3.0,
                         speed_max=7.0,
                         collider_name="training_dummy_monster")

        self.attack_distance = 0.75

        self.acceleration = 100.0

        # A reference vector, used to determine
        # which way to face the Actor.
        # Since the character faces along
        # the y-direction, we use the y-axis.
        self.y_vector = Vec2(0, 1)

    def run_logic(self, player, time_delta):
        """
        In short: find the vector between this enemy and the player.
        If the enemy is far from the player, use that vector to move towards the player.
        Otherwise, just stop for now. Finally, face the player.

        :param player:
        :param time_delta:
        :return:
        """

        vector_to_player = player.actor.getPos() - self.actor.getPos()

        vector_to_player_2D = vector_to_player.getXy()
        distance_to_player = vector_to_player_2D.length()

        vector_to_player_2D.normalize()

        heading = self.y_vector.signedAngleDeg(vector_to_player_2D)

        if distance_to_player > self.attack_distance * 0.9:
            self.walking = True
            vector_to_player.setZ(0)
            vector_to_player.normalize()
            self.velocity += vector_to_player * self.acceleration * time_delta
        else:
            self.walking = False
            self.velocity.set(0, 0, 0)

        self.actor.setH(heading)
