from direct.gui.DirectGui import DGG, DirectButton, DirectDialog, DirectFrame, DirectLabel
from direct.gui.OnscreenImage import OnscreenImage


class Menus:
    def __init__(self, game):
        self.game = game
        self.title = TitleMenu(game)
        self.game_over = GameOverMenu(game)
        self.select_character = CharacterSelectMenu(game)

    def __iter__(self):
        return iter([self.title, self.game_over, self.select_character])


class Menu:
    def __init__(self, game, *args):
        self.game = game

        self.font = self.game.default_font

        self.buttonImages = (loader.loadTexture("UI/UIButton.png"),  # Normal
                             loader.loadTexture("UI/UIButtonPressed.png"),  # Pressed
                             loader.loadTexture("UI/UIButtonHighlighted.png"),  # Rollover
                             loader.loadTexture("UI/UIButtonDisabled.png"))  # Disabled

        self.backdrop = None

        self.menu = None

        self.screen = None

        self.images = []

    def hide_menu(self):
        if self.backdrop is not None:
            self.backdrop.hide()
        if self.menu is not None:
            self.menu.hide()
        if self.screen is not None:
            self.screen.hide()
        for image in self.images:
            image.destroy()

    def show_menu(self):
        [menu.hide_menu() for menu in self.game.menus]
        if self.backdrop is not None:
            self.backdrop.show()
        if self.menu is not None:
            self.menu.show()
        if self.screen is not None:
            self.screen.show()
        self.create_images()

    def create_images(self):
        pass


class TitleMenu(Menu):
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
                              command=self.game.choose_hero,
                              pos=(0, 0, 0.2),
                              parent=self.menu,
                              scale=0.1,
                              text_font=self.font,
                              clickSound=loader.loadSfx("Sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)

        button = DirectButton(text="Quit",
                              command=self.game.quit,
                              pos=(0, 0, -0.2),
                              parent=self.menu,
                              scale=0.1,
                              text_font=self.font,
                              clickSound=loader.loadSfx("Sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)


class CharacterSelectMenu(Menu):
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
                              command=self.game.start_game,
                              extraArgs=["Wizard"],
                              pos=(-0.8, 0, -0.5),
                              parent=self.menu,
                              scale=0.1,
                              text_font=self.font,
                              clickSound=loader.loadSfx("Sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)

        button = DirectButton(text="Warrior",
                              command=self.game.start_game,
                              extraArgs=["Warrior"],
                              pos=(0.8, 0, -0.5),
                              parent=self.menu,
                              scale=0.1,
                              text_font=self.font,
                              clickSound=loader.loadSfx("Sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)

        self.hide_menu()

    def create_images(self):
        self.images = [OnscreenImage(image='Models/resources/wizard.jpg', pos=(-0.8, 0, 0.1), scale=0.4),
                       OnscreenImage(image='Models/resources/warrior.jpg', pos=(0.8, 0, 0.1), scale=0.4)]


class GameOverMenu(Menu):
    def __init__(self, *args):
        super().__init__(*args)
        self.screen = DirectDialog(frameSize=(-0.7, 0.7, -0.7, 0.7),
                                   fadeScreen=0.4,
                                   relief=DGG.FLAT,
                                   frameTexture="UI/stoneFrame.png")

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

        button = DirectButton(text="Restart",
                              command=self.game.start_game,
                              pos=(-0.3, 0, -0.2),
                              parent=self.screen,
                              scale=0.07,
                              text_font=self.font,
                              clickSound=loader.loadSfx("Sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)

        button = DirectButton(text="Quit",
                              command=self.game.quit,
                              pos=(0.3, 0, -0.2),
                              parent=self.screen,
                              scale=0.07,
                              text_font=self.font,
                              clickSound=loader.loadSfx("Sounds/UIClick.ogg"),
                              frameTexture=self.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))
        button.setTransparency(True)

        self.hide_menu()
