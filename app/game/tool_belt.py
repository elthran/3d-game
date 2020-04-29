from app.game.constants import Graphics
from app.game.interfaces import Command


class ToolBelt:
    def __init__(self, game=None, key_mapper=None):
        self.game = game
        self.key_mapper = key_mapper
        self.hero = None
        self.tools = {}

    def set_hero(self, hero):
        self.hero = hero

    def update(self, task):
        if self.hero:
            time_delta = min(globalClock.getDt(), Graphics.MAX_FRAME_RATE)
            self.execute(self.key_mapper, self.hero, time_delta)
        return task.cont

    def add_action(self, name, command_instance, operation):
        self.tools[name] = [command_instance, operation]

    def execute(self, keys, hero, time_delta):
        for key in keys:
            try:
                command_instance, operation = self.tools[key.name]
            except KeyError:
                continue

            command_instance.tool_belt_update(self.game, operation, key, hero, time_delta)
            key.update_old_state()


class NullCommand(Command):
    def __init__(self):
        pass

    def tool_belt_update(self, game, operation, key, hero, time_delta):
        pass
