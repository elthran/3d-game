from direct.showbase.ShowBase import ShowBase

from panda3d.core import CollisionCapsule

from app import *

MAX_FRAME_RATE = 1 / 60


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # globalClock.setMode(ClockObject.MLimited)
        # globalClock.setFrameRate(60)

        '''
        Environment stuff
        '''
        self.disableMouse()
        # properties = WindowProperties()
        # properties.setSize(1000, 750)
        # self.win.requestProperties(properties)
        main_light = DirectionalLight("main light")
        self.main_light_node_path = render.attachNewNode(main_light)
        self.main_light_node_path.setHpr(45, -45, 0)
        render.setLight(self.main_light_node_path)

        ambient_light = AmbientLight("ambient light")
        ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambient_light_node_path = render.attachNewNode(ambient_light)
        render.setLight(self.ambient_light_node_path)

        render.setShaderAuto()

        self.environment = loader.loadModel("Models/Misc/environment")
        self.environment.reparentTo(render)

        self.camera.setPos(0, 0, 32)
        self.camera.setP(-90)

        self.key_mapper = KeyMapper.initialize(self)

        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()
        self.cTrav.setRespectPrevTransform(True)

        self.pusher.setHorizontal(True)

        '''
        Collision detection stuff
        '''
        self.pusher.add_in_pattern("%fn-into-%in")
        self.accept("SlidingCrateMonster-into-Wall", self.stop_sliding_crate_monster)
        self.accept("SlidingCrateMonster-into-TrainingDummyMonster", self.sliding_crate_monster_hits_unit)
        self.accept("SlidingCrateMonster-into-Hero", self.sliding_crate_monster_hits_unit)

        '''
        CollisionEntry:
          from render/character/WizardHero
          into render/Wall []
          at -5.39875 8.2 0
          normal 0 1 0
          interior -5.39875 8.2 0 (depth 0)
          respect_prev_transform = 1
  '''

        self.accept("WizardHero-into-Wall", print)
        self.accept("TrainingDummyMonster-into-Wall", print)

        wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        # wallSolid = CollisionPlane(Plane(Vec3(8.0, 0, 0), Point3(-8.0, 0, 0)))
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setY(8.0)

        wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(-8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(-8.0)

        self.updateTask = taskMgr.add(self.update, "update")

        '''Game related stuff
        '''# Start off with no player; the
        # player-character will be created
        # in the "startGame" method, below.
        # Note that this replaces the
        # "self.player = Player()" line
        # that was here
        self.hero = None
        # Our enemies, traps, and "dead enemies"
        self.enemies = []
        self.trapEnemies = []
        self.deadEnemies = []

        # Set up some monster spawn points
        self.spawnPoints = []
        numPointsPerWall = 5
        for i in range(numPointsPerWall):
            coord = 7.0 / numPointsPerWall + 0.5
            self.spawnPoints.append(Vec3(-7.0, coord, 0))
            self.spawnPoints.append(Vec3(7.0, coord, 0))
            self.spawnPoints.append(Vec3(coord, -7.0, 0))
            self.spawnPoints.append(Vec3(coord, 7.0, 0))

        # Values to control when to spawn enemies, and
        # how many enemies there may be at once
        self.initialSpawnInterval = 1.0
        self.minimumSpawnInterval = 0.2
        self.spawnInterval = self.initialSpawnInterval
        self.spawnTimer = self.spawnInterval
        self.maxEnemies = 2
        self.maximumMaxEnemies = 20

        self.numTrapsPerSide = 2

        self.difficultyInterval = 5.0
        self.difficultyTimer = self.difficultyInterval

        # Start the game!
        self.start_game()

    def start_game(self):
        # We'll add this method presently.
        # In short, clean up anything in the
        # level--enemies, traps, etc.--before
        # starting a new one.
        # self.cleanup()

        self.hero = WizardHero(starting_position=Vec3(0, 0, 0))
        self.maxEnemies = 2
        self.spawnInterval = self.initialSpawnInterval
        self.display_damage = OnscreenText(text=f'Damage taken: {5 - self.hero.proficiencies.health.maximum}',
                                           pos=(1, -0.9), scale=0.07)
        self.training_dummy_monster = TrainingDummyMonster(starting_position=Vec3(5, 0, 0))
        # self.crate_interactive = CrateInteractive(starting_position=Vec3(-2, 3, 0))
        self.sliding_crate_monster = SlidingCrateMonster(starting_position=Vec3(2, 7, 0))

    def update(self, task):
        # Get the amount of time since the last update
        time_delta = min(globalClock.getDt(), MAX_FRAME_RATE)

        self.hero.update(time_delta, keys=self.key_mapper)

        self.training_dummy_monster.update(time_delta, hero=self.hero)
        self.sliding_crate_monster.update(time_delta, hero=self.hero)

        return task.cont

    @staticmethod
    def stop_sliding_crate_monster(entry):
        collider = entry.getFromNodePath()
        if collider.hasPythonTag("owner"):
            trap = collider.getPythonTag("owner")
            trap.moveDirection = 0
            trap.ignorePlayer = False

    def sliding_crate_monster_hits_unit(self, entry):
        collider = entry.getFromNodePath()
        if collider.hasPythonTag("owner"):
            trap = collider.getPythonTag("owner")
            # We don't want stationary traps to do damage, so ignore the collision if the "moveDirection" is 0
            if trap.moveDirection == 0:
                return

            collider = entry.getIntoNodePath()
            if collider.hasPythonTag("owner"):
                obj = collider.getPythonTag("owner")
                if isinstance(obj, Hero):
                    # If it hits a hero for the first time, do 1 damage and set the flag to have hit hero.
                    if not trap.ignorePlayer:
                        obj.update_health(-1)
                        self.display_damage.destroy()
                        self.display_damage = OnscreenText(text=f'Damage taken: {5 - obj.health}',
                                                           pos=(1, -0.9),
                                                           scale=0.07)
                        # self.display_damage.setText = f'Damage taken: {5 - obj.health}'
                        trap.ignorePlayer = True
                # If it hits a non-hero unit, take away 10 health.
                else:
                    obj.update_health(-10)


if __name__ in ['__main__', 'main']:
    game = Game()
    game.run()
