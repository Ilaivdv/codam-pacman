"""
Entry point for the game.
Validates config, falls back to default values on invalid keys.
"""
try:
    from src import start_game
    import os
    import sys
except ModuleNotFoundError as e:
    print(f"Missing modules! Please run the program through uv.\nError: {e}")
else:
    if __name__ == "__main__":
        try:
            assert len(sys.argv) == 2
        except AssertionError:
            print(("Error: Invalid arguments given, "
                   "please give a name ending in .json"))
            sys.exit(1)
        config_path: str = sys.argv[1]
        try:
            if not os.path.exists(config_path):
                raise ValueError(
                        f"Error: {config_path} is not a valid config file")
            elif not os.access(config_path, os.R_OK):
                raise ValueError(
                        ("Error: no permission to read "
                         f"file at path {config_path}"))
        except ValueError as e:
            print(e)
        else:
            try:
                start_game(config_path)
            except ModuleNotFoundError:
                print(("ERROR: missing dependencies! "
                       "install them using make install "
                       "and run the program through .venv"))
