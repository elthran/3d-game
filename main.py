from app import *


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # properties = WindowProperties()
        # properties.setSize(1000, 750)
        # self.win.requestProperties(properties)

        self.updateTask = taskMgr.add(self.update, "update")

        self.hero = Hero()

        self.display_damage = OnscreenText(text=f'Damage taken: {5 - self.hero.health}', pos=(1, -0.9), scale=0.07)

        self.training_dummy_monster = TrainingDummyMonster(Vec3(5, 0, 0))

        self.crate_interactive = CrateInteractive(Vec3(-2, 3, 0))

        self.sliding_crate_monster = SlidingCrateMonster(Vec3(2, 7, 0))

    def update(self, task):
        # Get the amount of time since the last update
        time_delta = globalClock.getDt()

        self.hero.update(self.key_mapper, time_delta)

        self.training_dummy_monster.update(self.hero, time_delta)

        self.sliding_crate_monster.update(self.hero, time_delta)

        return task.cont


if __name__ in ['__main__', 'main']:
    # game = Game()
    game.run()
