from panda3d.core import Vec3

from app.objects.game_objects.game_objects import GameObject
from app.objects.game_objects.physicals.characters.characters import CharacterObject
from .base import Monster


class Melee(Monster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         model_name="Misc/simpleEnemy",
                         model_animation={"stand": "Misc/simpleEnemy-stand",
                                          "walk": "Misc/simpleEnemy-walk",
                                          "attack": "Misc/simpleEnemy-attack",
                                          "die": "Misc/simpleEnemy-die",
                                          "spawn": "Misc/simpleEnemy-spawn"},
                         sound_spawning="resources/sounds/enemySpawn.ogg",
                         sound_dying="resources/sounds/enemyDie.ogg",
                         **kwargs)

        self.proficiencies.melee_attack.base_attack_range = 0.75
        self.proficiencies.melee_attack.base_damage = 0
        self.proficiencies.health.regeneration_base_amount = 0
        self.proficiencies.movement.base_acceleration = 100
        self.refresh()
        self.abilities.melee_attack.toggle_enabled(True)

    def run_logic(self, player, time_delta):
        """
        In short: find the vector between this enemy and the player.
        If the enemy is far from the player, use that vector to move towards the player.
        Otherwise, just stop for now. Finally, face the player.
        """
        vector_to_player = player.actor.getPos() - self.actor.getPos()
        vector_to_player_2D = vector_to_player.getXy()
        distance_to_player = vector_to_player_2D.length()
        vector_to_player_2D.normalize()
        heading = self.y_vector.signedAngleDeg(vector_to_player_2D)
        self.firing_vector = Vec3(0, 0, 0) - self.actor.getPos()

        if distance_to_player > self.proficiencies.melee_attack.distance * 0.9:  # It is not close enough to attack
            attack_control = self.actor.getAnimControl("attack")
            if not attack_control.isPlaying():
                self.walking = True
                vector_to_player.setZ(0)
                vector_to_player.normalize()
                self.velocity += vector_to_player * self.acceleration * time_delta
        else:  # It is close enough to attack
            self.abilities.melee_attack.update_direct(True, self, time_delta)
            self.walking = False
            self.velocity.set(0, 0, 0)
            # If we're waiting for an attack to land...

        self.actor.setH(heading)

    def update_health(self, health_delta, source=None):
        CharacterObject.update_health(self, health_delta, source=source)
        self.update_health_visual()

    def update_health_visual(self):
        color_shade = self.proficiencies.health.current / self.proficiencies.health.maximum
        if color_shade < 0:
            color_shade = 0
        # The parameters here are red, green, blue, and alpha
        self.actor.setColorScale(color_shade, color_shade, color_shade, 1)

    def remove_object_from_world(self):
        for ability in self.abilities:
            ability.remove_object_from_world()

        GameObject.remove_object_from_world(self)
