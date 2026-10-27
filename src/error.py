class PacmanError(Exception):
    """ Base exception for the Pac-Man project. """


class ConfigError(PacmanError):
    """ Exception for loading or validation of config. """


class HighscoreError(PacmanError):
    """ Exception for handling high scores. """
