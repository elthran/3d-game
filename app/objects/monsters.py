import random
from math import copysign

from panda3d.core import Vec3

from app.objects.abilities import Abilities
from app.objects.constants import CharacterTypes, Masks
from app.objects.characters import CharacterObject
from app.objects.game_objects import GameObject


class Monster(CharacterObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character_type = CharacterTypes.MONSTER
        # Set the collider for basic collisions. Monsters can collide into Heroes and Monsters
        self.collider.node().setFromCollideMask(Masks.HERO_AND_MONSTER)
        self.collider.node().setIntoCollideMask(Masks.MONSTER)

        self.experience_awarded_on_death = 1

        self.abilities = Abilities(character=self, enemies=Masks.HERO, allies=Masks.MONSTER)

    def update(self, time_delta, *args, hero=None, **kwargs):
        """
        In short, update as a PhysicalObject, then run whatever enemy-specific logic is to be done.
        The use of a separate "run_logic" method allows us to customise that specific logic to the enemy,
        without re-writing the rest.
        """
        super().update(time_delta, *args, **kwargs)
        assert hero, 'Requires hero keyword.'

        if self.dying:
            death_control = self.actor.getAnimControl("die")
            if death_control is None or not death_control.isPlaying():
                self.dead = True
                self.remove_object_from_world()
            return

        spawn_control = self.actor.getAnimControl("spawn")
        if spawn_control is not None and spawn_control.isPlaying():
            '''If the monster is still playing their spawn animation, they don't take action yet.'''
            return

        self.run_logic(hero, time_delta)

        # Play the appropriate animation. Can be improved? State-machine?
        # Should just be.... self.update_current_animation()
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
        """
        raise ValueError('run_logic must be implemented for each monster')


class TrainingDummyMonster(Monster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         model_name="resources/models/Misc/simpleEnemy",
                         model_animation={"stand": "resources/models/Misc/simpleEnemy-stand",
                                          "walk": "resources/models/Misc/simpleEnemy-walk",
                                          "attack": "resources/models/Misc/simpleEnemy-attack",
                                          "die": "resources/models/Misc/simpleEnemy-die",
                                          "spawn": "resources/models/Misc/simpleEnemy-spawn"},
                         sound_spawning="resources/sounds/enemySpawn.ogg",
                         sound_dying="resources/sounds/enemyDie.ogg",
                         **kwargs)

        self.proficiencies.melee_attack.base_attack_range = 0.75
        self.proficiencies.melee_attack.base_damage = 0
        self.proficiencies.movement.base_speed = 7
        self.proficiencies.health.regeneration_base_amount = 0
        self.acceleration = 100.0
        self.refresh()
        self.abilities.melee_attack.enable()
        self.abilities.frost_ray.enable()
        self.random_int = random.randint(1,10)

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
        self.firing_vector = Vec3(0,0,0) - self.actor.getPos()

        # if self.random_int > 5:
        #     self.abilities.frost_ray.update(None, True, self, time_delta)
        # else:
        #     self.abilities.frost_ray.update(None, False, self, time_delta)

        if distance_to_player > self.proficiencies.melee_attack.distance * 0.9:  # It is not close enough to attack
            attack_control = self.actor.getAnimControl("attack")
            if not attack_control.isPlaying():
                self.walking = True
                vector_to_player.setZ(0)
                vector_to_player.normalize()
                self.velocity += vector_to_player * self.acceleration * time_delta
                self.attack_wait_timer = 0.2
                self.attack_delay_timer = 0
        else:  # It is close enough to attack
            self.abilities.melee_attack.update(None, True, self, time_delta)
            self.walking = False
            self.velocity.set(0, 0, 0)
            # If we're waiting for an attack to land...

        self.actor.setH(heading)

    def update_health(self, health_delta, damage_dealer=None):
        CharacterObject.update_health(self, health_delta, damage_dealer=damage_dealer)
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


class SlidingCrateMonster(Monster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         model_name="resources/models/Misc/trap",
                         model_animation={"stand": "resources/models/Misc/trap-stand",
                                          "walk": "resources/models/Misc/trap-walk"},
                         **kwargs)
        self.proficiencies.movement.base_speed = 10
        self.invulnerable = True

        self.moveInX = False

        self.moveDirection = 0

        # This will allow us to prevent multiple collisions with the player during movement
        self.ignorePlayer = False

    def run_logic(self, player, time_delta):
        if self.moveDirection != 0:
            self.walking = True
            if self.moveInX:
                self.velocity.addX(self.moveDirection * self.acceleration * time_delta)
            else:
                self.velocity.addY(self.moveDirection * self.acceleration * time_delta)
        else:
            self.walking = False
            diff = player.actor.getPos() - self.actor.getPos()
            if self.moveInX:
                detector = diff.y
                movement = diff.x
            else:
                detector = diff.x
                movement = diff.y

            if abs(detector) < 0.5:
                self.moveDirection = copysign(1, movement)
