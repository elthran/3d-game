from random import choice

from panda3d.core import Vec3, DirectionalLight, AmbientLight, Vec4, CollisionCapsule, CollisionNode

from app.objects.game_objects.physicals.characters.monsters.melee import Melee


class World:
    def __init__(self, game):
        self.game = game

        background_music = loader.loadMusic("resources/music/background_theme.ogg")
        background_music.setLoop(True)
        # I find this piece to be pretty loud, so I've turned the volume down a lot.
        background_music.setVolume(0.5)
        background_music.play()

        main_light = DirectionalLight("main light")
        self.main_light_node_path = render.attachNewNode(main_light)
        self.main_light_node_path.setHpr(45, -45, 0)
        render.setLight(self.main_light_node_path)

        ambient_light = AmbientLight("ambient light")
        ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambient_light_node_path = render.attachNewNode(ambient_light)
        render.setLight(self.ambient_light_node_path)

        render.setShaderAuto()

        # self.environment = loader.loadModel("Misc/environment")
        # self.environment.reparentTo(render)

        self.walking_enemies = []
        self.deadEnemies = []

        # Set up some monster spawn points
        self.spawn_time = 5
        self.spawn_timer = 1
        self.maximum_walking_enemies = 2
        self.spawn_points = []
        number_points_per_wall = 5
        for i in range(number_points_per_wall):
            coord = 7.0 / number_points_per_wall + 0.5
            self.spawn_points.append(Vec3(-7.0, coord, 0))
            self.spawn_points.append(Vec3(7.0, coord, 0))
            self.spawn_points.append(Vec3(coord, -7.0, 0))
            self.spawn_points.append(Vec3(coord, 7.0, 0))

        self.generate_walls()

    def generate_walls(self):
        wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setY(8.0)

        wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setY(-8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setX(8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setX(-8.0)

    def spawn_enemy(self):
        spawn_point = choice(self.spawn_points)
        new_enemy = Melee(starting_position=spawn_point)
        self.walking_enemies.append(new_enemy)

    def update(self, time_delta):
        self.spawn_timer -= time_delta
        if self.spawn_timer <= 0 and len(self.walking_enemies) < self.game.hero.level:
            self.spawn_timer = self.spawn_time / self.game.hero.level
            self.spawn_enemy()

        [walking_enemy.update(time_delta, hero=self.game.hero) for walking_enemy in self.walking_enemies]

        self.walking_enemies = [enemy for enemy in self.walking_enemies if not enemy.dead]

    def cleanup(self):
        for walking_enemy in self.walking_enemies:
            walking_enemy.remove_object_from_world()
