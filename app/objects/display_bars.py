from direct.gui.DirectGui import DirectWaitBar, DGG
from panda3d.core import TextNode


class Hud:
    def __init__(self, display_text=None, maximum_value=None):
        self.player_health_bar = DirectWaitBar(text=display_text,
                                               text_fg=(1, 1, 1, 1),
                                               text_pos=(-1.2, -0.18, 0),
                                               text_align=TextNode.ALeft,
                                               value=maximum_value,
                                               range=maximum_value,
                                               barColor=(0, 1, 0.25, 1),
                                               barRelief=DGG.RAISED,
                                               barBorderWidth=(0.03, 0.03),
                                               borderWidth=(0.01, 0.01),
                                               relief=DGG.RIDGE,
                                               frameColor=(0.8, 0.05, 0.10, 1),
                                               frameSize=(-1.2, 0, 0, -0.1),
                                               pos=(-0.2, 0, base.a2dTop - 0.15))

        self.player_health_bar.setTransparency(1)

        self.hide()

    def show(self):
        self.player_health_bar["value"] = 8
        self.player_health_bar.show()

    def hide(self):
        self.player_health_bar.hide()

    def update_bar_value(self, new_value):
        self.player_health_bar["value"] = new_value
