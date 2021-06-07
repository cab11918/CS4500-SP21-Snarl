#! /usr/bin/python3
import sys
import json

from Snarl.src.room import Room


def main():
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

            if (parsed_input[0]["type"]) == "room":
                position = (parsed_input[0]["origin"][1], parsed_input[0]["origin"][0])
                width = parsed_input[0]["bounds"]["columns"]
                height = parsed_input[0]["bounds"]["rows"]
                point_x = parsed_input[1][1]
                point_y = parsed_input[1][0]
                if (point_x > (width - 1 + position[0]) or point_x < position[0] or
                        point_y > (height - 1 + position[1]) or point_y < position[1]):
                    print(json.dumps(
                        ["Failure: Point ", [point_y, point_x], " is not in room at ", [position[1], position[0]]]))

                else:
                    non_wall_tiles = []
                    doors = []
                    for i in range(height):
                        for j in range(width):
                            if parsed_input[0]["layout"][i][j] == 1:
                                non_wall_tiles.append((j, i))
                            elif parsed_input[0]["layout"][i][j] == 2:
                                doors.append((j, i))

                    parsed_room = Room(position, width, height, non_wall_tiles, doors)

                    point_in_room = (point_x - position[0], point_y - position[1])

                    traversable_points = [(point_in_room[0], point_in_room[1] - 1),
                                          (point_in_room[0] - 1, point_in_room[1]),
                                          (point_in_room[0] + 1, point_in_room[1]),
                                          (point_in_room[0], point_in_room[1] + 1)]
                    output_arr = []
                    traversable_tiles = parsed_room.doors + parsed_room.non_wall_tiles

                    for tile in traversable_points:
                        if tile in traversable_tiles:
                            output_arr.append([tile[1] + position[1], tile[0] + position[0]])

                    print(json.dumps(["Success: Traversable points from ", [point_y, point_x], " in room at ",
                                      [position[1], position[0]], " are ",
                                      output_arr
                                      ]))
            else:
                print("Only Room type supported for milestone 3.")

        except Exception:
            print("Parse failed, not a well-formed JSON.")


if __name__ == "__main__":
    main()
