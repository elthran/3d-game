from app.game.interfaces import Command


class Walk(Command):
    OFF = 1

    def __init__(self, max_states):
        self.operations = []
        self.states_seen = 0
        self.max_states = max_states

    def up(self, hero, time_delta):
        hero.velocity.addY(hero.acceleration * time_delta)
        hero.walking = True

    def down(self, hero, time_delta):
        hero.velocity.addY(-hero.acceleration * time_delta)
        hero.walking = True

    def left(self, hero, time_delta):
        hero.velocity.addX(-hero.acceleration * time_delta)
        hero.walking = True

    def right(self, hero, time_delta):
        hero.velocity.addX(hero.acceleration * time_delta)
        hero.walking = True

    def update(self, operation, key, hero, time_delta):
        self.states_seen += 1
        if key.on:
            self.operations.append(operation)

        if self.states_seen == self.max_states:
            self.states_seen = 0
            hero.walking = False
            for method in self.operations:
                method(hero, time_delta)

            self.operations = []
            if hero.walking == False:
                self.stop(hero)

    def stop(self, hero):
        hero.walking = False
        stand_control = hero.actor.getAnimControl("stand")
        if not stand_control.isPlaying():
            hero.actor.stop("walk")
            hero.actor.loop("stand")
