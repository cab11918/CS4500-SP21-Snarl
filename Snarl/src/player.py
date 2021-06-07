import uuid


class Player:
    player_id = -999
    player_name = None
    avatar = None
    position = None
    expelled = False
    is_movable = False
    vision = [[]]
    destination = None

    def __init__(self, player_id, player_name):
        """
        The Player class is a representation of the user who is interacting with the game. It stores the information
        needed for the user and update them according to Game Manager.

        Arguments:
            player_id (int): The unique identifier for the Player, it will be used when the fields were updated by
            Game Manager.
            player_name (String): A unique text representation of the Player's identity when playing the game.

        Returns: None

        Throws: None
        """
        self.player_id = player_id
        self.player_name = player_name
