from direct.showbase.ShowBase import ShowBase

from app import *
from app.game.constants import States
from app.game.states import GameState
from app.maps import World
from app.objects.game_objects.physicals.characters.heroes.deity.burning_sands import BurningSands
from app.temporary.debug_text import DebugText

MAX_FRAME_RATE = 1 / 60


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        self.camera.setPos(0, -20, 32)
        self.camera.setP(-60)

        self.key_mapper = KeyMapper.initialize(self)

        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()
        self.cTrav.setRespectPrevTransform(True)
        self.pusher.setHorizontal(True)

        self.huds = Huds(self)

        self.hero = None
        self.world = None

        self.default_font = loader.loadFont("resources/fonts/Wbxkomik.ttf")

        self.debug_text = DebugText()

        self.current_task = None
        self.state = GameState(States.MENU, game=self)
        self.current_menu = TitleMenu(self)
        self.current_menu.enter_menu()

    def resume(self):
        self.current_task = taskMgr.add(self.update, "update")
        self.huds.show()

    def pause(self):
        taskMgr.remove(self.current_task)
        self.huds.hide()

    def quit(self):
        self.cleanup()
        base.userExit()

    def start_game(self, hero_type):
        self.cleanup()

        self.hero = Hero(starting_position=Vec3(0, 0, 0))
        if hero_type == "Scholar":
            self.hero.archetype = Scholar(self.hero)
        elif hero_type == "Brute":
            self.hero.archetype = Brute(self.hero)
        else:
            raise ValueError(f"Archetype {hero_type} unknown.")
        self.hero.refresh()

        self.world = World(game=self)

    def select_religion(self, religion):
        if religion == "Undying":
            self.hero.religion = Undying(self.hero)
        elif religion == "Burning Sands":
            self.hero.religion = BurningSands(self.hero)
        else:
            raise ValueError(f"Religion {religion} unknown.")
        attribute_point_select_menu = AttributePointSelectMenu(self, hero=self.hero)
        attribute_point_select_menu.enter_menu()

    def update(self, task):
        # Get the amount of time since the last update
        time_delta = min(globalClock.getDt(), MAX_FRAME_RATE)

        if not self.hero.dead:
            self.hero.update(time_delta, keys=self.key_mapper)

            self.world.update(time_delta=time_delta)

            self.debug_text.update(hero=self.hero)

            # Make sure to update visuals after all effects, or the frame might look weird
            self.huds.update(hero=self.hero)

            if self.hero.level == 2 and self.hero.religion is None:
                self.state.set_next(States.MENU)
                religion_select_menu = ReligionSelection(self)
                religion_select_menu.enter_menu()
            elif self.hero.attribute_points > 0:
                self.state.set_next(States.MENU)
                attribute_point_select_menu = AttributePointSelectMenu(self, hero=self.hero)
                attribute_point_select_menu.enter_menu()
            elif self.hero.skill_points > 0:
                self.state.set_next(States.MENU)
                skill_point_select_menu = SkillPointSelectMenu(self, hero=self.hero)
                skill_point_select_menu.enter_menu()

            self.camera.setPos(self.hero.actor.getX(), self.hero.actor.getY() - 20, 32)

        elif self.hero.dead:
            self.state.set_next(States.MENU)
            game_over_menu = GameOverMenu(self, self.hero.kills)
            game_over_menu.enter_menu()

        return task.cont

    def cleanup(self):
        if self.world is not None:
            self.world.cleanup()
        if self.hero is not None:
            self.hero.remove_object_from_world()


if __name__ == "__main__":
    game = Game()
    game.run()
