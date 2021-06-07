#! /usr/bin/python3
import json
import sys

from Snarl.src.hallway import Hallway
from Snarl.src.room import Room
from Snarl.src.level import Level


def main():
    """
    This function takes a JSON value from the STDIN, parse the values into our data model and output the information
    needed to STDOUT

    Arguments: no argument
    Raises:  IndexError for any list index that are out of bound in the model due to the Non-well formed JSON input
            TypeError for anything that is not correctly initialized due to the Non-well formed JSON input.
    """

    # initialize the parsed input
    parsed_input = -1
    try:
        try:
            input_json = sys.argv[1]
            parsed_input = json.loads(input_json)
        except IndexError:
            input_json = sys.stdin.read()
            parsed_input = json.loads(input_json)
    except json.JSONDecodeError:
        print("Invalid json.")

    if parsed_input != -1:

        try:

            # take the input values from json.
            input_level = parsed_input[0]
            input_point = parsed_input[1]
            input_rooms = input_level["rooms"]
            input_hallways = input_level["hallways"]
            input_objects = input_level["objects"]

            # variables needed for Level model
            parsed_point = (input_point[1], input_point[0])
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

            # variables used to store all x y dimensions and generate the 2D array of the whole level
            all_x = []
            all_y = []
            all_wps_x = [0]
            all_wps_y = [0]

            for room in parsed_level.rooms:
                all_x.append(room.position[0] + room.width - 1)
                all_y.append(room.position[1] + room.height - 1)

            for hallway in parsed_level.hallways:
                for point in hallway.waypoints:
                    all_wps_x.append(point[0])
                    all_wps_y.append(point[1])

            board_col = max(max(all_x), max(all_wps_x)) + 1
            board_row = max(max(all_y), max(all_wps_y)) + 1

            # initialize output variables
            output_object = None
            output_traversable = False
            output_type = "void"
            output_reachable = []

            # check if the point contains an object and output the type of that object.
            if parsed_level.key_pos == parsed_point:
                output_object = "key"
            elif parsed_level.exit_pos == parsed_point:
                output_object = "exit"

            def point_in_range(p, p1, p2):
                """
                A helper that takes a point and two other points and check if the point is in the given range. The range
                means if they have the same y coordinate, does the point in their range of x coordinates, if they have
                the same x coordinate, does the point in their range of y coordinates.

                Arguments:
                    p: the point which will be checked
                    p1: one of the coordinate for comparison of range
                    p2: one of the coordinate for comparison of range
                """
                if p[0] == p1[0] == p2[0]:
                    return p[1] in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1)
                elif p[1] == p1[1] == p2[1]:
                    return p[0] in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1)

            # the enumeration of all the points the given coordinate intersect horizontally and vertically.
            search_list = []
            for i in range(0, board_row):
                search_list.append((parsed_point[0], i))
            for j in range(0, board_col):
                search_list.append((j, parsed_point[1]))

            # all the doors and waypoints that are intersecting the enumeration search list
            door_wpt_result_list = []

            # the hallway which the point is on and it would connect two reachable rooms.
            target_hallway = None

            # check if the given point is in the result list and if it is in their range pair by pair, if it's just a
            # hallway without any waypoint, check if it's in the range of two doors. it also helps to specify the target
            # hallway which will be used for figuring out the reachable rooms.
            for hallway in parsed_level.hallways:
                if hallway.door1 in search_list:
                    door_wpt_result_list.append(hallway.door1)
                if hallway.door2 in search_list:
                    door_wpt_result_list.append(hallway.door2)

            for hallway in parsed_level.hallways:
                if len(hallway.waypoints) == 0:
                    if hallway.door1 in door_wpt_result_list and hallway.door2 in door_wpt_result_list and \
                            point_in_range(
                                parsed_point,
                                hallway.door1,
                                hallway.door2):
                        output_type = "hallway"
                        target_hallway = hallway
                else:
                    on_waypoint = False
                    for waypoint in hallway.waypoints:
                        if waypoint == parsed_point:
                            output_type = "hallway"
                            on_waypoint = True
                            target_hallway = hallway
                            break
                        if waypoint in search_list:
                            door_wpt_result_list.append(waypoint)
                    temp_point = hallway.door1
                    i = 0
                    while i < len(hallway.waypoints) and not on_waypoint:
                        if temp_point in door_wpt_result_list and hallway.waypoints[
                            i] in door_wpt_result_list \
                                and point_in_range(parsed_point, temp_point, hallway.waypoints[i]):
                            output_type = "hallway"
                            target_hallway = hallway
                            break
                        else:
                            temp_point = hallway.waypoints[i]
                            i = i + 1
                    if hallway.waypoints[
                        len(
                            hallway.waypoints) - 1] in door_wpt_result_list and hallway.door2 in \
                            door_wpt_result_list and \
                            point_in_range(parsed_point, hallway.waypoints[len(hallway.waypoints) - 1],
                                           hallway.door2):
                        output_type = "hallway"
                        target_hallway = hallway

            for room in parsed_level.rooms:
                if parsed_point[0] in range(room.position[0], room.position[0] + room.width) and parsed_point[1] \
                        in range(room.position[1], room.position[1] + room.height):
                    output_type = "room"

            if output_type == "hallway":
                for room in parsed_level.rooms:
                    for door in room.doors:
                        if door == target_hallway.door1 or door == target_hallway.door2:
                            output_reachable.append([room.position[1], room.position[0]])

            elif output_type == "room":
                to_doors = []
                for room in parsed_level.rooms:
                    if parsed_point[0] in range(room.position[0], room.position[0] + room.width) and parsed_point[1] \
                            in range(room.position[1], room.position[1] + room.height):
                        for door in room.doors:
                            for hallway in parsed_level.hallways:
                                if door == hallway.door1:
                                    to_doors.append(hallway.door2)
                                elif door == hallway.door2:
                                    to_doors.append(hallway.door1)

                for door in to_doors:
                    for room in parsed_level.rooms:
                        if door in room.doors:
                            output_reachable.append([room.position[1], room.position[0]])

            if output_type == "hallway":
                output_traversable = True
            elif output_type == "room":
                for room in parsed_level.rooms:
                    if parsed_point in room.doors + room.non_wall_tiles:
                        output_traversable = True

            print(json.dumps({"traversable": output_traversable,
                              "object": output_object,
                              "type": output_type,
                              "reachable": output_reachable}))

        except (IndexError, TypeError):
            print("Parse failed, not a well-formed JSON.")


if __name__ == "__main__":
    main()
