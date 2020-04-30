from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.gui.OnscreenImage import OnscreenImage


from .base import *


class ArchetypeSelection(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title = DirectLabel(text="Select Hero",
                            scale=0.1,
                            pos=(0, 0, 0.9),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1))

        self.brute_x_pos = -0.8
        self.scholar_x_pos = 0.8

        buttons = [
            Button(menu=self,
                   text="Brute",
                   command=self.choose_archetype,
                   extra_args=["Brute"],
                   parent=self.menu,
                   pos=(self.brute_x_pos, 0, -0.5)),
            Button(menu=self,
                   text="Scholar",
                   command=self.choose_archetype,
                   extra_args=["Scholar"],
                   parent=self.menu,
                   pos=(self.scholar_x_pos, 0, -0.5))
        ]


        labels = [
            DirectLabel(text="Strong and Tough",
                        scale=0.04,
                        pos=(self.brute_x_pos, 0, -0.7),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1)),
            DirectLabel(text="Adept at Magic",
                        scale=0.04,
                        pos=(self.scholar_x_pos, 0, -0.7),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]

        self.hide_menu()

    def create_images(self):
        self.images = [
            OnscreenImage(image='resources/images/wizard.jpg', pos=(self.scholar_x_pos, 0, 0.1), scale=0.4),
            OnscreenImage(image='resources/images/warrior.jpg', pos=(self.brute_x_pos, 0, 0.1), scale=0.4)
        ]

    def enter_menu(self):
        self.show_menu()

    def choose_archetype(self, archetype_name):
        self.hide_menu()
        self.game.start_game(archetype_name)
        self.game.state.set_next(States.RUNNING)
