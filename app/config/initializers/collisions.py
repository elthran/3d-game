from app.config.initializers.game import *

game.pusher = CollisionHandlerPusher()
game.cTrav = CollisionTraverser()

game.pusher.setHorizontal(True)

game.pusher.add_in_pattern("%fn-into-%in")

game.collision_controller = CollisionController(game)

