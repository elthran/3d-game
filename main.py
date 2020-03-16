from app import *


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # properties = WindowProperties()
        # properties.setSize(1000, 750)
        # self.win.requestProperties(properties)


        self.hero = Hero()

        self.display_damage = OnscreenText(text=f'Damage taken: {5 - self.hero.health}', pos=(1, -0.9), scale=0.07)

        self.training_dummy_monster = TrainingDummyMonster(Vec3(5, 0, 0))

        self.crate_interactive = CrateInteractive(Vec3(-2, 3, 0))

        self.sliding_crate_monster = SlidingCrateMonster(Vec3(2, 7, 0))


if __name__ in ['__main__', 'main']:
    # game = Game()
    game.run()
