from ..base import *


class Scholar(SkillPointSelectTemplate):
    def __init__(self, *args):
        super().__init__(*args)

        skills = [skill for skill in self.hero.abilities if skill.skill_tree == "Scholar"]

        buttons = [
            Button(menu=self,
                   text=f"{skills[0].name}",
                   command=self.choose_skill,
                   extra_args=[f"{skills[0].name}"],
                   parent=self.menu,
                   pos=(-0.9, 0, -0.3)),
            Button(menu=self,
                   text=f"{skills[1].name}",
                   command=self.choose_skill,
                   extra_args=[f"{skills[1].name}"],
                   parent=self.menu,
                   pos=(0, 0, -0.3)),
            Button(menu=self,
                   text=f"{skills[2].name}",
                   command=self.choose_skill,
                   extra_args=[f"{skills[2].name}"],
                   parent=self.menu,
                   pos=(0.9, 0, -0.3)),
            Button(menu=self,
                   text="Resume",
                   command=self.exit_menu,
                   parent=self.menu,
                   pos=(0, 0, 0.5))
        ]

        labels = [
            DirectLabel(text=f"{skills[0].description}",
                        scale=0.03,
                        pos=(-0.9, 0, -0.6),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1)),
            DirectLabel(text=f"{skills[1].description}",
                        scale=0.03,
                        pos=(0, 0, -0.6),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1)),
            DirectLabel(text=f"{skills[2].description}",
                        scale=0.03,
                        pos=(0.9, 0, -0.6),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]