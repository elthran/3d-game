import random

from panda3d.core import Vec3, Vec2, Plane, Point3, TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from app.objects.abilities import Abilities
from app.objects.game_objects import GameObject
from .physicals import PhysicalObject
from .constants_physics import MASK_HERO, MASK_HERO_AND_MONSTER, MASK_MONSTER
from .characters import CharacterObject

import random


class Hero(CharacterObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the collider for Hero's to be Hero.
        self.collider.node().setIntoCollideMask(MASK_HERO)
        self.collider.node().setFromCollideMask(MASK_HERO_AND_MONSTER)

        self.abilities = Abilities(character=self, enemies=MASK_MONSTER, allies=MASK_HERO)

        # Since our "Game" object is the "ShowBase" object, we can access it via the global "base" variable.

        # Get mouse position
        self.last_mouse_pos = Vec2(0, 0)
        # Construct a plane facing upwards, and centred at (0, 0, 0) to triangulate mouse position
        self.ground_plane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))

        # Get's the Hero's current orientation for shooting projectiles (defines north????)
        self.y_vector = Vec2(0, 1)

        # Move to User class
        self.score = 0
        self.scoreUI = OnscreenText(text="0",
                                    pos=(-1.3, 0.825),
                                    mayChange=True,
                                    align=TextNode.ALeft)
        self.health_icons = []
        for i in range(self.proficiencies.health.value):
            icon = OnscreenImage(image="UI/health.png",
                                 pos=(-1.275 + i * 0.075, 0, 0.95),
                                 scale=0.04)
            # Since our icons have transparent regions, we'll activate transparency.
            icon.setTransparency(True)
            self.health_icons.append(icon)

    def update(self, time_delta, *args, keys=None, **kwargs):
        super().update(time_delta, *args, **kwargs)
        assert keys, 'Requires keys keyword.'

        self.walking = False
        if keys.up.on:
            self.walking = True
            self.velocity.addY(self.acceleration * time_delta)
        if keys.down.on:
            self.walking = True
            self.velocity.addY(-self.acceleration * time_delta)
        if keys.left.on:
            self.walking = True
            self.velocity.addX(-self.acceleration * time_delta)
        if keys.right.on:
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

        # Update the hero's knowledge of where the mouse is
        mouse_watcher = base.mouseWatcherNode
        if mouse_watcher.hasMouse():
            mouse_position = mouse_watcher.getMouse()
        else:
            mouse_position = self.last_mouse_pos
        mouse_position_3d = Point3()
        near_point = Point3()
        far_point = Point3()
        # Get the 3D line corresponding with the 2D mouse-position.
        # The "extrude" method will store its result in the "nearPoint" and "farPoint" objects.
        base.camLens.extrude(mouse_position, near_point, far_point)
        # Get the 3D point at which the 3D line intersects our ground-plane.
        # Similarly to the above, the "intersectsLine" method will store its result in the "mousePos3D" object.
        self.ground_plane.intersectsLine(mouse_position_3d,
                                         render.getRelativePoint(base.camera, near_point),
                                         render.getRelativePoint(base.camera, far_point))
        firing_vector = Vec3(mouse_position_3d - self.actor.getPos())
        firing_vector_2d = firing_vector.getXy()
        firing_vector_2d.normalize()
        firing_vector.normalize()
        heading = self.y_vector.signedAngleDeg(firing_vector_2d)
        self.actor.setH(heading)

        for ability in self.abilities.get_enabled():
            ability.update(time_delta,
                           active=keys.shoot.on,
                           firing_vector=firing_vector,
                           origin=self.actor.getPos())

        self.last_mouse_pos = mouse_position
        # Check if damage_taken_model can be refreshed
        if self.damage_taken_model and self.damage_taken_model_timer > 0:
            self.damage_taken_model_timer -= time_delta
            self.damage_taken_model.setScale(2.0 - self.damage_taken_model_timer / self.damage_taken_model_duration)
            if self.damage_taken_model_timer <= 0:
                self.damage_taken_model.hide()

    def update_health(self, health_delta):
        CharacterObject.update_health(self, health_delta)

        self.update_health_visual()

        self.damage_taken_model.show()
        self.damage_taken_model.setH(random.uniform(0.0, 360.0))
        self.damage_taken_model_timer = self.damage_taken_model_duration


    def update_health_visual(self):
        for index, icon in enumerate(self.health_icons):
            if index < self.proficiencies.health.current:
                icon.show()
            else:
                icon.hide()

    def update_score(self):
        self.scoreUI.setText(str(self.score))

    def remove_object_from_world(self):
        for ability in self.abilities:
            ability.remove_object_from_world()

        self.scoreUI.removeNode()
        for icon in self.health_icons:
            icon.removeNode()

        GameObject.remove_object_from_world(self)


class WizardHero(Hero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         model_name="Models/PandaChan/act_p3d_chan",
                         model_animation={"stand": "Models/PandaChan/a_p3d_chan_idle",
                                          "walk": "Models/PandaChan/a_p3d_chan_run"},
                         damage_taken_model="Models/Misc/playerHit",
                         **kwargs)
        self.attributes.agility.level = 3
        self.attributes.strength.level = 3
        self.attributes.vitality.level = 3
        self.refresh()
        self.abilities.frost_ray.enable()
        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)
