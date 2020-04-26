from direct.gui.DirectGui import DGG, DirectDialog, DirectFrame, DirectButton, DirectLabel
from direct.showbase.ShowBase import ShowBase

from panda3d.core import CollisionCapsule

from app import *
from app.objects.display_bars import Hud
from app.objects.heroes.archetype.brute import Brute
from app.objects.heroes.archetype.scholar import Scholar
from app.objects.heroes.deity.undying import Undying
from app.objects.menus.title import Title as TitleMenu
from app.objects.menus.attribute_point_select import AttributePointSelect as AttributePointSelectMenu
from app.objects.menus.game_over import GameOver as GameOverMenu
from app.objects.constants import States
from app.game.states import GameState

MAX_FRAME_RATE = 1 / 60


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.default_font = loader.loadFont("resources/fonts/Wbxkomik.ttf")

        background_music = loader.loadMusic("resources/music/background_theme.ogg")
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

        # self.environment = loader.loadModel("Misc/environment")
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

        self.hero = None
        self.hud = None
        self.walking_enemies = []
        self.sliding_enemies = []
        self.deadEnemies = []

        # Set up some monster spawn points
        self.spawn_time = 5
        self.spawn_timer = 1
        self.maximum_walking_enemies = 2
        self.spawn_points = []
        number_points_per_wall = 5
        for i in range(number_points_per_wall):
            coord = 7.0 / number_points_per_wall + 0.5
            self.spawn_points.append(Vec3(-7.0, coord, 0))
            self.spawn_points.append(Vec3(7.0, coord, 0))
            self.spawn_points.append(Vec3(coord, -7.0, 0))
            self.spawn_points.append(Vec3(coord, 7.0, 0))

        self.top_right_text = OnscreenText(text="Experience Points: 0",
                                       pos=(0.3, 0.8),
                                       mayChange=True,
                                       align=TextNode.ALeft,
                                       font=self.default_font)

        self.bottom_text = OnscreenText(text="Current Status:",
                                       pos=(0.3, -0.8),
                                       mayChange=True,
                                       align=TextNode.ALeft,
                                       font=self.default_font)


        self.current_task = None
        self.state = GameState(States.MENU, game=self)
        self.current_menu = TitleMenu(self)
        self.current_menu.enter_menu()

    def resume(self):
        self.current_task = taskMgr.add(self.update, "update")

    def pause(self):
        taskMgr.remove(self.current_task)

    def quit(self):
        self.cleanup()
        base.userExit()

    def start_game(self, hero_type):
        self.cleanup()

        self.game_started = True
        self.hero = Hero(starting_position=Vec3(0, 0, 0))
        if hero_type == "Wizard":
            self.hero.archetype = Scholar(self.hero)
        elif hero_type == "Warrior":
            self.hero.archetype = Brute(self.hero)
        # if hero_type == "Wizard":
        #     self.hero = Scholar(starting_position=Vec3(0, 0, 0))
        # elif hero_type == "Warrior":
        #     self.hero = Brute(starting_position=Vec3(0, 0, 0))

        self.hud_health = Hud(maximum_value=self.hero.proficiencies.health.maximum,
                              pos=(-0.2, 0, base.a2dTop - 0.15),
                              barColor=(0, 1, 0.25, 1))
        self.hud_health.show()

        self.hud_mana = Hud(maximum_value=self.hero.proficiencies.mana.maximum,
                            pos=(-0.2, 0, base.a2dTop - 0.3),
                            barColor=(0, 0, 2.55, 1))
        self.hud_mana.show()

        self.walking_enemies = []
        self.sliding_enemies = []
        self.deadEnemies = []

    def update(self, task):
        # Get the amount of time since the last update
        time_delta = min(globalClock.getDt(), MAX_FRAME_RATE)

        if not self.hero.dead:
            self.hero.update(time_delta, keys=self.key_mapper)

            self.spawn_timer -= time_delta
            if self.spawn_timer <= 0 and len(self.walking_enemies) < self.hero.level:
                self.spawn_timer = self.spawn_time / self.hero.level
                self.spawn_enemy()

            [walking_enemy.update(time_delta, hero=self.hero) for walking_enemy in self.walking_enemies]
            [sliding_enemy.update(time_delta, hero=self.hero) for sliding_enemy in self.sliding_enemies]

            self.walking_enemies = [enemy for enemy in self.walking_enemies if not enemy.dead]

            self.top_right_text.setText(f"Level: {self.hero.level}. "
                                    f"Experience Points: {self.hero.experience}/{self.hero.experience_maximum}. "
                                    f"\nHealth: {self.hero.proficiencies.health.current}/{self.hero.proficiencies.health.maximum}"
                                    f"\nStrength: {self.hero.attributes.strength.level}"
                                    f"\nDamage: {self.hero.proficiencies.melee_attack.damage}")

            self.bottom_text.setText(f"Afflictions: {[effect.name for effect in self.hero.active_effects]}")

            # Make sure to update visuals after all effects, or the frame might look weird
            self.hud_health.update_bar_value(self.hero.proficiencies.health.current)
            self.hud_mana.update_bar_value(self.hero.proficiencies.mana.current)

            if self.hero.attribute_points > 0:
                self.state.set_next(States.MENU)
                attribute_point_select_menu = AttributePointSelectMenu(self, hero=self.hero)
                attribute_point_select_menu.enter_menu()

            # Add code so you become Undying
            if self.hero.religion is None:
                self.hero.religion = Undying(self.hero)
                print(f"Hero is a {self.hero.religion}")


        elif self.hero.dead:
            self.state.set_next(States.MENU)
            game_over_menu = GameOverMenu(self, self.hero.kills)
            game_over_menu.enter_menu()

        return task.cont

    def spawn_enemy(self):
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


if __name__ == "__main__":
    game = Game()
    game.run()
