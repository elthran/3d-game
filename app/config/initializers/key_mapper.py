from app.objects.constants import Keys


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
        self.mouse_left = self.Key(Keys.MOUSE_LEFT)
        self.mouse_right = self.Key(Keys.MOUSE_RIGHT)

        app.accept("w", self.w.set_on)
        app.accept("w-up", self.w.set_off)
        app.accept("s", self.s.set_on)
        app.accept("s-up", self.s.set_off)
        app.accept("a", self.a.set_on)
        app.accept("a-up", self.a.set_off)
        app.accept("d", self.d.set_on)
        app.accept("d-up", self.d.set_off)
        app.accept("mouse1", self.mouse_left.set_on)
        app.accept("mouse1-up", self.mouse_left.set_off)
        app.accept("mouse3", self.mouse_right.set_on)
        app.accept("mouse3-up", self.mouse_right.set_off)

    def __iter__(self):
        return iter(vars(self).values())
