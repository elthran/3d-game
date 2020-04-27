from app.game.constants import States
from .base import *
from .archetype_selection import ArchetypeSelection


class GameOver(Menu):
    def __init__(self, *args, hero=None):
        super().__init__(*args)
        self.hero = hero

        self.screen = DirectDialog(frameSize=(-0.7, 0.7, -0.7, 0.7),
                                   fadeScreen=0.4,
                                   relief=DGG.FLAT,
                                   frameTexture="resources/images/stoneFrame.png")

        label = DirectLabel(text="Game Over!",
                            parent=self.screen,
                            scale=0.1,
                            pos=(0, 0, 0.2),
                            text_font=self.font,
                            relief=None)

        self.modifiable_score_label = DirectLabel(text="",
                                                  parent=self.screen,
                                                  scale=0.07,
                                                  pos=(0, 0, 0),
                                                  text_font=self.font,
                                                  relief=None)

        buttons = [
            Button(menu=self,
                   text="Restart",
                   command=self.next_menu,
                   extra_args=["ArchetypeSelection"],
                   parent=self.screen,
                   pos=(0, 0, 0.2)),
            Button(menu=self,
                   text="Quit",
                   command=self.exit_menu,
                   parent=self.screen,
                   pos=(0, 0, -0.2))
        ]

        if self.hero is not None:
            self.modifiable_score_label["text"] = "Total Kills: " + str(self.hero.kills)
            self.modifiable_score_label.setText()

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
