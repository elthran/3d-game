from panda3d.core import CollisionRay, CollisionHandlerQueue, Vec3, Vec4, CollisionNode, \
    Vec2, Plane, Point3, PointLight, TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from .physicals import PhysicalObject
from .constants_physics import MASK_NOTHING, MASK_HERO, MASK_MONSTER, MASK_HERO_AND_MONSTER
from .monsters import SlidingCrateMonster
from .characters import CharacterObject

from math import sin
from random import uniform


class Hero(CharacterObject):
    def __init__(self, starting_position=None, model_name=None, model_animation=None):
        super().__init__(starting_position, model_name, model_animation)
        # Set the collider for Hero's to be Hero.
        self.collider.node().setIntoCollideMask(MASK_HERO)
        self.collider.node().setFromCollideMask(MASK_HERO)

        # Since our "Game" object is the "ShowBase" object, we can access it via the global "base" variable.
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.actor.loop("stand")

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
        # End of User class

        # Getting hit by monster ---
        self.damageTakenModel = loader.loadModel("Models/Misc/playerHit")
        self.damageTakenModel.setLightOff()
        self.damageTakenModel.setZ(1.0)
        self.damageTakenModel.reparentTo(self.actor)
        self.damageTakenModel.hide()
        self.damageTakenModelTimer = 0
        self.damageTakenModelDuration = 0.15
        # ----------------------

    def update(self, time_delta, keys=None):
        CharacterObject.update(self, time_delta)

        # ------------------------------------------- NEW CODE
        # Update the hero's knowledge of where the mouse is
        mouseWatcher = base.mouseWatcherNode
        mousePos = mouseWatcher.getMouse() if mouseWatcher.hasMouse() else self.last_mouse_pos
        mousePos3D = Point3()
        nearPoint = Point3()
        farPoint = Point3()
        # Get the 3D line corresponding with the 2D mouse-position.
        # The "extrude" method will store its result in the "nearPoint" and "farPoint" objects.
        base.camLens.extrude(mousePos, nearPoint, farPoint)
        # Get the 3D point at which the 3D line intersects our ground-plane.
        # Similarly to the above, the "intersectsLine" method will store its result in the "mousePos3D" object.
        self.ground_plane.intersectsLine(mousePos3D,
                                         render.getRelativePoint(base.camera, nearPoint),
                                         render.getRelativePoint(base.camera, farPoint))

        firingVector = Vec3(mousePos3D - self.actor.getPos())
        firingVector2D = firingVector.getXy()
        firingVector2D.normalize()
        firingVector.normalize()

        heading = self.y_vector.signedAngleDeg(firingVector2D)

        self.actor.setH(heading)

        self.last_mouse_pos = mousePos
        # ------------------------------------------- END OF NEW CODE

        self.walking = False

        # If we're  pushing a movement key, add a relevant amount to our velocity.
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
            ability.update(time_delta=time_delta, active=keys.shoot.on, firingVector=firingVector, origin=self.actor.getPos())

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

        # Damage taken
        if self.damageTakenModelTimer > 0:
            self.damageTakenModelTimer -= time_delta
            self.damageTakenModel.setScale(2.0 - self.damageTakenModelTimer / self.damageTakenModelDuration)
            if self.damageTakenModelTimer <= 0:
                self.damageTakenModel.hide()

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

        self.beamHitModel.removeNode()
        render.clearLight(self.beamHitLightNodePath)
        self.beamHitLightNodePath.removeNode()
        self.scoreUI.removeNode()
        for icon in self.health_icons:
            icon.removeNode()

        PhysicalObject.remove_object_from_world(self)


class WizardHero(Hero):
    def __init__(self, starting_position=None, model_name=None, model_animation=None):
        super().__init__(starting_position=Vec3(0, 0, 0), model_name="Models/PandaChan/act_p3d_chan",
                         model_animation={"stand": "Models/PandaChan/a_p3d_chan_idle",
                                          "walk": "Models/PandaChan/a_p3d_chan_run"})
        self.attributes.agility.level = 3
        self.attributes.strength.level = 3
        self.attributes.vitality.level = 3
        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)
