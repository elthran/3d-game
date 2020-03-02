import random
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

from direct.gui.OnscreenText import OnscreenText

from objects.hero import Hero


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.coins = 0
        self.textObject = OnscreenText(text=f'Coins collected: {self.coins}',
                                       pos=(0.9, -0.9), scale=0.1, fg=(1, 1, 1, 1),
                                       mayChange=True)

        '''Disable the camera trackball controls.'''
        self.disableMouse()

        '''Load the environment model.'''
        self.scene = self.loader.loadModel("models/environment")
        '''Reparent the model to render.'''
        self.scene.reparentTo(self.render)
        '''Apply scale and position transforms on the model.'''
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        '''Add the spinCameraTask procedure to the task manager.'''
        self.taskMgr.add(self.spin_camera_task, "SpinCameraTask")

        '''Load and transform the panda actor.'''
        self.pandaActor = Actor("models/jacob-panda-model",
                                {"walk": "models/jacob-panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        '''Loop its animation.'''
        self.pandaActor.loop("walk")

        # self.pandaHero = Hero(models="models/jacob-panda-model")

        '''Create the four lerp intervals needed for the panda to walk back and forth.'''
        pos_interval_1 = self.pandaActor.posInterval(13,
                                                     Point3(0, -10, 0),
                                                     startPos=Point3(0, 10, 0))
        pos_interval_2 = self.pandaActor.posInterval(13,
                                                     Point3(0, 10, 0),
                                                     startPos=Point3(0, -10, 0))
        hpr_interval_1 = self.pandaActor.hprInterval(3,
                                                     Point3(180, 0, 0),
                                                     startHpr=Point3(0, 0, 0))
        hpr_interval_2 = self.pandaActor.hprInterval(3,
                                                     Point3(0, 0, 0),
                                                     startHpr=Point3(180, 0, 0))

        '''Create and play the sequence that coordinates the intervals.'''
        self.pandaPace = Sequence(pos_interval_1, hpr_interval_1,
                                  pos_interval_2, hpr_interval_2,
                                  name="pandaPace")
        self.pandaPace.loop()

    def update_ticker(self):
        """Add a coin to the total and update the ticker."""
        self.coins += 1
        self.textObject.setText(text=f'Coins collected: {self.coins}')
        return Task.cont

    def spin_camera_task(self, task):
        """Define a procedure to move the camera."""
        angle_degrees = task.time * 6.0
        angle_radians = angle_degrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angle_radians), -20 * cos(angle_radians), 3)
        self.camera.setHpr(angle_degrees, 0, 0)
        if random.randint(1, 100) >= 100:
            self.update_ticker()
        return Task.cont


if __name__ in ['__main__', 'main']:
    app = MyApp()
    app.run()
