import pytest

from importlib import import_module


@pytest.fixture(scope="session")
def game_instance():
    main = import_module('main')
    Game = main.Game
    return Game()


@pytest.fixture(scope="function")
def started_game(game_instance):
    game_instance.game_started = True
    yield game_instance
    game_instance.game_started = False
