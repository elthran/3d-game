import pytest

from importlib import import_module

def test_basic_game_load():
    import sys
    main = import_module('main')
    Game = main.Game
    assert Game() is not None
