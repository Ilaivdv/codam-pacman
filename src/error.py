
class PacmanError(Exception):
    """Base exception for the Pac-Man project."""


class AssetLoadError(PacmanError):
    """An asset is missing or invalid."""


class ConfigError(PacmanError):
    """An error occurred while loading or validating config."""


class GameError(PacmanError):
    """An error occurred in game logic."""


class UiError(PacmanError):
    """An error occurred in the UI."""


class HighscoreError(PacmanError):
    """An error occurred while handling high scores."""
