from app.config.initializers.game import *

# NOTE render is some kind of implict global defined by
# instantiating the game object.
main_light = DirectionalLight("main light")
game.main_light_node_path = render.attachNewNode(main_light)
game.main_light_node_path.setHpr(45, -45, 0)
render.setLight(game.main_light_node_path)

ambient_light = AmbientLight("ambient light")
ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
game.ambient_light_node_path = render.attachNewNode(ambient_light)
render.setLight(game.ambient_light_node_path)

render.setShaderAuto()
