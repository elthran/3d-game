from direct.gui.DirectGui import DirectFrame, DirectLabel

from app.objects.menus.base import *
from .archetypes.brute import Brute
from .archetypes.scholar import Scholar


class SkillPointSelect(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title = [
            DirectLabel(text="Choose a Skill to Learn",
                        scale=0.1,
                        pos=(0, 0, 0.85),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]

        self.archetype_button = None
        self.religion_button = None
        self.specialization_button = None

        self.hide_menu()

    def update_text(self):
        if self.hero.archetype and self.archetype_button is None:
            # next_menu = getattr(f"{self.hero.archetype.name}", "enter_menu")
            next_menu = None
            if self.hero.archetype.name == "Brute":
                next_menu = Brute(self.game)
            elif self.hero.archetype.name == "Scholar":
                next_menu = Scholar(self.game)
            self.archetype_button = Button(menu=self,
                                           text=f"{self.hero.archetype.name}",
                                           command=self.next_menu,
                                           extra_args=[next_menu],
                                           parent=self.menu,
                                           pos=(-0.95, 0, 0.6))

        if self.religion_button is None:
            self.religion_button = Button(menu=self,
                                          text=f"No Religion",
                                          command=None,
                                          parent=self.menu,
                                          pos=(0.0, 0, 0.6))
        if self.specialization_button is None:
            self.specialization_button = Button(menu=self,
                                                text=f"No Specialization",
                                                command=None,
                                                parent=self.menu,
                                                pos=(0.95, 0, 0.6))

    def choose_skill(self, skill_name):
        self.hero.learn_skill(skill_name)
        self.exit_menu()
