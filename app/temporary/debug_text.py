from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class DebugText:
    def __init__(self):
        self.top_right_text = OnscreenText(text="",
                                           scale=0.05,
                                           pos=(0.6, 0.9),
                                           mayChange=True,
                                           align=TextNode.ALeft)

        self.bottom_text = OnscreenText(text="",
                                        scale=0.05,
                                        pos=(0.3, -0.8),
                                        mayChange=True,
                                        align=TextNode.ALeft)

    def update(self, hero):
        self.top_right_text.setText(f"""
                    Character: {hero.identity}
                    Level: {hero.level}
                    Health: {round(hero.proficiencies.health.current, 3)}/{hero.proficiencies.health.maximum}
                    Mana: {round(hero.proficiencies.mana.current, 3)}/{hero.proficiencies.mana.maximum}
                    Experience: {hero.experience}/{hero.experience_maximum}
                    Movement Speed: {hero.proficiencies.movement.speed_maximum}
                    Acceleration: {hero.acceleration}
                    Melee Damage: {hero.proficiencies.melee_attack.damage}
                    Regeneration: {hero.proficiencies.health.regeneration_amount}
                    Resistances:
                        Physical: {hero.proficiencies.resistances.physical}
                        Magical: {hero.proficiencies.resistances.magical}
                        Fire: {hero.proficiencies.resistances.fire}
                        Frost: {hero.proficiencies.resistances.frost}
        """)

        self.bottom_text.setText(f"""
                    Status Effects: {[effect.name for effect in hero.active_effects]}
        """)