from app.objects.interfaces import Command


class ToolBelt:
    def __init__(self):
        self.tools = {}

    def add_action(self, name, command_instance, operation):
        self.tools[name] = [command_instance, operation]

    def execute(self, keys, hero, time_delta):
        for key in keys:
            command_instance, operation = self.tools[key.name]
            command_instance.update(operation, key, hero, time_delta)


class NullCommand(Command):
    def __init__(self):
        pass

    def update(self, operation, key, hero, time_delta):
        pass
