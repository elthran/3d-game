class KeyMap:
    @classmethod
    def initialize(cls, app):
        cls(app)

    def __init__(self, app):
        self.app = app

        self.app.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False
        }

        self.app.accept("w", self.updateKeyMap, ["up", True])
        self.app.accept("w-up", self.updateKeyMap, ["up", False])
        self.app.accept("s", self.updateKeyMap, ["down", True])
        self.app.accept("s-up", self.updateKeyMap, ["down", False])
        self.app.accept("a", self.updateKeyMap, ["left", True])
        self.app.accept("a-up", self.updateKeyMap, ["left", False])
        self.app.accept("d", self.updateKeyMap, ["right", True])
        self.app.accept("d-up", self.updateKeyMap, ["right", False])
        self.app.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.app.accept("mouse1-up", self.updateKeyMap, ["shoot", False])

    def updateKeyMap(self, controlName, controlState):
        self.app.keyMap[controlName] = controlState
