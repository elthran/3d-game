from app.game.constants import States
from .base import *
from .archetype_selection import ArchetypeSelection


class Home(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title = [
            DirectLabel(text="Elthran's World",
                        scale=0.1,
                        pos=(0, 0, 0.9),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1)),
            DirectLabel(text="featuring",
                        scale=0.07,
                        pos=(0, 0, 0.79),
                        parent=self.menu,
                        text_font=self.default_font,
                        frameColor=(0.5, 0.5, 0.5, 1)),
            DirectLabel(text="Klondikemarlen",
                        scale=0.08,
                        pos=(0, 0, 0.65),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]

        buttons = [
            Button(menu=self,
                   text="Start Game",
                   command=self.next_menu,
                   extra_args=["ArchetypeSelection"],
                   parent=self.menu,
                   pos=(0, 0, 0.2)),
            Button(menu=self,
                   text="Quit",
                   command=self.exit_menu,
                   parent=self.menu,
                   pos=(0, 0, -0.2))
        ]

        self.hide_menu()

    def enter_menu(self):
        self.show_menu()

    def next_menu(self, menu_name):
        self.hide_menu()
        if menu_name == "ArchetypeSelection":
            archetype_selection = ArchetypeSelection(self.game)
            archetype_selection.enter_menu()

    def exit_menu(self):
        self.hide_menu()
        self.game.state.set_next(States.QUIT)
