from app.game.constants import States
from .base import *


class SkillPointSelect(Menu):
    def __init__(self, *args, hero=None):
        super().__init__(*args)
        self.hero = hero

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
                        text_font=self.font,
                        text_fg=(1, 1, 1, 1)),
            DirectLabel(text="Choose a Skill to Learn",
                        scale=0.08,
                        pos=(0, 0, 0.75),
                        parent=self.menu,
                        relief=None,
                        text_font=self.font,
                        text_fg=(1, 1, 1, 1))
        ]

        buttons = [
            Button(menu=self,
                   text="Frost Ray",
                   command=self.exit_menu,
                   extra_args=["Frost Ray"],
                   parent=self.menu,
                   pos=(-0.9, 0, -0.5)),
            Button(menu=self,
                   text="Weapon Master",
                   command=self.exit_menu,
                   extra_args=["Weapon Master"],
                   parent=self.menu,
                   pos=(0, 0, -0.5)),
            Button(menu=self,
                   text="Regrowth",
                   command=self.exit_menu,
                   extra_args=["Regrowth"],
                   parent=self.menu,
                   pos=(0.9, 0, -0.5))
        ]

        self.hide_menu()

    def create_images(self):
        self.images = []

    def enter_menu(self):
        self.show_menu()

    def exit_menu(self, skill_name):
        self.hide_menu()
        self.hero.learn_skill(skill_name)
        self.game.state.set_next(States.RUNNING)
