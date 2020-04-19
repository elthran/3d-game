import pytest

class TestGame:
    def test_init(game_instance):
        assert game_instance is not None


    def test_start_game_with_Warrior(game_instance):
        assert game_instance.start_game('Warrior')


    def test_update_with_Warrior(mocker, game_instance):
        game_instance.start_game('Warrior')
        assert started_game.update(started_game.updateTask) is not None

