from app.objects.constants import States
from .base import *
from .character_select import CharacterSelect


class Title(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title_1 = DirectLabel(text="Elthran's World",
                              scale=0.1,
                              pos=(0, 0, 0.9),
                              parent=self.menu,
                              relief=None,
                              text_font=self.font,
                              text_fg=(1, 1, 1, 1))

        title_2 = DirectLabel(text="featuring",
                              scale=0.07,
                              pos=(0, 0, 0.79),
                              parent=self.menu,
                              text_font=self.font,
                              frameColor=(0.5, 0.5, 0.5, 1))

        title_3 = DirectLabel(text="Klondikemarlen",
                              scale=0.08,
                              pos=(0, 0, 0.65),
                              parent=self.menu,
                              relief=None,
                              text_font=self.font,
                              text_fg=(1, 1, 1, 1))

        button = DirectButton(text="Start Game",
                              command=self.next_menu,
                              extraArgs=["CharacterSelect"],
                              pos=(0, 0, 0.2),
                              parent=self.menu,
                              scale=0.1,
                              text_font=self.font,
                              clickSound=loader.loadSfx("resources/sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)

        button = DirectButton(text="Quit",
                              command=self.exit_menu,
                              pos=(0, 0, -0.2),
                              parent=self.menu,
                              scale=0.1,
                              text_font=self.font,
                              clickSound=loader.loadSfx("resources/sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)

        self.hide_menu()

    def enter_menu(self):
        self.show_menu()


    def next_menu(self, menu_name):
        self.hide_menu()
        if menu_name == "CharacterSelect":
            character_select = CharacterSelect(self.game)
            character_select.enter_menu()


    def exit_menu(self):
        self.hide_menu()
        self.game.state.set_next(States.QUIT)
