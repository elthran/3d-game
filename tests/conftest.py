import pytest

from importlib import import_module


@pytest.fixture(scope="session")
def game_instance():
    main = import_module('main')
    Game = main.Game
    return Game()
