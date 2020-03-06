class KeyMap:
    @classmethod
    def initialize(cls, app):
        cls(app)

    def __init__(self, app):
        self.app = app

        self.key_map = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False
        }

        self.app.accept("w", self.update_key_map, ["up", True])
        self.app.accept("w-up", self.update_key_map, ["up", False])
        self.app.accept("s", self.update_key_map, ["down", True])
        self.app.accept("s-up", self.update_key_map, ["down", False])
        self.app.accept("a", self.update_key_map, ["left", True])
        self.app.accept("a-up", self.update_key_map, ["left", False])
        self.app.accept("d", self.update_key_map, ["right", True])
        self.app.accept("d-up", self.update_key_map, ["right", False])
        self.app.accept("mouse1", self.update_key_map, ["shoot", True])
        self.app.accept("mouse1-up", self.update_key_map, ["shoot", False])

        self.app.key_map = self.key_map

    def update_key_map(self, controlName, controlState):
        self.key_map[controlName] = controlState
