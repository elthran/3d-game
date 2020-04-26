import pytest
from panda3d.core import loadPrcFileData

from importlib import import_module


import os

TESTS_CONFIG_PRC = """
model-path {main_dir}/resources/models
"""


@pytest.fixture(scope="session")
def game_instance():
    main = import_module('main')

    # hack patch model path
    main_dir = os.path.dirname(main.__file__)
    loadPrcFileData(name='tests_Config.pry', data=TESTS_CONFIG_PRC.format(main_dir=main_dir))

    game = main.Game()
    return game


@pytest.fixture(scope="function")
def started_game(game_instance):
    # Do we need this?
    # game_instance.state.set_next(States.RUNNING)
    yield game_instance
