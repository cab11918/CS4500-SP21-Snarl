import json
import os

from Snarl.src.hallway import Hallway
from Snarl.src.room import Room
from Snarl.src.level import Level


def levels_reader(levels_file):
    """
    A JSON reader that parse the information of a level into the game model.
    :param levels_file: the file given
    :return: A number indicates how many levels and the levels being parsed
    :except: IndexError When the level information is incorrect
    :except: TypeError When the level information is incorrect
    """
    parsed_level_num = None
    parsed_levels = []
    name, extension = os.path.splitext(levels_file)
    parsed_spec = []
    if extension != ".levels":
        print("Unsupported file type.")
        return

    line_buffer = ""
    with open(levels_file) as lines:
        try:
            while True:
                line_buffer += next(lines)
                try:
                    parsed_spec.append(json.loads(line_buffer))
                    line_buffer = ""
                except json.JSONDecodeError:
                    pass

        except StopIteration:
            pass

    parsed_level_num = parsed_spec.pop(0)
    parsed_level_num = int(parsed_level_num)
    try:
        for input_level in parsed_spec:
            # take the input values from json.
            input_rooms = input_level["rooms"]
            input_hallways = input_level["hallways"]
            input_objects = input_level["objects"]

            # variables needed for Level model
            parsed_rooms = []
            parsed_hallways = []
            parsed_level = None
            parsed_key_pos = None
            parsed_exit_pos = None

            for room in input_rooms:
                position = (room["origin"][1], room["origin"][0])
                width = room["bounds"]["columns"]
                height = room["bounds"]["rows"]
                non_wall_tiles = []
                doors = []

                for i in range(height):
                    for j in range(width):
                        if room["layout"][i][j] == 1:
                            non_wall_tiles.append((j + position[0], i + position[1]))
                        elif room["layout"][i][j] == 2:
                            doors.append((j + position[0], i + position[1]))

                parsed_room = Room(position, width, height, non_wall_tiles, doors)
                parsed_rooms.append(parsed_room)

            for hallway in input_hallways:
                door1 = (hallway["from"][1], hallway["from"][0])
                door2 = (hallway["to"][1], hallway["to"][0])
                way_points = []
                for wpt in hallway["waypoints"]:
                    way_points.append((wpt[1], wpt[0]))
                parsed_hallways.append(Hallway(door1, door2, way_points))
            for obj in input_objects:
                if obj["type"] == "key":
                    parsed_key_pos = (obj["position"][1], obj["position"][0])
                elif obj["type"] == "exit":
                    parsed_exit_pos = (obj["position"][1], obj["position"][0])

            # the level was constructed
            parsed_level = Level(parsed_rooms, parsed_hallways, parsed_key_pos, parsed_exit_pos)
            parsed_levels.append(parsed_level)

    except (IndexError, TypeError):
        print("Parse failed, not well-formed level JSON!")

    return parsed_level_num, parsed_levels
