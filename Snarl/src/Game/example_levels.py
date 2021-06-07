#! /usr/bin/python3
import sys
import PySimpleGUI as sg
from Snarl.src.hallway import Hallway
from Snarl.src.room import Room
from Snarl.src.tile import Tile


def render_level(level):
    """Takes a level representation designed by our team and render all the components as a graphical interface by
    using PySimpleGUI.

    Arguments:
        level(Level): a level representation which contains rooms and hallways.

    Returns:
        None
    """

    # variables used to store all x y dimensions and generate the 2D array of the whole level
    all_x = []
    all_y = []
    all_wps_x = [0]
    all_wps_y = [0]

    for room in level.rooms:
        all_x.append(room.position.x + room.width - 1)
        all_y.append(room.position.y + room.height - 1)

    for hallway in level.hallways:
        for point in hallway.waypoints:
            all_wps_x.append(point.x)
            all_wps_y.append(point.y)

    board_col = max(max(all_x), max(all_wps_x)) + 1
    board_row = max(max(all_y), max(all_wps_y)) + 1

    # the 2D array generated by using the given size calculated
    board = [[None for i in range(board_col)] for j in range(board_row)]

    def render_hallway(tile1, tile2):
        """Takes two tiles in a same row or same column and render all the tiles graphically between the given tiles
         on board.

        Arguments:
            tile1(Tile): the start point of the drawing process.
            tile2(Tile): the finish point of the drawing process.

        Returns:
            None

        """

        # the current tile used for drawing, will be updated when one tile drawing process was finished
        temp_tile = Tile(min(tile1.x, tile2.x), min(tile1.y, tile2.y))

        # drawing tiles for the hallway vertically
        if tile1.x == tile2.x:
            for m in range(abs(tile1.y - tile2.y)):
                temp_tile.y += 1
                board[temp_tile.y][temp_tile.x] = sg.Image(filename='resources/hallway.png', size=(20, 20),
                                                           key=(temp_tile.y, temp_tile.x),
                                                           pad=(0, 0))
        # drawing tiles for the hallway vertically
        if tile1.y == tile2.y:
            for n in range(abs(tile1.x - tile2.x)):
                temp_tile.x += 1
                board[temp_tile.y][temp_tile.x] = sg.Image(filename='resources/hallway.png', size=(20, 20),
                                                           key=(temp_tile.y, temp_tile.x),
                                                           pad=(0, 0))

    # use the position of two doors and list of waypoint positions stored in hallway and pass them into the helper
    # function render_hallway
    for hallway in level.hallways:
        d1x = hallway.door1.x
        d1y = hallway.door1.y
        d2x = hallway.door2.x
        d2y = hallway.door2.y

        if len(hallway.waypoints) == 0:
            render_hallway(hallway.door1, hallway.door2)
        else:
            # store the current tile in progress and all the visited tiles
            visited = [Tile(d1x, d1y)]
            current_tile = Tile(d1x, d1y)
            while True:
                for waypoint in hallway.waypoints:
                    if (waypoint.x == current_tile.x or waypoint.y == current_tile.y) and waypoint not in visited:
                        render_hallway(current_tile, waypoint)
                        visited.append(waypoint)
                        current_tile = waypoint
                # once all the waypoints and two doors were visited, end calling the helper function to draw
                if len(visited) > len(hallway.waypoints):
                    render_hallway(current_tile, Tile(d2x, d2y))
                    break

    # draw all the rooms on the board
    for room in level.rooms:
        for tile in room.non_wall_tiles:
            board[tile.y][tile.x] = sg.Image(filename='resources/dirt.png', size=(20, 20), key=(tile.y, tile.x),
                                             pad=(0, 0))
        for door in room.doors:
            board[door.y][door.x] = sg.Image(filename='resources/door.png', size=(20, 20), key=(tile.y, tile.x),
                                             pad=(0, 0))
    # draw all the walls on the board
    for i in range(board_col):
        for j in range(board_row):
            if board[j][i] is None:
                board[j][i] = sg.Image(filename='resources/wall.png', size=(20, 20), key=(j, i),
                                       pad=(0, 0))

    # set the theme and title of the GUI window
    sg.theme('DarkAmber')
    layout = board
    window = sg.Window('Snarl', layout)

    # show the rendered level
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
    window.close()


class Tile:
    def __init__(self, x, y):
        """The Tile class which represent a tile in the level by storing the X, Y position.

        Arguments:
            x(int): the x coordinate of the tile.
            y(int): the y coordinate of the tile.
        """
        self.x = x
        self.y = y


