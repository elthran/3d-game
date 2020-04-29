from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class User:
    def __init__(self):
        self.score = 0

        self.health_icons = []

    def set_hero(self, Hero):
        for i in range(Hero.max_health):
            icon = OnscreenImage(image="resources/images/health.png",
                                 pos=(-1.275 + i * 0.075, 0, 0.95),
                                 scale=0.04)
            # Since our icons have transparent regions, we'll activate transparency.
            icon.setTransparency(True)
            self.health_icons.append(icon)

    def update_health_UI(self):
        for index, icon in enumerate(self.health_icons):
            if index < self.health:
                icon.show()
            else:
                icon.hide()
