from app.objects.constants import States
from .base import *


class AttributePointSelect(Menu):
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
            DirectLabel(text="Choose an Attribute to Increase",
                        scale=0.08,
                        pos=(0, 0, 0.75),
                        parent=self.menu,
                        relief=None,
                        text_font=self.font,
                        text_fg=(1, 1, 1, 1))
        ]

        buttons = [
            Button(menu=self,
                   text="Strength",
                   command=self.exit_menu,
                   extra_args=["Strength"],
                   parent=self.menu,
                   pos=(-0.9, 0, -0.5)),
            Button(menu=self,
                   text="Vitality",
                   command=self.exit_menu,
                   extra_args=["Vitality"],
                   parent=self.menu,
                   pos=(0, 0, -0.5)),
            Button(menu=self,
                   text="Intellect",
                   command=self.exit_menu,
                   extra_args=["Intellect"],
                   parent=self.menu,
                   pos=(0.9, 0, -0.5))
        ]

        self.hide_menu()

    def create_images(self):
        self.images = []

    def enter_menu(self):
        self.show_menu()

    def exit_menu(self, attribute_name):
        self.hide_menu()
        self.hero.gain_attribute(attribute_name)
        self.game.state.set_next(States.RUNNING)
