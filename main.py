from direct.showbase.ShowBase import ShowBase

from app import *
from app.maps.base import World
from app.objects.game_objects.physicals.characters.heroes.archetype.brute import Brute
from app.objects.game_objects.physicals.characters.heroes.archetype.scholar import Scholar
from app.objects.game_objects.physicals.characters.heroes.deity.undying import Undying
from app.objects.huds import Huds
from app.objects.menus.home import Home as TitleMenu
from app.objects.menus.attribute_point_select import AttributePointSelect as AttributePointSelectMenu
from app.objects.menus.skill_point_select import SkillPointSelect as SkillPointSelectMenu
from app.objects.menus.game_over import GameOver as GameOverMenu
from app.game.constants import States
from app.game.states import GameState
from app.objects.menus.religion_selection import ReligionSelection

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

        self.huds = Huds(game)

        self.hero = None
        self.world = None

        self.default_font = loader.loadFont("resources/fonts/Wbxkomik.ttf")
        self.top_right_text = OnscreenText(text="Experience Points: 0",
                                           pos=(0.8, 0.9),
                                           mayChange=True,
                                           align=TextNode.ALeft)

        self.bottom_text = OnscreenText(text="Current Status:",
                                        pos=(0.3, -0.8),
                                        mayChange=True,
                                        align=TextNode.ALeft)

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
        self.hero.refresh()

        self.world = World(game=self)

    def select_religion(self, religion):
        if religion == "Undying":
            self.hero.religion = Undying(self.hero)
        attribute_point_select_menu = AttributePointSelectMenu(self, hero=self.hero)
        attribute_point_select_menu.enter_menu()

    def update(self, task):
        # Get the amount of time since the last update
        time_delta = min(globalClock.getDt(), MAX_FRAME_RATE)

        if not self.hero.dead:
            self.hero.update(time_delta, keys=self.key_mapper)

            self.world.update(time_delta=time_delta)

            self.top_right_text.setText(f"""
Level: {self.hero.level}.
Health: {self.hero.proficiencies.health.current}/{self.hero.proficiencies.health.maximum}
Mana: {self.hero.proficiencies.mana.current}/{self.hero.proficiencies.mana.maximum}
Experience: {self.hero.experience}/{self.hero.experience_maximum}
Movement Speed: {self.hero.proficiencies.movement.speed_maximum}
Acceleration: {self.hero.acceleration}
Damage: {self.hero.proficiencies.melee_attack.damage}
Regeneration: {self.hero.proficiencies.health.regeneration_amount}
""")

            self.bottom_text.setText(f"Afflictions: {[effect.name for effect in self.hero.active_effects]}")

            # Make sure to update visuals after all effects, or the frame might look weird
            self.huds.update(health=self.hero.proficiencies.health.current,
                             mana=self.hero.proficiencies.mana.current,
                             health_maximum=self.hero.proficiencies.health.maximum,
                             mana_maximum=self.hero.proficiencies.mana.maximum)

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