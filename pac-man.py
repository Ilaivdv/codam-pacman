try:
    from src import start_game
except ModuleNotFoundError:
    print(("ERROR: missing modules! "
           "install dependencies using make install "
           "and run the program through .venv"))
else:
    if __name__ == "__main__":
        start_game()
