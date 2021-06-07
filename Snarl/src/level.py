#! /usr/bin/python3
class Level:
    rooms = []
    hallways = []
    key_pos = (-1, -1)
    exit_pos = (-1, -1)

    def __init__(self, rooms, hallways, key_pos, exit_pos):
        """The Level class which represent a level by storing the list of rooms and a list of hallways.

        Arguments:
            rooms([Room,...]): the list of all rooms in this level.
            hallways([Hallway,...]): the list of all hallways in this level.
            key_pos(Key): the position of the Key
            exit_pos(Exit): the position of the Exit
        """
        self.rooms = rooms
        self.hallways = hallways
        self.key_pos = key_pos
        self.exit_pos = exit_pos
