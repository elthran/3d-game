from app.config.initializers.direct import *
from app.config.initializers.panda3d import *
from app.components import *


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)


loadPrcFile('app/config/Config.prc')
game = Game()
