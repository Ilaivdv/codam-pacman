import os
try:
    from src import start_game
except ModuleNotFoundError:
    print(("ERROR: missing dependencies! "
           "install them using make install "
           "and run the program through .venv"))
else:
    if __name__ == "__main__":
        config_path: str = "config.json"
        try:
            if not os.path.exists(config_path):
                raise ValueError(
                        f"Error: {config_path} is not a valid config file")
            elif not os.access(config_path, os.R_OK):
                raise ValueError(
                        f"Error: no permission to read file at path {config_path}")
        except ValueError as e:
            print(e)
        else:
            start_game(config_path)
