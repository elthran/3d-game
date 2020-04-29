from app.game.constants import States
from app.game.interfaces import Command
from app.objects.menus.attribute_point_select import AttributePointSelect


class AttributeMenuCommand(Command):
    def __init__(self, game=None):
        self.game = game
        self.menu = AttributePointSelect(self.game)

    def tool_belt_update(self, game, operation, key, hero, time_delta):
        if key.on and key.has_changed:
            if self.game.state.current == States.RUNNING:
                self.game.state.set_next(States.MENU)
                self.menu.enter_menu(hero=hero)
            elif self.game.state.current == States.MENU:
                print("triggered")
                self.menu.exit_menu()