class Level:
    def __init__(self, rooms, hallways):
        """The Level class which represent a level by storing the list of rooms and a list of hallways.

        Arguments:
            rooms([Room,...]): the list of all rooms in this level.
            hallways([Hallway,...]): the list of all hallways in this level.
        """
        self.rooms = rooms
        self.hallways = hallways


# level 1

room1 = Room(Tile(0, 0), 4, 3, [Tile(1, 1), Tile(2, 1)], [Tile(3, 1)])
room2 = Room(Tile(6, 0), 3, 3, [Tile(7, 1)], [Tile(6, 1)])
hallway1 = Hallway(Tile(3, 1), Tile(6, 1), [])
level1 = Level([room1, room2], [hallway1])

# level 2

room3 = Room(Tile(0, 0), 5, 5, [Tile(1, 1), Tile(1, 2), Tile(2, 2), Tile(3, 2), Tile(1, 3), Tile(2, 3), Tile(3, 3)],
             [Tile(0, 1), Tile(1, 4)])
room4 = Room(Tile(6, 0), 4, 5, [Tile(8, 1), Tile(8, 2), Tile(7, 2), Tile(8, 3), Tile(7, 3)], [Tile(9, 1)])
hallway2 = Hallway(Tile(1, 4), Tile(9, 1), [Tile(1, 5), Tile(10, 5), Tile(10, 1)])

level2 = Level([room3, room4], [hallway2])

# level 3

room5 = Room(Tile(12, 0), 3, 4, [Tile(14, 0), Tile(13, 1), Tile(14, 1), Tile(13, 2), Tile(14, 2)], [Tile(12, 2)])
room6 = Room(Tile(3, 1), 4, 5, [Tile(4, 2), Tile(5, 2), Tile(4, 3), Tile(5, 3), Tile(4, 4)], [Tile(6, 2)])
room7 = Room(Tile(7, 0), 5, 5,
             [Tile(8, 1), Tile(9, 1), Tile(10, 1), Tile(8, 2), Tile(9, 2), Tile(10, 2), Tile(8, 3), Tile(9, 3),
              Tile(10, 3)], [Tile(7, 2), Tile(11, 2), Tile(9, 4)])
room8 = Room(Tile(5, 7), 8, 8, [Tile(9, 7), Tile(9, 8), Tile(8, 8), Tile(7, 8), Tile(7, 9), Tile(8, 9), Tile(9, 9),
                                Tile(10, 9), Tile(10, 10), Tile(9, 10), Tile(7, 10), Tile(6, 10), Tile(6, 11),
                                Tile(8, 11), Tile(9, 11), Tile(6, 12), Tile(7, 12), Tile(6, 13), Tile(7, 13)],
             [Tile(9, 7), Tile(5, 10)])
room9 = Room(Tile(0, 9), 3, 4, [Tile(0, 10), Tile(1, 10), Tile(0, 11), Tile(1, 11)], [Tile(2, 10), Tile(0, 12)])
room10 = Room(Tile(2, 18), 5, 4,
              [Tile(3, 19), Tile(4, 19), Tile(5, 19), Tile(3, 20), Tile(4, 20), Tile(5, 20), Tile(3, 21), Tile(4, 21),
               Tile(5, 21)], [Tile(2, 19)])

hallway3 = Hallway(Tile(9, 4), Tile(9, 7), [])
hallway4 = Hallway(Tile(5, 10), Tile(2, 10), [])
hallway5 = Hallway(Tile(0, 12), Tile(2, 19), [Tile(0, 17), Tile(2, 17)])
level3 = Level([room5, room6, room7, room8, room9, room10], [hallway3, hallway4, hallway5])

# level4
room11 = Room(Tile(0, 0), 5, 4, [Tile(1, 1), Tile(2, 1), Tile(3, 2), Tile(1, 2), Tile(2, 2)], [Tile(3, 2)])
room12 = Room(Tile(5, 0), 3, 4, [Tile(6, 1), Tile(6, 2)], [Tile(6, 1)])
room13 = Room(Tile(8, 0), 4, 4, [Tile(9, 1), Tile(10, 1), Tile(9, 2), Tile(10, 2), Tile(8, 2)], [Tile(8, 2)])
level4 = Level([room11, room12, room13], [])

# render the hard-coded 4 levels presentation
render_level(level1)
render_level(level2)
render_level(level3)
render_level(level4)
