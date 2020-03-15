class KeyMapper:
    class Key:
        OFF = 0
        ON = 1

        def __init__(self, name, state=OFF):
            self.name = name
            self.state = state

        def toggle(self):
            if self.state == self.ON:
                self.state = self.OFF
            else:
                self.state = self.ON

        def set_on(self):
            self.state = self.ON

        def set_off(self):
            self.state = self.OFF

        @property
        def on(self):
            return self.state == self.ON

        @property
        def off(self):
            return self.state == self.OFF

    def __init__(self, app):
        self.up = self.Key("up")
        self.down = self.Key("down")
        self.left = self.Key("left")
        self.right = self.Key("right")
        self.shoot = self.Key("shoot")

        app.accept("w", self.up.set_on)
        app.accept("w-up", self.up.set_off)
        app.accept("s", self.down.set_on)
        app.accept("s-up", self.down.set_off)
        app.accept("a", self.left.set_on)
        app.accept("a-up", self.left.set_off)
        app.accept("d", self.right.set_on)
        app.accept("d-up", self.right.set_off)
        app.accept("mouse1", self.shoot.set_on)
        app.accept("mouse1-up", self.shoot.set_off)
