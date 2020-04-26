from direct.gui.DirectGui import DGG, DirectButton, DirectDialog, DirectFrame, DirectLabel
from direct.gui.OnscreenImage import OnscreenImage


class Menu:
    def __init__(self, game, *args):
        self.game = game

        self.font = self.game.default_font

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
