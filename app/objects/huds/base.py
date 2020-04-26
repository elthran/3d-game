import math

from direct.gui.DirectGui import DirectWaitBar, DGG
from panda3d.core import TextNode


class Hud:
    def __init__(self,
                 maximum_value=None,
                 pos=None,
                 barColor=None):
        self.maximum_value = maximum_value
        self.display_bar = DirectWaitBar(text_align=TextNode.ALeft,
                                         value=maximum_value,
                                         range=maximum_value,
                                         barColor=barColor,
                                         barRelief=DGG.RAISED,
                                         barBorderWidth=(0.03, 0.03),
                                         borderWidth=(0.01, 0.01),
                                         relief=DGG.RIDGE,
                                         frameColor=(0.8, 0.05, 0.10, 1),
                                         frameSize=(-1.2, 0, 0, -0.1),
                                         pos=pos)

        self.display_bar.setTransparency(1)

        self.hide()

    def show(self):
        self.display_bar["value"] = self.maximum_value
        self.display_bar.show()

    def hide(self):
        self.display_bar.hide()

    def update_bar_value(self, new_value):
        self.display_bar["value"] = math.floor(new_value)
