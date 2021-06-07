class Tile:
    tile_type = None
    occupied_by = []

    def __init__(self, tile_type, occupied_by):
        """The Tile class which represent a tile in the level by storing the array of objects that was occupied and the
        type of the tiles can be 'wall', 'floor','hallway', 'door' ,and 'void'.

        Arguments:
            tile_type(str): the type of the tile. It can be wall, floor, hallway, or door.
            occupied_by([Player | Adversary]): an array of objects that is currently on the tile.
        """
        self.tile_type = tile_type
        self.occupied_by = occupied_by
