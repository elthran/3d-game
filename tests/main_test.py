from app.game.constants import States


class TestGame:
    def test_init(self, game_instance):
        assert game_instance is not None

    def test_start_game_with_Warrior(self, game_instance):
        assert game_instance.start_game('Warrior') is None

    def test_update_with_Warrior(self, game_instance):
        game_instance.current_menu.hide_menu()
        game_instance.start_game('Warrior')
        game_instance.state.set_next(States.RUNNING)
        assert game_instance.update(game_instance.current_task) is not None

