import sys
import os
try:
    from src import start_game
except ModuleNotFoundError:
    print(("ERROR: missing dependencies! "
           "install them using make install "
           "and run the program through .venv"))
else:
    if __name__ == "__main__":
        try:
            if len(sys.argv) != 2:
                raise ValueError("Error: Too many arguments!")
            if not os.path.exists(sys.argv[1]):
                raise ValueError(
                        f"Error: {sys.argv[1]} is not a valid config file")
            elif not os.access(sys.argv[1], os.R_OK):
                raise ValueError(
                        f"Error: no permission to read file at path {sys.argv[1]}")
        except ValueError as e:
            print(e)
        else:
            start_game(sys.argv[1])
