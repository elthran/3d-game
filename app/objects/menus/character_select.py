from app.objects.constants import States
from .base import *


class CharacterSelect(Menu):
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
                            text_font=self.font,
                            text_fg=(1, 1, 1, 1))

        self.brute_x_pos = -0.8
        self.scholar_x_pos = 0.8

        buttons = [
            Button(menu=self,
                   text="Brute",
                   command=self.exit_menu,
                   extra_args=["Brute"],
                   pos=(self.brute_x_pos, 0, -0.5)),
            Button(menu=self,
                   text="Scholar",
                   command=self.exit_menu,
                   extra_args=["Scholar"],
                   pos=(self.scholar_x_pos, 0, -0.5))
        ]

        self.hide_menu()

    def create_images(self):
        self.images = [
            OnscreenImage(image='resources/images/wizard.jpg', pos=(self.scholar_x_pos, 0, 0.1), scale=0.4),
            OnscreenImage(image='resources/images/warrior.jpg', pos=(self.brute_x_pos, 0, 0.1), scale=0.4)
        ]

    def enter_menu(self):
        self.show_menu()

    def exit_menu(self, character_name):
        self.hide_menu()
        self.game.start_game(character_name)
        self.game.state.set_next(States.RUNNING)
