from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    @abstractmethod
    def update(self, player_pos, vis_board):
        """Takes a state representation designed by our team and render all the components as a graphical interface by
        using Pygame.

        Arguments:
            player_pos: the current position of the player.
            vis_board: the vision of the given player which is a 2D array of Tiles.

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

    @abstractmethod
    def move(self):
        """Takes a position given from the model and call the components in the game model to handle the given move.

        Returns:
            None
        """
        pass
