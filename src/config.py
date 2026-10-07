import json
from pydantic import BaseModel
import os



def json_gen() -> None:
    """
    generate Json test file
    """
    result: dict = {}
    result['highscore_filename'] = "hello.json"
    result['level'] = [{"width": 5, "length": 5}, 
                       {"width": 10, "length": 10},
                       {"width": 15, "length": 15},
                       {"width": 20, "length": 20},
                       {"width": 25, "length": 25},
                       {"width": 30, "length": 30}]
    result['lives'] = 3
    result['pacgum'] = 42
    result['points_per_pacgum'] = 10
    result['points_per_super_pacgum'] = 50
    result['points_per_ghost'] = 200
    result['seed'] = 42
    result['level_max_time'] = 90
    data_path: str = os.path.dirname(os.getcwd()) + '/data/'
    with open(data_path + "config.json", "w" ) as f:
        json.dump(result, f, indent=2)


class Config(BaseModel):
    
    @staticmethod
    def parse(filename: str) -> dict:
        """
        get dict from config file, ignore #, /**/, //
        """
        data_path: str = os.path.dirname(os.getcwd()) + '/data/'
        lines: list = []
        file_path: str = data_path + filename
        with open(file_path, "r") as f:
            for line in f:
                if line.lstrip().startswith("#") or line.lstrip().startswith("/*") or line.lstrip().startswith("//"):
                    continue
                if "/*" in line:
                    start: int = line.find("/*")
                    end: int = line.find("*/", start)
                    if end != -1:
                        k: str = line[0:start] + line[(end+2):-1]
                        line = k
                if "//" in line:
                    start: int = line.find("//")
                    k = line[0:start]
                    line = k
                lines.append(line)
        return(json.loads("".join(lines)))

Config.parse("config.json")