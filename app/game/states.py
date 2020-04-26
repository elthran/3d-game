from app.objects.constants import States


class GameState:
    def __init__(self, current=None, game=None):
        self.current = current
        self.game = game

    def set_next(self, next_state):
        self.current = next_state
        if next_state == States.MENU:
            self.game.pause()
        elif next_state == States.RUNNING:
            self.game.resume()
        elif next_state == States.QUIT:
            self.game.quit()
