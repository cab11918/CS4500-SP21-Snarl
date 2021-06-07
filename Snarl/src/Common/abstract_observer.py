from abc import ABC, abstractmethod


class AbstractObserver(ABC):
    @abstractmethod
    def update(self):
        """Takes a state representation designed by our team and render all the components as a graphical interface by
        using Pygame.
        Returns:
            None
        """
        pass

    @abstractmethod
    def open_window(self):
        """Open up a Pygame window and render all the informtion that was currently stored in the GUI model.
        Returns:
            None
        """
        pass
