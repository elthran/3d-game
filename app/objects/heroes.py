from panda3d.core import Vec3, Vec2, Plane, Point3, TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from .physicals import PhysicalObject
from .constants_physics import MASK_HERO
from .characters import CharacterObject


class Hero(CharacterObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the collider for Hero's to be Hero.
        self.collider.node().setIntoCollideMask(MASK_HERO)
        self.collider.node().setFromCollideMask(MASK_HERO)

        # Since our "Game" object is the "ShowBase" object, we can access it via the global "base" variable.
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

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

    def update(self, time_delta, keys=None):
        CharacterObject.update(self, time_delta)

        # Update the hero's knowledge of where the mouse is
        mouse_watcher = base.mouseWatcherNode
        mouse_position = mouse_watcher.getMouse() if mouse_watcher.hasMouse() else self.last_mouse_pos
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
        self.last_mouse_pos = mouse_position

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
        for ability in self.abilities:
            ability.update(time_delta=time_delta, active=keys.shoot.on, firing_vector=firing_vector, origin=self.actor.getPos())

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

        PhysicalObject.remove_object_from_world(self)


class WizardHero(Hero):
    def __init__(self, starting_position=None, model_name=None, model_animation=None, damage_taken_model=None):
        super().__init__(starting_position=Vec3(0, 0, 0), model_name="Models/PandaChan/act_p3d_chan",
                         model_animation={"stand": "Models/PandaChan/a_p3d_chan_idle",
                                          "walk": "Models/PandaChan/a_p3d_chan_run"},
                         damage_taken_model="Models/Misc/playerHit")
        self.attributes.agility.level = 3
        self.attributes.strength.level = 3
        self.attributes.vitality.level = 3
        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)
