from app.game.constants import States
from .base import *


class ReligionSelection(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title = DirectLabel(text="Select Religion",
                            scale=0.1,
                            pos=(0, 0, 0.9),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1))

        self.undying_x_pos = -0.7
        self.burning_sands_x_pos = 0.7

        buttons = [
            Button(menu=self,
                   text="Undying",
                   command=self.exit_menu,
                   extra_args=["Undying"],
                   parent=self.menu,
                   pos=(self.undying_x_pos, 0, 0.1)),
            Button(menu=self,
                   text="Burning Sands",
                   command=self.exit_menu,
                   extra_args=["Burning Sands"],
                   parent=self.menu,
                   pos=(self.burning_sands_x_pos, 0, 0.1))
        ]

        labels = [
            DirectLabel(text="Gain Frost Resistance",
                        scale=0.04,
                        pos=(self.undying_x_pos, 0, -0.2),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1)),
            DirectLabel(text="Gain Fire Resistance",
                        scale=0.04,
                        pos=(self.burning_sands_x_pos, 0, -0.2),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]

        self.hide_menu()

    def create_images(self):
        self.images = []

    def enter_menu(self):
        self.show_menu()

    def exit_menu(self, religion):
        self.hide_menu()
        self.game.select_religion(religion)
