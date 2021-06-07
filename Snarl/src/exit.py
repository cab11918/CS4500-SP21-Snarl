class Exit:
    position = (-1, -1)
    exit_unlocked = False

    """
    This is a a class to represent the Exit object in our game state.
    """

    def __init__(self, position):
        self.position = position
