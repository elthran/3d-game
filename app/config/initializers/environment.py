from app.config.initializers.game import *

# TODO: pick a better name for this file.
game.environment = loader.loadModel("Models/Misc/environment")
game.environment.reparentTo(render)
