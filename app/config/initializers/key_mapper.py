class Keys:
    W = "w"
    S = "s"
    A = "a"
    D = "d"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    MOUSE_ONE = "mouse_one"

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


    @classmethod
    def initialize(cls, app):
        return cls(app)

    def __init__(self, app):
        self.w = self.Key(Keys.W)
        self.s = self.Key(Keys.S)
        self.a = self.Key(Keys.A)
        self.d = self.Key(Keys.D)
        self.mouse_one = self.Key(Keys.MOUSE_ONE)

        app.accept("w", self.w.set_on)
        app.accept("w-up", self.w.set_off)
        app.accept("s", self.s.set_on)
        app.accept("s-up", self.s.set_off)
        app.accept("a", self.a.set_on)
        app.accept("a-up", self.a.set_off)
        app.accept("d", self.d.set_on)
        app.accept("d-up", self.d.set_off)
        app.accept("mouse1", self.mouse_one.set_on)
        app.accept("mouse1-up", self.mouse_one.set_off)


    def __iter__(self):
        return iter(vars(self).values())
