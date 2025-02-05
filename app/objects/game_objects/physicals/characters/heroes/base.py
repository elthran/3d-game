from panda3d.core import Vec2, Vec3, Plane, Point3

from app.game.movement import Walk
from app.objects.skills import Abilities
from app.objects.game_objects.game_objects import GameObject
from app.game.tool_belt import NullCommand
from app.game.constants import CharacterTypes, Masks, Keys
from app.objects.game_objects.physicals.characters.characters import CharacterObject

import random


class Hero(CharacterObject):
    def __init__(self, *args, tool_belt=None, **kwargs):
        super().__init__(*args,
                         model_name="PandaChan/act_p3d_chan",
                         model_animation={"stand": "PandaChan/a_p3d_chan_idle",
                                          "walk": "PandaChan/a_p3d_chan_run"},
                         damage_taken_model="Misc/playerHit",
                         **kwargs)

        self.character_type = CharacterTypes.HERO
        # Set the collider for Hero's to be Hero.
        self.collider.node().setFromCollideMask(Masks.HERO_AND_MONSTER)
        self.collider.node().setIntoCollideMask(Masks.HERO)
        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)

        # Give them the ability package and the toolbelt
        self.abilities = Abilities(character=self, enemies=Masks.MONSTER, allies=Masks.HERO)
        self.tool_belt = tool_belt
        self.tool_belt.set_hero(self)

        # Set basic keys to the hero toolbelt
        walk = Walk(4)
        self.tool_belt.add_action(Keys.W, walk, walk.up)
        self.tool_belt.add_action(Keys.S, walk, walk.down)
        self.tool_belt.add_action(Keys.A, walk, walk.left)
        self.tool_belt.add_action(Keys.D, walk, walk.right)
        self.abilities.melee_attack.equip_to_tool_belt(Keys.MOUSE_LEFT)  # Hoping to deprecate this with line below....
        self.tool_belt.add_action(Keys.MOUSE_LEFT, self.abilities.melee_attack, None)
        self.tool_belt.add_action(Keys.MOUSE_RIGHT, NullCommand(), None)

        # Set basic hero statistics
        self.kills = 0
        self.level = 1
        self._experience = 0
        self.skill_points = 0
        self.attribute_points = 0
        self.archetype = None
        self.religion = None
        self.specialization = None

        # Set mouse coordinates in relation to hero
        self.firing_vector = None
        self.firing_vector_2d = None
        self.mouse_position = None
        self.mouse_position_3d = None
        self.last_mouse_pos = Vec2(0, 0)
        self.ground_plane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, new_value):
        if new_value >= self.experience_maximum:
            self._experience = new_value - self.experience_maximum
            self.level_up()
        else:
            self._experience = new_value

    @property
    def experience_maximum(self):
        return self.level * 1

    @property
    def identity(self):
        if self.specialization:
            return self.specialization
        elif self.archetype:
            return self.archetype
        else:
            return "Basic"

    def level_up(self):
        self.level += 1
        self.attribute_points += 1
        if self.level % 2 == 1:
            self.skill_points += 1

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

    def gain_attribute(self, attribute_name):
        self.attribute_points -= 1
        self.attributes.increase_attribute_by_name(attribute_name, 1)

    def learn_skill(self, skill_name):
        self.skill_points -= 1
        self.abilities.increase_skill_level_by_name(skill_name, 1)

