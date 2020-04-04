from math import copysign
from random import uniform

from panda3d.core import Vec2, CollisionNode, CollisionSegment, CollisionHandlerQueue

from app.objects.constants_physics import MASK_NOTHING, MASK_HERO, MASK_MONSTER, MASK_HERO_AND_MONSTER
from app.objects.characters import CharacterObject


class Monster(CharacterObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the collider for basic collisions. Monsters can collide into Heroes and Monsters
        self.collider.node().setIntoCollideMask(MASK_HERO_AND_MONSTER)
        self.collider.node().setFromCollideMask(MASK_HERO_AND_MONSTER)

        self.experience_rewarded = 1

    def update(self, time_delta, player=None):
        """
        In short, update as a PhysicalObject, then run whatever enemy-specific logic is to be done.
        The use of a separate "run_logic" method allows us to customise that specific logic to the enemy,
        without re-writing the rest.

        :param player:
        :param time_delta:
        :return:
        """
        CharacterObject.update(self, time_delta)

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
    def __init__(self, starting_position=None, model_name=None, model_animation=None, damage_taken_model=None):
        super().__init__(starting_position, model_name="Models/Misc/simpleEnemy",
                         model_animation={"stand": "Models/Misc/simpleEnemy-stand",
                                          "walk": "Models/Misc/simpleEnemy-walk",
                                          "attack": "Models/Misc/simpleEnemy-attack",
                                          "die": "Models/Misc/simpleEnemy-die",
                                          "spawn": "Models/Misc/simpleEnemy-spawn"})
        self.attributes.agility.level = 1
        self.attributes.strength.level = 1
        self.attributes.vitality.level = 1
        self.proficiencies.attack_melee_distance.hardcoded_value = 0.75
        self.acceleration = 100.0

        # Attack player code
        '''A mask that matches the player's, so that the enemy's attack will hit the player-character,
        but not the enemy-character (or other enemies)'''
        self.attack_segment = CollisionSegment(0, 0, 0, 1, 0, 0)
        segment_node = CollisionNode("enemyAttackSegment")
        segment_node.addSolid(self.attack_segment)
        segment_node.setFromCollideMask(MASK_HERO)
        segment_node.setIntoCollideMask(MASK_NOTHING)
        self.attack_segment_node_path = render.attachNewNode(segment_node)
        self.segment_queue = CollisionHandlerQueue()

        base.cTrav.addCollider(self.attack_segment_node_path, self.segment_queue)

        '''How much damage the enemy's attack does.
         That is, this results in the player-character's health being reduced by one.'''
        # The delay between the start of an attack, and the attack (potentially) landing
        self.attack_delay = 0.3
        self.attack_delay_timer = 0
        # How long to wait between attacks
        self.attack_wait_timer = 0
        # End of attack player code

        self.collider.node().setIntoCollideMask(MASK_MONSTER)
        '''end of bit masks?'''

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
        spawnControl = self.actor.getAnimControl("spawn")
        if spawnControl is not None and spawnControl.isPlaying():
            return

        vector_to_player = player.actor.getPos() - self.actor.getPos()
        vector_to_player_2D = vector_to_player.getXy()
        distance_to_player = vector_to_player_2D.length()
        vector_to_player_2D.normalize()
        heading = self.y_vector.signedAngleDeg(vector_to_player_2D)

        if distance_to_player > self.proficiencies.attack_melee_distance.value * 0.9:  # It is not close enough to attack
            attack_control = self.actor.getAnimControl("attack")
            if not attack_control.isPlaying():
                self.walking = True
                vector_to_player.setZ(0)
                vector_to_player.normalize()
                self.velocity += vector_to_player * self.acceleration * time_delta
                self.attack_wait_timer = 0.2
                self.attack_delay_timer = 0
        else:  # It is close enough to attack
            self.walking = False
            self.velocity.set(0, 0, 0)
            # If we're waiting for an attack to land...
            if self.attack_delay_timer > 0:
                self.attack_delay_timer -= time_delta
                # If the time has come for the attack to land...
                if self.attack_delay_timer <= 0:
                    # Check for a hit..
                    if self.segment_queue.getNumEntries() > 0:
                        self.segment_queue.sortEntries()
                        segment_hit = self.segment_queue.getEntry(0)

                        hit_node_path = segment_hit.getIntoNodePath()
                        if hit_node_path.hasPythonTag("owner"):
                            # Apply damage!
                            hit_object = hit_node_path.getPythonTag("owner")
                            hit_object.update_health(-self.proficiencies.damage_base.value)
                            self.attack_wait_timer = 1.0
            # If we're instead waiting to be allowed to attack...
            elif self.attack_wait_timer > 0:
                self.attack_wait_timer -= time_delta
                # If the wait has ended...
                if self.attack_wait_timer <= 0:
                    '''Start an attack! (And set the wait-timer to a random amount, to vary things a little bit.)'''
                    self.attack_wait_timer = uniform(0.5, 0.7)
                    self.attack_delay_timer = self.attack_delay
                    self.actor.play("attack")

        self.actor.setH(heading)

        '''Set the segment's start- and end- points. 
        "getQuat" returns a quaternion--a representation of orientation 
        or rotation--that represents the NodePath's orientation. This is useful here, 
        because Panda's quaternion class has methods to get forward, right, and up vectors for that orientation.
        Thus, what we're doing is making the segment point "forwards".'''
        self.attack_segment.setPointA(self.actor.getPos())
        self.attack_segment.setPointB(self.actor.getPos() + self.actor.getQuat().getForward() * self.proficiencies.attack_melee_distance.value)

    def update_health_visual(self):
        color_shade = self.proficiencies.health.current /self.proficiencies.health.value
        if color_shade < 0:
            color_shade = 0
        # The parameters here are red, green, blue, and alpha
        self.actor.setColorScale(color_shade, color_shade, color_shade, 1)

    def remove_object_from_world(self):
        base.cTrav.removeCollider(self.attack_segment_node_path)
        self.attack_segment_node_path.removeNode()
        self.remove_object_from_world()


class SlidingCrateMonster(Monster):
    def __init__(self, starting_position=None, model_name=None, model_animation=None, damage_taken_model=None):
        super().__init__(starting_position, model_name="Models/Misc/trap",
                         model_animation={"stand": "Models/Misc/trap-stand",
                                          "walk": "Models/Misc/trap-walk"})
        self.attributes.agility = 5
        self.attributes.strength = 1
        self.attributes.vitality = 1
        self.invulnerable = True

        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

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
