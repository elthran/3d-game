class TestGame:
    def test_init(self, game_instance):
        assert game_instance is not None

    def test_start_game_with_Warrior(self, game_instance):
        assert game_instance.start_game('Warrior') is None

    def test_update_with_Warrior(self, game_instance):
        game_instance.start_game('Warrior')
        assert game_instance.update(game_instance.updateTask) is not None

