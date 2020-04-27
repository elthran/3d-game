from direct.gui.DirectGui import DGG, DirectButton, DirectDialog, DirectFrame, DirectLabel
from direct.gui.OnscreenImage import OnscreenImage


class Menu:
    def __init__(self, game, *args):
        self.game = game

        self.default_font = loader.loadFont("resources/fonts/Wbxkomik.ttf")

        self.buttonImages = (loader.loadTexture("resources/images/UIButton.png"),  # Normal
                             loader.loadTexture("resources/images/UIButtonPressed.png"),  # Pressed
                             loader.loadTexture("resources/images/UIButtonHighlighted.png"),  # Rollover
                             loader.loadTexture("resources/images/UIButtonDisabled.png"))  # Disabled

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
        if self.backdrop is not None:
            self.backdrop.show()
        if self.menu is not None:
            self.menu.show()
        if self.screen is not None:
            self.screen.show()
        self.create_images()

    def create_images(self):
        pass


class Button:
    def __init__(self, menu, text, command, parent=None, extra_args=None, pos=(0, 0, 0)):

        if extra_args is None:
            extra_args = []

        button = DirectButton(text=text,
                              command=command,
                              extraArgs=extra_args,
                              pos=pos,
                              parent=parent,
                              scale=0.1,
                              text_font=menu.default_font,
                              clickSound=loader.loadSfx("resources/sounds/UIClick.ogg"),
                              frameTexture=menu.buttonImages,
                              frameSize=(-4, 4, -1, 1),
                              text_scale=0.75,
                              relief=DGG.FLAT,
                              text_pos=(0, -0.2))

        button.setTransparency(True)
