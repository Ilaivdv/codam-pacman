from pydantic import BaseModel
from typing import Any
import json
import os


class Config(BaseModel):
    @staticmethod
    def parse(filename: str) -> dict[str, Any]:
        """
        Get dict from config file, ignore #, /**/, //

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
        return dict(json.loads("".join(lines)))
