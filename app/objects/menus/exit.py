from direct.gui.DirectGui import DirectFrame

from .base import *


class Exit(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.hero = None

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        self.buttons = {
            'resume':
                Button(menu=self,
                       text="Resume",
                       command=self.resume_game,
                       parent=self.menu,
                       pos=(0, 0, 0.2)),
            'exit':
                Button(menu=self,
                       text="Exit",
                       command=self.exit_game,
                       parent=self.menu,
                       pos=(0, 0, -0.2))
        }

        self.hide_menu()
