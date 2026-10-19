from pydantic import BaseModel
from typing import Any
import json
import os
from .error import ConfigError


class Config(BaseModel):

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
                    'level': [
                        {"width": 5, "length": 5},
                        {"width": 10, "length": 10},
                        {"width": 15, "length": 15},
                        {"width": 20, "length": 20},
                        {"width": 25, "length": 25},
                        {"width": 30, "length": 30}],
                    'lives': 3, 'pacgum': 42,
                    'points_per_pacgum': 10,
                    'points_per_super_pacgum': 50,
                    'points_per_ghost': 200,
                    'seed': 42,
                    'level_max_time': 90
                }
        for key in game_set.keys():
            if key in config_dict.keys():
                game_set[key] = config_dict[key]
            else:
                notification.append("NOTICE: Missing KEY in config.json,"
                                    f"using a default value: {key}")
        if notification:
            game_set["notification"] = notification
        else:
            game_set["notification"] = None
        return game_set

    @staticmethod
    def parse_highscore() -> Any:
        file_path: str = os.path.expanduser("~/.local/share/highscore.json")
        if os.path.isfile(file_path):
            if os.stat(file_path).st_size == 0:
                return {}
            try:
                with open(file_path, "r") as f:
                    highscore_dict: Any = json.load(f)
            except ConfigError as e:
                print(e)
            return (dict(sorted(highscore_dict.items(), key=lambda x: x[1],
                         reverse=True)))
        else:
            with open(file_path, 'w') as f:
                pass
            return {}
