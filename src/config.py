import json
from pydantic import BaseModel
import re

def json_gen() -> None:
    """
    generate Json test file
    """
    result: dict = {}
    result['highscore_filename'] = "hello.json"
    level: dict = {
        "1": (5, 5),
        "2": (10,10),
        "3": (15, 15)
    }
    result['level'] = "2"
    x, y = level[result['level']]
    result['width'] = x
    result['length'] = y
    result['lives'] = 3
    result['pacgum'] = 42
    result['points_per_pacgum'] = 10
    result['points_per_super_pacgum'] = 50
    result['points_per_ghost'] = 200
    result['seed'] = 42
    result['level_max_time'] = 90
    with open("config.json", "w" ) as f:
        json.dump(result, f, indent=2)


class Config(BaseModel):
    
    @staticmethod
    def parse(file_path: str) -> dict:
        """
        get dict from config file, ignore #, /**/, //
        """
        lines: list = []
        with open(file_path, "r") as f:
            for line in f:
                if line.lstrip().startswith("#") or line.lstrip().startswith("/*") or line.lstrip().startswith("//"):
                    continue
                lines.append(line)
        print(json.loads("".join(lines)))
        return(json.loads("".join(lines)))

Config.parse("config.json")