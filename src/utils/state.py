from abc import ABC, abstractmethod
from typing import Any


class State(ABC):
    """ An abstract State class. """

    def __init__(self, parent: Any) -> None:
        """
        Initializes State.

        Args:
            parent: State's parent.
        """

        self.parent: Any = parent

    @abstractmethod
    def on_enter(self) -> None:
        """ Handle events when state just entered. """
        pass

    @abstractmethod
    def state_process(self) -> None:
        """ Handle events for current state. """
        pass

    def __str__(self) -> str:
        """ Returns the name of State's parent class. """
        return self.__class__.__name__
