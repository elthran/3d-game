from panda3d.core import Vec2, Vec3, Plane, Point3, TextNode
from direct.gui.OnscreenText import OnscreenText

from app.objects.movement import Walk
from app.objects.abilities import Abilities
from app.objects.game_objects import GameObject
from app.objects.tool_belt import ToolBelt, NullCommand
from .constants import CharacterTypes, Masks, Keys
from app.objects.characters import CharacterObject

import random


class Hero(CharacterObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character_type = CharacterTypes.HERO
        # Set the collider for Hero's to be Hero.
        self.collider.node().setFromCollideMask(Masks.HERO_AND_MONSTER)
        self.collider.node().setIntoCollideMask(Masks.HERO)

        self.abilities = Abilities(character=self, enemies=Masks.MONSTER, allies=Masks.HERO)
        self.tool_belt = ToolBelt()

        self.kills = 0
        self._level = 1
        self._experience = 0

        walk = Walk(4)
        self.tool_belt.add_action(Keys.W, walk, walk.up)
        self.tool_belt.add_action(Keys.S, walk, walk.down)
        self.tool_belt.add_action(Keys.A, walk, walk.left)
        self.tool_belt.add_action(Keys.D, walk, walk.right)
        self.tool_belt.add_action(Keys.MOUSE_LEFT, NullCommand(), None)
        self.tool_belt.add_action(Keys.MOUSE_RIGHT, NullCommand(), None)

        self.firing_vector = None
        self.firing_vector_2d = None

        self.mouse_position = None
        self.mouse_position_3d = None
        self.last_mouse_pos = Vec2(0, 0)
        self.ground_plane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))

        # Move to User class
        self.scoreUI = OnscreenText(text="0",
                                    pos=(-1.3, 0.825),
                                    mayChange=True,
                                    align=TextNode.ALeft)

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, new_value):
        while new_value >= 2:
            self.level += 1
            new_value -= 2
        self._experience = new_value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_value):
        self.attributes.vitality.level += (new_value - self.level)
        self.attributes.intellect.level += (new_value - self.level)
        self._level = new_value

    def update(self, time_delta, *args, keys=None, **kwargs):
        super().update(time_delta, *args, **kwargs)
        assert keys, 'Requires keys keyword.'

        # This can be improved. If the character is walking go through the two possibilites (was standing/ was walking)
        # Else set them to loop stand.
        # Should just be.... self.update_current_animation()
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

        self.update_ground_plane_and_mouse_position()

        self.update_firing_vector_and_heading()

        self.tool_belt.execute(keys, self, time_delta)

        # Check if damage_taken_model can be refreshed
        if self.damage_taken_model and self.damage_taken_model_timer > 0:
            self.damage_taken_model_timer -= time_delta
            self.damage_taken_model.setScale(2.0 - self.damage_taken_model_timer / self.damage_taken_model_duration)
            if self.damage_taken_model_timer <= 0:
                self.damage_taken_model.hide()

    def update_ground_plane_and_mouse_position(self):
        """Updates the hero's knowledge of where the ground-plane intersects with the mouse.
        """
        mouse_watcher = base.mouseWatcherNode
        if mouse_watcher.hasMouse():
            self.mouse_position = mouse_watcher.getMouse()
        else:
            self.mouse_position = self.last_mouse_pos
        self.mouse_position_3d = Point3()
        near_point = Point3()
        far_point = Point3()
        # The "extrude" method will store its result in the "nearPoint" and "farPoint" objects.
        base.camLens.extrude(self.mouse_position, near_point, far_point)
        # Similarly to the above, the "intersectsLine" method will store its result in the "mousePos3D" object.
        self.ground_plane.intersectsLine(self.mouse_position_3d,
                                         render.getRelativePoint(base.camera, near_point),
                                         render.getRelativePoint(base.camera, far_point))
        # We create a fall back, in case the next position is unobtainable
        self.last_mouse_pos = self.mouse_position

    def update_firing_vector_and_heading(self):
        """Creates a firing_vector which is the vector from the Hero to the mouse,
        and updates the Hero's heading to face it.
        """
        self.firing_vector = Vec3(self.mouse_position_3d - self.actor.getPos())
        self.firing_vector_2d = self.firing_vector.getXy()
        self.firing_vector_2d.normalize()
        self.firing_vector.normalize()
        new_heading = self.y_vector.signedAngleDeg(self.firing_vector_2d)
        self.actor.setH(new_heading)

    def update_health(self, health_delta, source=None):
        CharacterObject.update_health(self, health_delta, source=source)

        self.update_health_visual()

        self.damage_taken_model.show()
        self.damage_taken_model.setH(random.uniform(0.0, 360.0))
        self.damage_taken_model_timer = self.damage_taken_model_duration

    def update_health_visual(self):
        pass

    def remove_object_from_world(self):
        for ability in self.abilities:
            ability.remove_object_from_world()

        GameObject.remove_object_from_world(self)


class WarriorHero(Hero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         model_name="resources/models/PandaChan/act_p3d_chan",
                         model_animation={"stand": "resources/models/PandaChan/a_p3d_chan_idle",
                                          "walk": "resources/models/PandaChan/a_p3d_chan_run"},
                         damage_taken_model="resources/models/Misc/playerHit",
                         **kwargs)
        self.attributes.agility.level = 2
        self.attributes.intellect.level = 0
        self.attributes.strength.level = 5
        self.attributes.vitality.level = 3
        self.refresh()
        self.abilities.melee_attack.enable()
        self.tool_belt.add_action(Keys.MOUSE_LEFT, self.abilities.melee_attack, None)
        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)


class WizardHero(Hero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         model_name="resources/models/PandaChan/act_p3d_chan",
                         model_animation={"stand": "resources/models/PandaChan/a_p3d_chan_idle",
                                          "walk": "resources/models/PandaChan/a_p3d_chan_run"},
                         damage_taken_model="resources/models/Misc/playerHit",
                         **kwargs)
        self.attributes.agility.level = 2
        self.attributes.intellect.level = 6
        self.attributes.strength.level = 1
        self.attributes.vitality.level = 2
        self.refresh()
        self.abilities.frost_ray.enable()
        self.abilities.melee_attack.enable()
        self.tool_belt.add_action(Keys.MOUSE_LEFT, self.abilities.melee_attack, None)
        self.tool_belt.add_action(Keys.MOUSE_RIGHT, self.abilities.frost_ray, None)
        self.tool_belt.add_action(Keys.F, self.abilities.mana_armour, None)
        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)
