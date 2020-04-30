from app.game.constants import Keys


class KeyMapper:
    class Key:
        OFF = 0
        ON = 1

        def __init__(self, name, state=OFF):
            self.name = name
            self.old_state = state
            self.state = state

        @property
        def has_changed(self):
            return self.old_state != self.state

        @property
        def on(self):
            return self.state == self.ON

        @property
        def off(self):
            return self.state == self.OFF

        def update_old_state(self):
            self.old_state = self.state

        def toggle(self):
            if self.state == self.ON:
                self.state = self.OFF
            else:
                self.state = self.ON

        def set_on(self):
            self.state = self.ON

        def set_off(self):
            self.state = self.OFF

    @classmethod
    def initialize(cls, app):
        return cls(app)

    def __init__(self, app):
        self.a = self.Key(Keys.A)
        self.b = self.Key(Keys.B)
        self.c = self.Key(Keys.C)
        self.d = self.Key(Keys.D)
        self.e = self.Key(Keys.E)
        self.f = self.Key(Keys.F)
        self.g = self.Key(Keys.G)
        self.h = self.Key(Keys.H)
        self.i = self.Key(Keys.I)
        self.j = self.Key(Keys.J)
        self.k = self.Key(Keys.K)
        self.l = self.Key(Keys.L)
        self.m = self.Key(Keys.M)
        self.n = self.Key(Keys.N)
        self.o = self.Key(Keys.O)
        self.p = self.Key(Keys.P)
        self.q = self.Key(Keys.Q)
        self.r = self.Key(Keys.R)
        self.s = self.Key(Keys.S)
        self.t = self.Key(Keys.T)
        self.u = self.Key(Keys.U)
        self.v = self.Key(Keys.V)
        self.w = self.Key(Keys.W)
        self.x = self.Key(Keys.X)
        self.y = self.Key(Keys.Y)
        self.z = self.Key(Keys.Z)
        self.escape = self.Key(Keys.ESCAPE)
        self.mouse_left = self.Key(Keys.MOUSE_LEFT)
        self.mouse_right = self.Key(Keys.MOUSE_RIGHT)

        app.accept("a", self.a.set_on)
        app.accept("a-up", self.a.set_off)
        app.accept("b", self.b.set_on)
        app.accept("b-up", self.b.set_off)
        app.accept("c", self.c.set_on)
        app.accept("c-up", self.c.set_off)
        app.accept("d", self.d.set_on)
        app.accept("d-up", self.d.set_off)
        app.accept("e", self.e.set_on)
        app.accept("e-up", self.e.set_off)
        app.accept("f", self.f.set_on)
        app.accept("f-up", self.f.set_off)
        app.accept("g", self.g.set_on)
        app.accept("g-up", self.g.set_off)
        app.accept("h", self.h.set_on)
        app.accept("h-up", self.h.set_off)
        app.accept("i", self.i.set_on)
        app.accept("i-up", self.i.set_off)
        app.accept("j", self.j.set_on)
        app.accept("j-up", self.j.set_off)
        app.accept("k", self.k.set_on)
        app.accept("k-up", self.k.set_off)
        app.accept("l", self.l.set_on)
        app.accept("l-up", self.l.set_off)
        app.accept("m", self.m.set_on)
        app.accept("m-up", self.m.set_off)
        app.accept("n", self.n.set_on)
        app.accept("n-up", self.n.set_off)
        app.accept("o", self.o.set_on)
        app.accept("o-up", self.o.set_off)
        app.accept("p", self.p.set_on)
        app.accept("p-up", self.p.set_off)
        app.accept("q", self.q.set_on)
        app.accept("q-up", self.q.set_off)
        app.accept("r", self.r.set_on)
        app.accept("r-up", self.r.set_off)
        app.accept("s", self.s.set_on)
        app.accept("s-up", self.s.set_off)
        app.accept("t", self.t.set_on)
        app.accept("t-up", self.t.set_off)
        app.accept("u", self.u.set_on)
        app.accept("u-up", self.u.set_off)
        app.accept("v", self.v.set_on)
        app.accept("v-up", self.v.set_off)
        app.accept("w", self.w.set_on)
        app.accept("w-up", self.w.set_off)
        app.accept("x", self.x.set_on)
        app.accept("x-up", self.x.set_off)
        app.accept("y", self.y.set_on)
        app.accept("y-up", self.y.set_off)
        app.accept("z", self.z.set_on)
        app.accept("z-up", self.z.set_off)
        app.accept("escape", self.escape.set_on)
        app.accept("escape-up", self.escape.set_off)
        app.accept("mouse1", self.mouse_left.set_on)
        app.accept("mouse1-up", self.mouse_left.set_off)
        app.accept("mouse3", self.mouse_right.set_on)
        app.accept("mouse3-up", self.mouse_right.set_off)

    def __iter__(self):
        return iter(vars(self).values())
