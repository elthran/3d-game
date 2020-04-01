from panda3d.core import CollisionRay, CollisionHandlerQueue, Vec3, Vec4, CollisionNode, \
    BitMask32, Vec2, Plane, Point3, PointLight, TextNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from app.Objects.monsters import SlidingCrateMonster
from app.Objects.characters import CharacterObject

from math import sin
from random import uniform


class Hero(CharacterObject):
    def __init__(self, pos, model_name, model_animation, health_max, speed_max):
        CharacterObject.__init__(self, pos, model_name, model_animation, health_max, speed_max)

        # Turn the model to face the other way.
        self.actor.getChild(0).setH(180)

        # Since our "Game" object is the "ShowBase" object, we can access it via the global "base" variable.
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        # ------------------------------------------- NEW CODE
        '''The shooting ray? '''
        self.ray = CollisionRay(0, 0, 0, 0, 1, 0)
        rayNode = CollisionNode("playerRay")
        rayNode.addSolid(self.ray)
        self.rayNodePath = render.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        '''We want this ray to collide with things, so tell our traverser about it. However, note that,
        unlike with "CollisionHandlerPusher", we don't have to tell our "CollisionHandlerQueue" about it.'''
        base.cTrav.addCollider(self.rayNodePath, self.rayQueue)
        self.laser_damage_per_second = 5.0

        # Get mouse position
        self.lastMousePos = Vec2(0, 0)
        # Construct a plane facing upwards, and centred at (0, 0, 0) to triangulate mouse position
        self.groundPlane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))

        self.yVector = Vec2(0, 1)

        '''bit masks?'''
        mask = BitMask32()
        mask.setBit(1)
        # This is the important one for preventing ray-collisions. The other is more a gameplay decision.
        self.collider.node().setIntoCollideMask(mask)
        mask = BitMask32()
        mask.setBit(1)
        self.collider.node().setFromCollideMask(mask)
        # After we've made our ray-node:
        mask = BitMask32()
        '''Note that we set a different bit here! This means that the ray's mask and the collider's mask don't match, 
        and so the ray won't collide with the collider.'''
        mask.setBit(2)
        rayNode.setFromCollideMask(mask)
        mask = BitMask32()
        rayNode.setIntoCollideMask(mask)
        '''end of bit masks?'''

        '''The laser model?'''
        # A nice laser-beam model to show our laser
        self.beamModel = loader.loadModel("Models/Misc/bambooLaser")
        self.beamModel.reparentTo(self.actor)
        self.beamModel.setZ(1.5)
        # This prevents lights from affecting this particular node
        self.beamModel.setLightOff()
        # We don't start out firing the laser, so
        # we have it initially hidden.
        self.beamModel.hide()
        '''end of laser model?'''
        # ------------------------------------------- END OF NEW CODE

        self.actor.loop("stand")

        # Move to User class
        self.score = 0
        self.scoreUI = OnscreenText(text="0",
                                    pos=(-1.3, 0.825),
                                    mayChange=True,
                                    align=TextNode.ALeft)
        self.health_icons = []
        for i in range(self.health_max):
            icon = OnscreenImage(image="UI/health.png",
                                 pos=(-1.275 + i * 0.075, 0, 0.95),
                                 scale=0.04)
            # Since our icons have transparent regions, we'll activate transparency.
            icon.setTransparency(True)
            self.health_icons.append(icon)
        # End of User class


        # Laser Stuff ---------------------------------------
        self.beamHitModel = loader.loadModel("Models/Misc/bambooLaserHit")
        self.beamHitModel.reparentTo(render)
        self.beamHitModel.setZ(1.5)
        self.beamHitModel.setLightOff()
        self.beamHitModel.hide()

        self.beamHitPulseRate = 0.15
        self.beamHitTimer = 0

        self.beamHitLight = PointLight("beamHitLight")
        self.beamHitLight.setColor(Vec4(0.1, 1.0, 0.2, 1))
        # These "attenuation" values govern how the light
        # fades with distance. They are, respectively,
        # the constant, linear, and quadratic coefficients
        # of the light's falloff equation.
        # I experimented until I found values that
        # looked nice.
        self.beamHitLight.setAttenuation((1.0, 0.1, 0.5))
        self.beamHitLightNodePath = render.attachNewNode(self.beamHitLight)
        # Note that we haven't yet applied the light to
        # a NodePath, and so it won't yet illuminate
        # anything.
        # --------------------------------------------------------------

        # Getting hit by monster ---
        self.damageTakenModel = loader.loadModel("Models/Misc/playerHit")
        self.damageTakenModel.setLightOff()
        self.damageTakenModel.setZ(1.0)
        self.damageTakenModel.reparentTo(self.actor)
        self.damageTakenModel.hide()
        self.damageTakenModelTimer = 0
        self.damageTakenModelDuration = 0.15
        # ----------------------

    def update(self, keys, time_delta):
        CharacterObject.update_position(self, time_delta)

        # ------------------------------------------- NEW CODE
        # Update the hero's knowledge of where the mouse is
        mouseWatcher = base.mouseWatcherNode
        mousePos = mouseWatcher.getMouse() if mouseWatcher.hasMouse() else self.lastMousePos
        mousePos3D = Point3()
        nearPoint = Point3()
        farPoint = Point3()
        # Get the 3D line corresponding with the 2D mouse-position.
        # The "extrude" method will store its result in the "nearPoint" and "farPoint" objects.
        base.camLens.extrude(mousePos, nearPoint, farPoint)
        # Get the 3D point at which the 3D line intersects our ground-plane.
        # Similarly to the above, the "intersectsLine" method will store its result in the "mousePos3D" object.
        self.groundPlane.intersectsLine(mousePos3D,
                                        render.getRelativePoint(base.camera, nearPoint),
                                        render.getRelativePoint(base.camera, farPoint))
        firingVector = Vec3(mousePos3D - self.actor.getPos())
        firingVector2D = firingVector.getXy()
        firingVector2D.normalize()
        firingVector.normalize()

        heading = self.yVector.signedAngleDeg(firingVector2D)

        self.actor.setH(heading)

        if firingVector.length() > 0.001:
            self.ray.setOrigin(self.actor.getPos())
            self.ray.setDirection(firingVector)

        self.lastMousePos = mousePos
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
        # ------------------------------------------- NEW CODE
        if keys.shoot.on:
            if self.rayQueue.getNumEntries() > 0:
                scored_hit = False
                self.rayQueue.sortEntries()
                ray_hit = self.rayQueue.getEntry(0)
                hit_pos = ray_hit.getSurfacePoint(render)
                hit_node_path = ray_hit.getIntoNodePath()
                print(hit_node_path)
                if hit_node_path.hasPythonTag("owner"):
                    hit_object = hit_node_path.getPythonTag("owner")
                    if not isinstance(hit_object, SlidingCrateMonster):
                        hit_object.update_health(-(self.laser_damage_per_second * time_delta))
                        scored_hit = True
                # Find out how long the beam is, and scale the beam-model accordingly.
                beam_length = (hit_pos - self.actor.getPos()).length()
                self.beamModel.setSy(beam_length)
                self.beamModel.show()
                if scored_hit:
                    self.beamHitModel.show()
                    self.beamHitModel.setPos(hit_pos)
                    self.beamHitLightNodePath.setPos(hit_pos + Vec3(0, 0, 0.5))
                    # If the light hasn't already been set here, set it
                    if not render.hasLight(self.beamHitLightNodePath):
                        # Apply the light to the scene, so that it
                        # illuminates things
                        render.setLight(self.beamHitLightNodePath)
                else:
                    # If the light has been set here, remove it
                    # See explanation in the tutorial-text below...
                    if render.hasLight(self.beamHitLightNodePath):
                        # Clear the light from the scene, so that it
                        # no longer illuminates anything
                        render.clearLight(self.beamHitLightNodePath)
                    self.beamHitModel.hide()
        else:
            if render.hasLight(self.beamHitLightNodePath):
                # Clear the light from the scene, so that it
                # no longer illuminates anything
                render.clearLight(self.beamHitLightNodePath)
            # If we're not shooting, don't show the beam-model.
            self.beamModel.hide()
            self.beamHitModel.hide()
        # ------------------------------------------- END OF NEW CODE

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

        # In short, run a timer, and use the timer in a sine-function
        # to pulse the scale of the beam-hit model. When the timer
        # runs down (and the scale is at its lowest), reset the timer
        # and randomise the beam-hit model's rotation.
        self.beamHitTimer -= time_delta
        if self.beamHitTimer <= 0:
            self.beamHitTimer = self.beamHitPulseRate
            self.beamHitModel.setH(uniform(0.0, 360.0))
        self.beamHitModel.setScale(sin(self.beamHitTimer * 3.142 / self.beamHitPulseRate) * 0.4 + 0.9)

        # Damage taken
        if self.damageTakenModelTimer > 0:
            self.damageTakenModelTimer -= time_delta
            self.damageTakenModel.setScale(2.0 - self.damageTakenModelTimer / self.damageTakenModelDuration)
            if self.damageTakenModelTimer <= 0:
                self.damageTakenModel.hide()

    def update_health(self, health_delta):
        self.damageTakenModel.show()
        self.damageTakenModel.setH(uniform(0.0, 360.0))
        self.damageTakenModelTimer = self.damageTakenModelDuration

        self.health += health_delta

        if self.health > self.health_max:
            self.health = self.health_max

        print(f"Hero health: {self.health}/{self.health_max}")

        self.update_health_UI()

    def update_health_UI(self):
        for index, icon in enumerate(self.health_icons):
            if index < self.health:
                icon.show()
            else:
                icon.hide()

    def update_score(self):
        self.scoreUI.setText(str(self.score))

    def cleanup(self):
        base.cTrav.removeCollider(self.rayNodePath)
        GameObject.cleanup(self)
        self.beamHitModel.removeNode()
        render.clearLight(self.beamHitLightNodePath)
        self.beamHitLightNodePath.removeNode()
        self.scoreUI.removeNode()
        for icon in self.health_icons:
            icon.removeNode()


class CurrentHero(Hero):
    def __init__(self):
        Hero.__init__(self,
                      pos=Vec3(0, 0, 0),
                      model_name="Models/PandaChan/act_p3d_chan",
                      model_animation={"stand": "Models/PandaChan/a_p3d_chan_idle",
                                       "walk": "Models/PandaChan/a_p3d_chan_run"},
                      health_max=5,
                      speed_max=10)


class TestModelHero(Hero):
    def __init__(self):
        Hero.__init__(self,
                      pos=Vec3(-1, 0, 0),
                      model_name="Models/TestHero/drui-dude",
                      model_animation={},
                      health_max=5,
                      speed_max=10)
