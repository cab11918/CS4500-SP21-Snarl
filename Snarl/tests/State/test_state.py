#! /usr/bin/python3
import json
import sys
import uuid
import json

from Snarl.src.hallway import Hallway
from Snarl.src.room import Room
from Snarl.src.level import Level
from Snarl.src.adversary import Adversary
from Snarl.src.player import Player
from Snarl.src.game_state import GameState
from Snarl.src.exit import Exit
from Snarl.src.key import Key
from Snarl.src.tile import Tile
from Snarl.src.Game.rule_checker import RuleChecker


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
            input_state = parsed_input[0]
            input_name = parsed_input[1]
            input_point = parsed_input[2]

            # input for Level
            input_level = input_state["level"]
            input_rooms = input_level["rooms"]
            input_hallways = input_level["hallways"]
            input_objects = input_level["objects"]

            # input for actor list and exit status

            input_players = input_state["players"]
            input_adversaries = input_state["adversaries"]
            input_exit_locked = input_state["exit-locked"]

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

            # variables needed for actor list and exit status

            parsed_players = []
            parsed_adversaries = []

            for input_player in input_players:
                temp_player = Player(str(uuid.uuid1()), input_player["name"])
                temp_player.position = (input_player["position"][1], input_player["position"][0])
                parsed_players.append(temp_player)

            for input_adversary in input_adversaries:
                if input_adversary["type"] == "zombie":
                    temp_zombie = Adversary(input_adversary["name"], "zombie")
                    temp_zombie.position = (input_adversary["position"][1], input_adversary["position"][0])
                    parsed_adversaries.append(temp_zombie)
                elif input_adversary["type"] == "ghost":
                    temp_ghost = Adversary(input_adversary["name"], "ghost")
                    temp_ghost.position = (input_adversary["position"][1], input_adversary["position"][0])
                    parsed_adversaries.append(temp_ghost)

            parsed_exit_unlocked = not input_exit_locked

            # for this milestone, we assume only one level

            parsed_state = GameState(0, 0, parsed_exit_unlocked, parsed_players, parsed_adversaries, 1)
            parsed_state.init_map(parsed_level)
            player_pos = []
            adversary_pos = []
            for player in parsed_players:
                player_pos.append(player.position)
            for adversary in parsed_adversaries:
                adversary_pos.append(adversary.position)

            parsed_state = parsed_state.get_state(player_pos, adversary_pos, parsed_exit_unlocked)

            is_in_state = False
            the_player = None
            rule_checker = RuleChecker(parsed_state)

            for player in parsed_state.players:
                if player.player_name == input_name:
                    is_in_state = True
                    the_player = player
                    break

            def cons_out_state(given_state):
                # parsing the output state

                out_rooms = []
                out_objects = []
                out_hallways = []
                out_players = []
                out_adversaries = []
                out_exit_locked = not given_state.unlocked

                for room in parsed_level.rooms:
                    temp_layout = []
                    for i in range(0, room.height):
                        temp_row = []
                        for j in range(0, room.width):
                            if (j + room.position[0], i + room.position[1]) in room.non_wall_tiles:
                                temp_row.append(1)
                            elif (j + room.position[0], i + room.position[1]) in room.doors:
                                temp_row.append(2)
                            else:
                                temp_row.append(0)
                        temp_layout.append(temp_row)

                    out_rooms.append({"type": "room",
                                      "origin": [room.position[1], room.position[0]],
                                      "bounds": {
                                          "rows": room.height,
                                          "columns": room.width
                                      },
                                      "layout": temp_layout})

                if not parsed_state.unlocked:
                    out_objects.append({"type": "key",
                                        "position": [parsed_level.key_pos[1], parsed_level.key_pos[0]]})
                out_objects.append({"type": "exit",
                                    "position": [parsed_level.exit_pos[1], parsed_level.exit_pos[0]]})

                for hallway in parsed_level.hallways:
                    temp_wpts = []
                    for wpt in hallway.waypoints:
                        temp_wpts.append([wpt[1], wpt[0]])
                    out_hallways.append({"type": "hallway",
                                         "from": [hallway.door1[1], hallway.door1[0]],
                                         "to": [hallway.door2[1], hallway.door2[0]],
                                         "waypoints": temp_wpts
                                         })

                out_level = {"type": "level",
                             "rooms": out_rooms,
                             "hallways": out_hallways,
                             "objects": out_objects
                             }

                for player in given_state.players:
                    out_players.append({"type": "player",
                                        "name": player.player_name,
                                        "position": [player.position[1], player.position[0]]})

                for adversary in given_state.adversaries:
                    out_adversaries.append({"type": adversary.adversary_type,
                                            "name": adversary.adversary_name,
                                            "position": [adversary.position[1], adversary.position[0]]})

                return {"type": "state",
                        "level": out_level,
                        "players": out_players,
                        "adversaries": out_adversaries,
                        "exit-locked": out_exit_locked}

            if not is_in_state:
                # If the player isn’t part of the input state
                print(json.dumps(["Failure", "Player ", input_name, " is not a part of the game."]))
                return
            else:
                # If the player’s destination tile is not traversable
                if not rule_checker.is_valid_tile((parsed_point[0], parsed_point[1])) or not rule_checker.can_interact(
                        (the_player.position[0], the_player.position[1]), (parsed_point[0], parsed_point[1])):
                    print(json.dumps(
                        ["Failure", "The destination position ", [parsed_point[1], parsed_point[0]], " is invalid."]))
                    return
                else:
                    # If the given player exists in the input state, can be moved to the given position, and the
                    # position is not occupied by an exit or an adversary,
                    if ((not any(isinstance(tile_obj, Exit) for tile_obj in
                                 parsed_state.board[parsed_point[1]][
                                     parsed_point[0]].occupied_by) or not parsed_state.unlocked)
                            and not any(isinstance(tile_obj, Adversary) for tile_obj in
                                        parsed_state.board[parsed_point[1]][parsed_point[0]].occupied_by)):
                        if (any(isinstance(tile_obj, Key) for tile_obj in
                                parsed_state.board[parsed_point[1]][parsed_point[0]].occupied_by)):
                            parsed_state.unlocked = True
                            parsed_state.board[parsed_point[1]][
                                parsed_point[0]].occupied_by = []

                        parsed_state.board[the_player.position[1]][the_player.position[0]].occupied_by = []
                        the_player.position = parsed_point
                        parsed_state.board[the_player.position[1]][the_player.position[0]].occupied_by.append(
                            the_player)

                        print(json.dumps(["Success", cons_out_state(parsed_state)]))

                    # If the player landed on an adversary,
                    if any(isinstance(tile_obj, Adversary) for tile_obj in
                           parsed_state.board[parsed_point[1]][parsed_point[0]].occupied_by):
                        parsed_state.move(the_player.position, parsed_point)

                        parsed_state.board[the_player.position[1]][the_player.position[0]].occupied_by = []
                        if the_player in parsed_players:
                            parsed_players.remove(the_player)

                        print(json.dumps(["Success", "Player ", the_player.player_name, " was ejected",
                                          cons_out_state(parsed_state)]))

                    # If the player landed on an exit and the exit is unlocked
                    if any(isinstance(tile_obj, Exit) for tile_obj in
                           parsed_state.board[parsed_point[1]][
                               parsed_point[0]].occupied_by) and parsed_state.unlocked:

                        parsed_state.board[the_player.position[1]][the_player.position[0]].occupied_by = []
                        if the_player in parsed_players:
                            parsed_players.remove(the_player)

                        print(json.dumps(["Success", "Player ", the_player.player_name, " exited",
                                          cons_out_state(parsed_state)]))

        except (IndexError, TypeError):
            print("Parse failed, not a well-formed JSON.")


if __name__ == "__main__":
    main()
