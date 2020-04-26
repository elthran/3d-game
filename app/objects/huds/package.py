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

    def update(self, health=None, mana=None, health_maximum=None, mana_maximum=None):
        self.hud_health.update_bar_value(new_value=health, maximum_value=health_maximum)
        self.hud_mana.update_bar_value(new_value=mana, maximum_value=mana_maximum)

    def hide(self):
        for hud in self:
            hud.hide()

    def show(self):
        for hud in self:
            hud.show()
