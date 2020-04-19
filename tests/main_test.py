import pytest


def test_basic_game_load(game_instance):
    assert game_instance is not None


def test_update(mocker, game_instance):
    task_mock = "<class 'panda3d.core.PythonTask'>"
    assert game_instance.update(task_mock) is not None
