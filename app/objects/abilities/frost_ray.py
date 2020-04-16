from panda3d.core import CollisionRay, Vec3, PointLight, Vec4, AudioSound

from math import sin
from random import uniform
from app.objects.abilities import Ability
from app.objects.damage import Damage
from app.objects.interfaces import Command


class FrostRay(Ability, Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Frost Ray"
        self.description = "Shoot a ray of frost at an enemy."
        self.collision_node = CollisionRay(0, 0, 0, 0, 1, 0)
        # Sound files
        self.sound_miss_file_path = "resources/sounds/laserNoHit.ogg"
        self.sound_hit_file_path = "resources/sounds/laserHit.ogg"
        self.sound_damage_file_path = "resources/sounds/FemaleDmgNoise.ogg"

    def display_init(self):
        '''The laser model: A nice laser-beam model to show our laser'''
        self.model = loader.loadModel("resources/models/Misc/bambooLaser")
        self.model.reparentTo(self.character.actor)
        self.model.setZ(1.5)
        # This prevents lights from affecting this particular node
        self.model.setLightOff()
        # We don't start out firing the laser, so we have it initially hidden.
        self.model.hide()

        '''The laser's hit animation'''
        self.model_collision = loader.loadModel("resources/models/Misc/bambooLaserHit")
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

    def get_damage(self, time_delta=None):
        base_damage = 5
        bonus_damage = self.character.attributes.intellect.level
        total_damage = (base_damage + bonus_damage) * time_delta
        return Damage(source=self.character, frost=total_damage)

    def update(self, operation, key, hero, time_delta):
        active = key.on if (self.character.proficiencies.mana.current > 0) else 0
        self.update_direct(active, hero, time_delta)

    def update_direct(self, active, hero, time_delta):
        super().update(time_delta)

        origin = hero.actor.getPos()
        # In short, run a timer, and use the timer in a sine-function
        # to pulse the scale of the beam-hit model. When the timer
        # runs down (and the scale is at its lowest), reset the timer
        # and randomise the beam-hit model's rotation.
        self.beam_hit_timer -= time_delta
        if self.beam_hit_timer <= 0:
            self.beam_hit_timer = self.beam_hit_pulse_rate
            self.model_collision.setH(uniform(0.0, 360.0))
        self.model_collision.setScale(sin(self.beam_hit_timer * 3.142 / self.beam_hit_pulse_rate) * 0.4 + 0.9)

        if active:
            self.character.proficiencies.mana.current -= 0.05
            if self.collision_node_queue.getNumEntries() > 0:
                scored_hit = False
                self.collision_node_queue.sortEntries()
                ray_hit = self.collision_node_queue.getEntry(0)
                hit_pos = ray_hit.getSurfacePoint(render)
                hit_node_path = ray_hit.getIntoNodePath()  # Into node model name?
                if hit_node_path.hasPythonTag("owner"):
                    hit_object = hit_node_path.getPythonTag("owner")
                    hit_object.take_damage(damage=self.get_damage(time_delta))
                    scored_hit = True
                # Find out how long the beam is, and scale the beam-model accordingly.
                beam_length = (hit_pos - self.character.actor.getPos()).length()
                self.model.setSy(beam_length)
                self.model.show()
                if scored_hit:
                    if self.sound_miss.status() == AudioSound.PLAYING:
                        self.sound_miss.stop()
                    if self.sound_hit.status() != AudioSound.PLAYING:
                        self.sound_hit.play()

                    self.model_collision.show()
                    self.model_collision.setPos(hit_pos)
                    self.beam_hit_light_node_path.setPos(hit_pos + Vec3(0, 0, 0.5))
                    # If the light hasn't already been set here, set it
                    if not render.hasLight(self.beam_hit_light_node_path):
                        # Apply the light to the scene, so that it
                        # illuminates things
                        render.setLight(self.beam_hit_light_node_path)
                else:
                    if self.sound_hit.status() == AudioSound.PLAYING:
                        self.sound_hit.stop()
                    if self.sound_miss.status() != AudioSound.PLAYING:
                        self.sound_miss.play()
                    # If the light has been set here, remove it
                    # See explanation in the tutorial-text below...
                    if render.hasLight(self.beam_hit_light_node_path):
                        # Clear the light from the scene, so that it
                        # no longer illuminates anything
                        render.clearLight(self.beam_hit_light_node_path)
                    self.model_collision.hide()

        else:
            if self.sound_hit.status() == AudioSound.PLAYING:
                self.sound_hit.stop()
            if self.sound_miss.status() == AudioSound.PLAYING:
                self.sound_miss.stop()
            if render.hasLight(self.beam_hit_light_node_path):
                # Clear the light from the scene, so that it
                # no longer illuminates anything
                render.clearLight(self.beam_hit_light_node_path)
            # If we're not shooting, don't show the beam-model.
            self.model.hide()
            self.model_collision.hide()

        if self.character.firing_vector.length() > 0.001:
            self.collision_node.setOrigin(origin)
            self.collision_node.setDirection(self.character.firing_vector)