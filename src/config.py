from .error import ConfigError
from pydantic import BaseModel
from typing import Any
import json
import os


class Config(BaseModel):
    """
    This is the config validator class, reads required files
    for configuration and score saving and falls back to defaults on any
    missing/invalid keys
    """

    @staticmethod
    def parse(filename: str) -> dict[str, Any]:
        """
        Get dict from config file, ignore #, /**/, //
        checking the keys and fill in default value

        Args:
            filename: The relative file path to config json file

        Returns:
            The config as a dictionary.
        """

        data_path: str = os.path.dirname(os.getcwd() + "/")
        lines: list[str] = []
        file_path: str = data_path + "/" + filename
        with open(file_path, "r") as f:
            for line in f:
                if line.lstrip().startswith("#") or \
                        line.lstrip().startswith("/*") or \
                        line.lstrip().startswith("//"):
                    continue
                if "/*" in line:
                    start = line.find("/*")
                    end = line.find("*/", start)
                    if end != -1:
                        k: str = line[0:start] + line[(end+2):-1]
                        line = k
                if "//" in line:
                    start = line.find("//")
                    k = line[0:start]
                    line = k
                lines.append(line)
        config_dict: dict[str, Any] = dict(json.loads("".join(lines)))
        notification: list[str] = []
        game_set: dict[str, Any] = {
                    'highscore_filename': "highscore.json",
                    "level": 10,
                    "width": 15,
                    "height": 15,
                    "lives": 3, "pacgum": 42,
                    "points_per_pacgum": 10,
                    "points_per_super_pacgum": 50,
                    "points_per_ghost": 200,
                    "seed": 42,
                    "level_max_time": 120
                }
        for key in game_set.keys():
            if key in config_dict.keys():
                if ((key == "width" or key == "height")
                   and (config_dict[key] > 20 or config_dict[key] <= 10)):
                    notification.append(("NOTICE: Using a default size(15"
                                         f"x15), wrong {key} value in config "
                                         f"file: {config_dict[key]} -> "
                                         f"{game_set[key]}"))
                    game_set[key] = 15
                elif (key in ["lives", "level", "pacgum"] or "points" in key
                      or "time" in key):
                    if key == "level" and config_dict[key] < 10:
                        notification.append(("NOTICE: Game need at least 10 "
                                             "levels, using a default value:"
                                             f" {key}({config_dict[key]} -> "
                                             f"{game_set[key]})"))
                    elif key == "lives" and config_dict[key] > 10:
                        notification.append(("NOTICE: Game has too many lives,"
                                             " using a default value:"
                                             f" {key}({config_dict[key]} -> "
                                             f"{game_set[key]})"))
                    elif config_dict[key] <= 0 or config_dict[key] >= 500:
                        notification.append(("NOTICE: Invalid VALUE in config "
                                             "file, using a default value:"
                                             f" {key}({config_dict[key]} -> "
                                             f"{game_set[key]})"))
                    else:
                        game_set.update({key: config_dict[key]})
                else:
                    game_set.update({key: config_dict[key]})
            else:
                notification.append(("NOTICE: Missing KEY in config file,"
                                     " using a default value: "
                                     f"{key}({game_set[key]})"))
        if notification:
            game_set["notification"] = notification
        else:
            game_set["notification"] = []
        return game_set

    @staticmethod
    def parse_highscore() -> Any:
        """
        Parses/creates highscore json file in user's directory.

        Returns:
            Any - Parsed json file or empty dict
        """

        from .game import settings
        assert settings is not None
        filename: str = settings.highscore_filename
        path: str = "".join(["~/.local/share/", filename])
        file_path: str = os.path.expanduser(path)
        if os.path.isfile(file_path):
            if os.stat(file_path).st_size == 0:
                return {}
            try:
                with open(file_path, "r") as f:
                    highscore_dict: Any = json.load(f)
            except ConfigError as e:
                print(e)
            else:
                if len(highscore_dict) == 1:
                    return highscore_dict
                else:
                    return (dict(sorted(highscore_dict.items(),
                                        key=lambda x: x[1],
                                        reverse=True)[:10]))
        else:
            with open(file_path, 'w') as f:
                pass
            return {}
