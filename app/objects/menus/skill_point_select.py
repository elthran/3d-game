from direct.gui.DirectGui import DirectFrame, DirectLabel

from .base import *


class SkillPointSelect(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title = [
            DirectLabel(text="Level Up!",
                        scale=0.1,
                        pos=(0, 0, 0.85),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1)),
            DirectLabel(text="Choose a Skill to Learn",
                        scale=0.08,
                        pos=(0, 0, 0.75),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]

        buttons = [
            Button(menu=self,
                   text="Frost Ray",
                   command=self.choose_skill,
                   extra_args=["Frost Ray"],
                   parent=self.menu,
                   pos=(-0.9, 0, -0.5)),
            Button(menu=self,
                   text="Weapon Master",
                   command=self.choose_skill,
                   extra_args=["Weapon Master"],
                   parent=self.menu,
                   pos=(0, 0, -0.5)),
            Button(menu=self,
                   text="Regrowth",
                   command=self.choose_skill,
                   extra_args=["Regrowth"],
                   parent=self.menu,
                   pos=(0.9, 0, -0.5))
        ]

        self.hide_menu()

    def choose_skill(self, skill_name):
        self.hero.learn_skill(skill_name)
        self.exit_menu()
