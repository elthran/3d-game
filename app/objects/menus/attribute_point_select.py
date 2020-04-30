from direct.gui.DirectGui import DirectFrame, DirectLabel

from .base import *


class AttributePointSelect(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.hero = None

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        self.titles = {
            'top': DirectLabel(text="Level Up!",
                               scale=0.1,
                               pos=(0, 0, 0.85),
                               parent=self.menu,
                               relief=None,
                               text_font=self.default_font,
                               text_fg=(1, 1, 1, 1)),
            'bottom':
                DirectLabel(text="Choose an Attribute to Increase",
                            scale=0.08,
                            pos=(0, 0, 0.75),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1))
        }

        self.buttons = {
            'strength':
                Button(menu=self,
                       text="Strength",
                       command=self.gain_attribute,
                       extra_args=["Strength"],
                       parent=self.menu,
                       pos=(-0.9, 0, -0.5)),
            'vitality':
                Button(menu=self,
                       text="Vitality",
                       command=self.gain_attribute,
                       extra_args=["Vitality"],
                       parent=self.menu,
                       pos=(0, 0, -0.5)),
            'intellect':
                Button(menu=self,
                       text="Intellect",
                       command=self.gain_attribute,
                       extra_args=["Intellect"],
                       parent=self.menu,
                       pos=(0.9, 0, -0.5))
        }

        self.labels = {
            'available_points':
                DirectLabel(text="",
                            scale=0.1,
                            pos=(0.9, 0, 0.1),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1)),
            'strength':
                DirectLabel(text="",
                            scale=0.04,
                            pos=(-0.9, 0, -0.7),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1)),
            'vitality':
                DirectLabel(text="",
                            scale=0.04,
                            pos=(0, 0, -0.7),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1)),
            'intellect':
                DirectLabel(text="",
                            scale=0.04,
                            pos=(0.9, 0, -0.7),
                            parent=self.menu,
                            relief=None,
                            text_font=self.default_font,
                            text_fg=(1, 1, 1, 1))
        }

        self.hide_menu()

    def update_text(self):
        self.labels['strength'].setText(str(self.hero.attributes.strength.level))
        self.labels['vitality'].setText(str(self.hero.attributes.vitality.level))
        self.labels['intellect'].setText(str(self.hero.attributes.intellect.level))
        self.labels['available_points'].setText(f"Available Points: {self.hero.attribute_points}")

    def gain_attribute(self, attribute_name):
        if self.hero.attribute_points > 0:
            self.game.hero.gain_attribute(attribute_name)
            self.update_text()
