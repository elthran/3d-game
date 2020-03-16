from app import *


class FinalTweaks:
    def __init__(self, app):
        app.hero = Hero()

        app.display_damage = OnscreenText(text=f'Damage taken: {5 - app.hero.health}', pos=(1, -0.9), scale=0.07)

        app.training_dummy_monster = TrainingDummyMonster(Vec3(5, 0, 0))

        app.crate_interactive = CrateInteractive(Vec3(-2, 3, 0))

        app.sliding_crate_monster = SlidingCrateMonster(Vec3(2, 7, 0))




if __name__ in ['__main__', 'main']:
    FinalTweaks(game)
    game.run()
