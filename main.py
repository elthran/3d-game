from direct.gui.DirectGui import DGG, DirectDialog, DirectFrame, DirectButton, DirectLabel
from direct.showbase.ShowBase import ShowBase

from panda3d.core import CollisionCapsule

from app import *
from app.objects.display_bars import Hud

MAX_FRAME_RATE = 1 / 60


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.default_font = loader.loadFont("Fonts/Wbxkomik.ttf")

        background_music = loader.loadMusic("Music/background_theme.mp3")
        background_music.setLoop(True)
        # I find this piece to be pretty loud, so I've turned the volume down a lot.
        background_music.setVolume(0.5)
        background_music.play()

        self.disableMouse()

        main_light = DirectionalLight("main light")
        self.main_light_node_path = render.attachNewNode(main_light)
        self.main_light_node_path.setHpr(45, -45, 0)
        render.setLight(self.main_light_node_path)

        ambient_light = AmbientLight("ambient light")
        ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambient_light_node_path = render.attachNewNode(ambient_light)
        render.setLight(self.ambient_light_node_path)

        render.setShaderAuto()

        # self.environment = loader.loadModel("Models/Misc/environment")
        # self.environment.reparentTo(render)

        self.camera.setPos(0, -20, 32)
        self.camera.setP(-60)

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
        wall.show()
        wall.setY(-8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setX(8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setX(-8.0)

        self.updateTask = taskMgr.add(self.update, "update")

        self.hero = None
        self.hud = None
        self.walking_enemies = []
        self.sliding_enemies = []
        self.deadEnemies = []

        # Set up some monster spawn points
        self.spawn_time = 5
        self.spawn_timer = 5
        self.maximum_walking_enemies = 2
        self.spawn_points = []
        number_points_per_wall = 5
        for i in range(number_points_per_wall):
            coord = 7.0 / number_points_per_wall + 0.5
            self.spawn_points.append(Vec3(-7.0, coord, 0))
            self.spawn_points.append(Vec3(7.0, coord, 0))
            self.spawn_points.append(Vec3(coord, -7.0, 0))
            self.spawn_points.append(Vec3(coord, 7.0, 0))

        self.kill_count = OnscreenText(text="Experience Points: 0",
                                       pos=(0.3, 0.8),
                                       mayChange=True,
                                       align=TextNode.ALeft,
                                       font=self.default_font)

        self.menus = Menus(self)
        self.game_started = False

    def choose_hero(self):
        self.menus.select_character.show_menu()

    def start_game(self, hero_type):
        self.cleanup()
        [menu.hide_menu() for menu in self.menus]
        self.game_started = True
        if hero_type == "Wizard":
            self.hero = WizardHero(starting_position=Vec3(0, 0, 0))
        elif hero_type == "Warrior":
            self.hero = WarriorHero(starting_position=Vec3(0, 0, 0))

        self.hud = Hud(display_text=f"{self.hero.__class__.__name__}'s Health",
                       maximum_value=self.hero.proficiencies.health.maximum)
        self.hud.show()

        self.walking_enemies = []
        self.sliding_enemies = []
        self.deadEnemies = []

    def update(self, task):
        if not self.game_started:
            return task.cont

        # Get the amount of time since the last update
        time_delta = min(globalClock.getDt(), MAX_FRAME_RATE)

        if not self.hero.dead:
            self.hero.update(time_delta, keys=self.key_mapper)

            self.spawn_timer -= time_delta
            if self.spawn_timer <= 0 or len(self.walking_enemies) == 0:
                self.spawn_timer = self.spawn_time
                self.spawn_enemy()

            [walking_enemy.update(time_delta, hero=self.hero) for walking_enemy in self.walking_enemies]
            [sliding_enemy.update(time_delta, hero=self.hero) for sliding_enemy in self.sliding_enemies]

            self.walking_enemies = [enemy for enemy in self.walking_enemies if not enemy.dead]

            self.kill_count.setText(f"Experience Points: {self.hero.experience}")

            # Make sure to update visuals after all effects, or the frame might look weird
            self.hud.update_bar_value(self.hero.proficiencies.health.current)

        elif self.hero.dead:
            # If the game-over screen isn't showing...
            if self.menus.game_over.screen.isHidden():
                self.menus.game_over.screen.show()
                self.menus.game_over.modifiable_score_label["text"] = "Final score: " + str(self.hero.experience)
                self.menus.game_over.modifiable_score_label.setText()

        return task.cont

    def spawn_enemy(self):
        if len(self.walking_enemies) < self.maximum_walking_enemies:
            spawn_point = random.choice(self.spawn_points)
            new_enemy = TrainingDummyMonster(starting_position=spawn_point)
            self.walking_enemies.append(new_enemy)

    def cleanup(self):
        for walking_enemy in self.walking_enemies:
            walking_enemy.remove_object_from_world()
        for sliding_enemy in self.sliding_enemies:
            sliding_enemy.remove_object_from_world()
        if self.hero is not None:
            self.hero.remove_object_from_world()

    def quit(self):
        self.cleanup()
        base.userExit()

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
                        trap.ignorePlayer = True
                # If it hits a non-hero unit, take away 10 health.
                else:
                    obj.update_health(-10)


if __name__ in ['__main__', 'main']:
    game = Game()
    game.run()
