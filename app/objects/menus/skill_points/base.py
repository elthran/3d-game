from direct.gui.DirectGui import DirectFrame, DirectLabel

from ..base import *


class SkillPointSelectTemplate(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title = [
            DirectLabel(text="Choose a Skill to Learn",
                        scale=0.1,
                        pos=(0, 0, 0.85),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]

        self.labels = {
            'skill_points':
                DirectLabel(text="",
                            scale=0.1,
                            pos=(0.9, 0, 0.1),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1))
        }

        self.archetype_button = None

        self.hide_menu()

    def choose_skill(self, skill_name):
        self.hero.learn_skill(skill_name)
        self.exit_menu()

    def update_text(self):
        self.labels['skill_points'].setText(f"Available Points: {self.hero.skill_points}")
