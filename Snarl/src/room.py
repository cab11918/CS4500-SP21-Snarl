class Room:
    position = (-1, -1)
    width = -1
    height = -1
    non_wall_tiles = []
    doors = []

    def __init__(self, position, width, height, non_wall_tiles, doors):
        """The room class which represent a room by storing its Cartesian position, dimensions, floor tiles and doors.

        Arguments:
            position(x,y): the x,y coordinate from the upper left corner of the room.
            width(int): the width dimension of the room.
            height(int): the height dimension of the room.
            non_wall_tiles([(x,y),...]): all the coordinates of tiles that are not wall in this room dimension.
            doors([(x,y)),...]): all the doors of the room.
        """
        self.position = position
        self.width = width
        self.height = height
        self.non_wall_tiles = non_wall_tiles
        self.doors = doors
