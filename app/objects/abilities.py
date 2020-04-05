from panda3d.core import CollisionHandlerQueue, CollisionNode, CollisionRay, Vec3, PointLight, Vec4, CollisionSegment

from app.objects.game_objects import GameObject
from .constants_physics import MASK_MONSTER, MASK_NOTHING, MASK_HERO, MASK_HERO_AND_MONSTER
from .physicals import PhysicalObject

import math
import random


class Abilities:
    def __init__(self, character, enemies, allies):
        self.character = character
        self.frost_ray = FrostRay(character=character, enemies=enemies, allies=allies)
        self.melee_attack = MeleeAttack(character=character, enemies=enemies, allies=allies)

    def refresh(self):
        pass

    def __iter__(self):
        return iter([self.frost_ray, self.melee_attack])


class Ability(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character = kwargs.pop('character')
        self.enemies = kwargs.pop('enemies')
        self.allies = kwargs.pop('allies')
        self.model = None  # The basic model of the animation
        self.model_collision = None  # The model when the animation collides with another object
        self.damage = None
        self.damage_per_second = None
        if self.enemies == 'Monsters':
            self.from_collider_attack = MASK_MONSTER
            self.from_collider_protect = MASK_HERO
        elif self.enemies == 'Heroes':
            self.from_collider_attack = MASK_HERO
            self.from_collider_protect = MASK_MONSTER
        self.from_collider_all = MASK_HERO_AND_MONSTER
        self.into_collider = MASK_NOTHING
        self.enabled = False

    def enable(self):
        self.enabled = True

    def update(self, time_delta, **kwargs):
        pass

    def remove_object_from_world(self):
        pass


class FrostRay(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Frost Ray"
        self.description = "Shoot a ray of frost at an enemy."
        self.damage_per_second = 5.0

        self.physics_init()
        self.display_init()

    def physics_init(self):
        self.ray = CollisionRay(0, 0, 0, 0, 1, 0)
        ray_node = CollisionNode(self.__class__.__name__)
        # After we've made our ray-node:
        ray_node.setFromCollideMask(self.from_collider_attack)
        ray_node.setIntoCollideMask(self.into_collider)
        ray_node.addSolid(self.ray)
        self.ray_node_path = render.attachNewNode(ray_node)
        self.ray_queue = CollisionHandlerQueue()
        '''We want this ray to collide with things, so tell our traverser about it. However, note that,
        unlike with "CollisionHandlerPusher", we don't have to tell our "CollisionHandlerQueue" about it.'''
        base.cTrav.addCollider(self.ray_node_path, self.ray_queue)

    def display_init(self):
        '''The laser model: A nice laser-beam model to show our laser'''
        self.model = loader.loadModel("Models/Misc/bambooLaser")
        self.model.reparentTo(self.character.actor)
        self.model.setZ(1.5)
        # This prevents lights from affecting this particular node
        self.model.setLightOff()
        # We don't start out firing the laser, so we have it initially hidden.
        self.model.hide()

        '''The laser's hit animation'''
        self.model_collision = loader.loadModel("Models/Misc/bambooLaserHit")
        self.model_collision.reparentTo(render)
        self.model_collision.setZ(1.5)
        self.model_collision.setLightOff()
        self.model_collision.hide()

        self.beam_hit_pulse_rate = 0.15
        self.beam_hit_timer = 0

        self.beam_hit_light = PointLight("beamHitLight")
        self.beam_hit_light.setColor(Vec4(0.1, 1.0, 0.2, 1))
        # These "attenuation" values govern how the light
        # fades with distance. They are, respectively,
        # the constant, linear, and quadratic coefficients
        # of the light's falloff equation.
        # I experimented until I found values that
        # looked nice.
        self.beam_hit_light.setAttenuation((1.0, 0.1, 0.5))
        self.beam_hit_light_node_path = render.attachNewNode(self.beam_hit_light)
        # Note that we haven't yet applied the light to
        # a NodePath, and so it won't yet illuminate
        # anything.
        # --------------------------------------------------------------

    def update(self, active=None, firing_vector=None, origin=None, time_delta=None):
        # In short, run a timer, and use the timer in a sine-function
        # to pulse the scale of the beam-hit model. When the timer
        # runs down (and the scale is at its lowest), reset the timer
        # and randomise the beam-hit model's rotation.
        self.beam_hit_timer -= time_delta
        if self.beam_hit_timer <= 0:
            self.beam_hit_timer = self.beam_hit_pulse_rate
            self.model_collision.setH(random.uniform(0.0, 360.0))
        self.model_collision.setScale(math.sin(self.beam_hit_timer * 3.142 / self.beam_hit_pulse_rate) * 0.4 + 0.9)

        if active:
            if self.ray_queue.getNumEntries() > 0:
                scored_hit = False
                self.ray_queue.sortEntries()
                ray_hit = self.ray_queue.getEntry(0)
                hit_pos = ray_hit.getSurfacePoint(render)
                hit_node_path = ray_hit.getIntoNodePath()  # Into node model name?
                if hit_node_path.hasPythonTag("owner"):
                    hit_object = hit_node_path.getPythonTag("owner")
                    hit_object.update_health(-(self.damage_per_second * time_delta))
                    scored_hit = True
                # Find out how long the beam is, and scale the beam-model accordingly.
                beam_length = (hit_pos - self.character.actor.getPos()).length()
                self.model.setSy(beam_length)
                self.model.show()
                if scored_hit:
                    self.model_collision.show()
                    self.model_collision.setPos(hit_pos)
                    self.beam_hit_light_node_path.setPos(hit_pos + Vec3(0, 0, 0.5))
                    # If the light hasn't already been set here, set it
                    if not render.hasLight(self.beam_hit_light_node_path):
                        # Apply the light to the scene, so that it
                        # illuminates things
                        render.setLight(self.beam_hit_light_node_path)
                else:
                    # If the light has been set here, remove it
                    # See explanation in the tutorial-text below...
                    if render.hasLight(self.beam_hit_light_node_path):
                        # Clear the light from the scene, so that it
                        # no longer illuminates anything
                        render.clearLight(self.beam_hit_light_node_path)
                    self.model_collision.hide()

        else:
            if render.hasLight(self.beam_hit_light_node_path):
                # Clear the light from the scene, so that it
                # no longer illuminates anything
                render.clearLight(self.beam_hit_light_node_path)
            # If we're not shooting, don't show the beam-model.
            self.model.hide()
            self.model_collision.hide()

        if firing_vector.length() > 0.001:
            self.ray.setOrigin(origin)
            self.ray.setDirection(firing_vector)
        GameObject.update(self, time_delta)

    def remove_object_from_world(self):
        self.model_collision.removeNode()

        base.cTrav.removeCollider(self.ray_node_path)

        render.clearLight(self.beam_hit_light_node_path)
        self.beam_hit_light_node_path.removeNode()

        PhysicalObject.remove_object_from_world(self)


class MeleeAttack(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Melee Attack"
        self.description = "Swing your currently equipped weapon at an enemy.."

        self.damage = 1

        self.delay = 0.3  # The delay between the start of an attack, and the attack (potentially) landing
        self.delay_timer = 0  # Init the timer
        self.wait_timer = 0.2  # How long to wait between attacks

        self.physics_init()
        # self.display_init()

    def physics_init(self):
        """A mask that matches the player's, so that the enemy's attack will hit the player-character,
        but not the enemy-character (or other enemies)
        """
        self.attack_segment = CollisionSegment(0, 0, 0, 1, 0, 0)
        segment_node = CollisionNode("enemyAttackSegment")
        segment_node.addSolid(self.attack_segment)
        segment_node.setFromCollideMask(self.from_collider_attack)
        segment_node.setIntoCollideMask(self.into_collider)
        self.attack_segment_node_path = render.attachNewNode(segment_node)
        self.segment_queue = CollisionHandlerQueue()
        base.cTrav.addCollider(self.attack_segment_node_path, self.segment_queue)

    def update(self, time_delta, distance_to_player):
        if distance_to_player > self.character.proficiencies.attack_melee_distance.value:
            return
        if self.delay_timer > 0:
            self.delay_timer -= time_delta
            if self.delay_timer <= 0:
                # The animation has finished. See if the attack hit with a collision.
                print("The animation has finished! See if it landed.")
                if self.segment_queue.getNumEntries() > 0:
                    self.segment_queue.sortEntries()
                    segment_hit = self.segment_queue.getEntry(0)
                    hit_node_path = segment_hit.getIntoNodePath()
                    if hit_node_path.hasPythonTag("owner"):
                        # Apply damage!
                        hit_object = hit_node_path.getPythonTag("owner")
                        print(f"The attack has hit a {hit_object.__class__.__name__}!")
                        hit_object.update_health(-self.damage)
                        self.wait_timer = 1.0
        # If we're instead waiting to be allowed to attack...
        elif self.wait_timer > 0:
            self.wait_timer -= time_delta
            # If the wait has ended...
            if self.wait_timer <= 0:
                # Start an attack. The next frame should do the actual attack.
                # The attack lands when the delay_timer gets to 0.
                print("Monster is starting an attack")
                self.wait_timer = random.uniform(0.5, 0.7)
                self.delay_timer = self.delay
                self.character.actor.play("attack")

    def remove_object_from_world(self):
        base.cTrav.removeCollider(self.attack_segment_node_path)
        self.attack_segment_node_path.removeNode()

        GameObject.remove_object_from_world(self)


