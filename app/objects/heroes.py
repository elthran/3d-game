from app.config.initializers.panda3d import *

from app.objects.monsters import SlidingCrateMonster
from app.objects.templates import GameObject


class Hero(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                            pos=Vec3(0, 0, 0),
                            model_name="Models/PandaChan/act_p3d_chan",
                            model_animation={"stand": "Models/PandaChan/a_p3d_chan_idle",
                                             "walk": "Models/PandaChan/a_p3d_chan_run"},
                            health_max=5,
                            speed_max=10)

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
        self.damagePerSecond = -5.0

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

    def update(self, keys, time_delta):
        GameObject.update_position(self, time_delta)

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
                self.rayQueue.sortEntries()
                rayHit = self.rayQueue.getEntry(0)
                hitPos = rayHit.getSurfacePoint(render)
                hitNodePath = rayHit.getIntoNodePath()
                print(hitNodePath)
                if hitNodePath.hasPythonTag("owner"):
                    hitObject = hitNodePath.getPythonTag("owner")
                    if not isinstance(hitObject, SlidingCrateMonster):
                        hitObject.update_health(self.damagePerSecond * time_delta)
                # Find out how long the beam is, and scale the beam-model accordingly.
                beamLength = (hitPos - self.actor.getPos()).length()
                self.beamModel.setSy(beamLength)
                self.beamModel.show()
        else:
            # If we're not shooting, don't show the beam-model.
            self.beamModel.hide()
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

    def cleanup(self):
        base.cTrav.removeCollider(self.rayNodePath)
        GameObject.cleanup(self)
