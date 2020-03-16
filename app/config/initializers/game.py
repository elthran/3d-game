import builtins

from app.config.initializers.direct import *
from app.config.initializers.panda3d import *
from app.config.initializers.math import *

from app.components import *
from app.models import *
from app.controllers import *


insert_into_global_namespace(builtins, locals())


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)


loadPrcFile('app/config/Config.prc')
game = Game()
