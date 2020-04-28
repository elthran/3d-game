from .base import Hud


class Huds:
    def __init__(self, game):
        self.game = game
        self.hud_health = Hud(maximum_value=0,
                              pos=(-0.2, 0, base.a2dTop - 0.15),
                              barColor=(0, 1, 0.25, 1))
        self.hud_mana = Hud(maximum_value=0,
                            pos=(-0.2, 0, base.a2dTop - 0.3),
                            barColor=(0, 0, 2.55, 1))

    def __iter__(self):
        return iter([self.hud_health, self.hud_mana])

    def update(self, hero):
        self.hud_health.update_bar_value(new_value=hero.proficiencies.health.current,
                                         maximum_value=hero.proficiencies.health.maximum)

        self.hud_mana.update_bar_value(new_value=hero.proficiencies.mana.current,
                                       maximum_value=hero.proficiencies.mana.maximum)

    def hide(self):
        for hud in self:
            hud.hide()

    def show(self):
        for hud in self:
            hud.show()
