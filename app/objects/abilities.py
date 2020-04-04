from panda3d.core import CollisionHandlerQueue, CollisionNode, CollisionRay, Vec3, PointLight, Vec4

from .constants_physics import MASK_MONSTER, MASK_NOTHING
from .physicals import PhysicalObject

from math import sin
from random import uniform


class Abilities:
    def __init__(self, character):
        self.character = character
        self.frost_ray = FrostRay(character)

    def __iter__(self):
        return iter([self.frost_ray])


class Ability:
    def __init__(self, character):
        self.character = character
        self.model = None  # The basic model of the animation
        self.model_collision = None  # The model when the animation collides with another object
        self.damage_per_second = None

    def update(self, time_delta, active, firingVector, origin):
        pass

    def remove_object_from_world(self):
        pass


class FrostRay(Ability):
    def __init__(self, character):
        super().__init__(character)
        self.name = "Frost Ray"
        self.description = "Shoot a ray of frost at an enemy."
        self.damage_per_second = 5.0

        self.physics_init()
        self.display_init()

    def physics_init(self):
        self.ray = CollisionRay(0, 0, 0, 0, 1, 0)
        ray_node = CollisionNode(self.__class__.__name__)
        # After we've made our ray-node:
        ray_node.setFromCollideMask(MASK_MONSTER)
        ray_node.setIntoCollideMask(MASK_NOTHING)
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

    def update(self, time_delta, active, firing_vector, origin):
        # In short, run a timer, and use the timer in a sine-function
        # to pulse the scale of the beam-hit model. When the timer
        # runs down (and the scale is at its lowest), reset the timer
        # and randomise the beam-hit model's rotation.
        self.beam_hit_timer -= time_delta
        if self.beam_hit_timer <= 0:
            self.beam_hit_timer = self.beam_hit_pulse_rate
            self.model_collision.setH(uniform(0.0, 360.0))
        self.model_collision.setScale(sin(self.beam_hit_timer * 3.142 / self.beam_hit_pulse_rate) * 0.4 + 0.9)

        if not active:
            if render.hasLight(self.beam_hit_light_node_path):
                # Clear the light from the scene, so that it
                # no longer illuminates anything
                render.clearLight(self.beam_hit_light_node_path)
            # If we're not shooting, don't show the beam-model.
            self.model.hide()
            self.model_collision.hide()
            return

        if self.ray_queue.getNumEntries() > 0:
            scored_hit = False
            self.ray_queue.sortEntries()
            ray_hit = self.ray_queue.getEntry(0)
            hit_pos = ray_hit.getSurfacePoint(render)
            hit_node_path = ray_hit.getIntoNodePath()
            print(hit_node_path)
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

        if firing_vector.length() > 0.001:
            self.ray.setOrigin(origin)
            self.ray.setDirection(firing_vector)

    def remove_object_from_world(self):
        self.model_collision.removeNode()

        base.cTrav.removeCollider(self.ray_node_path)

        render.clearLight(self.beam_hit_light_node_path)
        self.beam_hit_light_node_path.removeNode()

        PhysicalObject.remove_object_from_world(self)
