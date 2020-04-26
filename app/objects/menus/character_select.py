from app.objects.constants import States
from .base import *


class CharacterSelect(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title_1 = DirectLabel(text="Select Hero",
                              scale=0.1,
                              pos=(0, 0, 0.9),
                              parent=self.menu,
                              relief=None,
                              text_font=self.font,
                              text_fg=(1, 1, 1, 1))

        button = DirectButton(text="Wizard",
                              command=self.exit_menu,
                              extraArgs=["Wizard"],
                              pos=(-0.8, 0, -0.5),
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

        button = DirectButton(text="Warrior",
                              command=self.exit_menu,
                              extraArgs=["Warrior"],
                              pos=(0.8, 0, -0.5),
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

    def create_images(self):
        self.images = [OnscreenImage(image='resources/images/wizard.jpg', pos=(-0.8, 0, 0.1), scale=0.4),
                       OnscreenImage(image='resources/images/warrior.jpg', pos=(0.8, 0, 0.1), scale=0.4)]


    def enter_menu(self):
        self.show_menu()

    def exit_menu(self, character_name):
        self.hide_menu()
        self.game.start_game(character_name)
        self.game.state.set_next(States.RUNNING)
