from app.config.initializers.game import *

game.pusher = CollisionHandlerPusher()
game.cTrav = CollisionTraverser()

game.pusher.setHorizontal(True)

game.pusher.add_in_pattern("%fn-into-%in")

game.collision_controller = CollisionController(game)

wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
wallNode = CollisionNode("Wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setY(8.0)

wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
wallNode = CollisionNode("Wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setY(-8.0)

wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
wallNode = CollisionNode("Wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setX(8.0)

wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
wallNode = CollisionNode("Wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setX(-8.0)
