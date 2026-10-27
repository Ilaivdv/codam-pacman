import pytest  # noqa
from src.config import Config


def test_normal() -> None:
    assert Config.parse("tests/normal.json") == {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': []
                }


def test_missing_lives() -> None:
    assert Config.parse("tests/missing_lives.json") == {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': [
                        'NOTICE: Missing KEY in config file,using a default'
                        ' value: lives(3)',
                    ],
                }


def test_file_not_exist() -> None:
    assert Config.parse("tests/file_not_exist.json") == {
                    'highscore_filename': "m.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': []
                }


def test_level_minus() -> None:
    assert Config.parse("tests/level_minus.json") == {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': [
                        'NOTICE: Invalid VALUE in config file,using a default'
                        ' value: level(-1 -> 10)',
                    ]
                }


def test_size_not_good() -> None:
    assert Config.parse("tests/size_not_good.json") == {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': [
                        'NOTICE: Using a default size(15x15), wrong width'
                        ' value in config file: 10 -> 15',
                        'NOTICE: Using a default size(15x15), wrong height'
                        ' value in config file: 10 -> 15',
                    ]
                }


def test_size_minus() -> None:
    assert Config.parse("tests/size_minus.json") == {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': [
                        'NOTICE: Using a default size(15x15), wrong width '
                        'value in config file: -10 -> 15',
                        'NOTICE: Using a default size(15x15), wrong height '
                        'value in config file: -10 -> 15',
                    ]
                }


def test_pacgum_minus() -> None:
    assert Config.parse("tests/pacgum_minus.json") == {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': [
                        'NOTICE: Invalid VALUE in config file,using a '
                        'default value: pacgum(-42 -> 42)',
                    ]
                }


def test_json_with_comments() -> None:
    assert Config.parse("tests/json_with_comments.json") == {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90,
                    'notification': []
                }
