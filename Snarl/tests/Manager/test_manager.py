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
from Snarl.src.Game.game_manager import GameManager


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
            input_name_list = parsed_input[0] if 1 <= len(parsed_input[0]) <= 4 else None
            input_level = parsed_input[1]
            parsed_natural = parsed_input[2]
            input_point_list = parsed_input[3]
            input_actor_move_list_list = parsed_input[4]

            parsed_player_list = []
            parsed_adversary_list = []
            curr = 0
            for name in input_name_list:
                parsed_player_list.append(Player(curr, name))
                curr += 1
            for i in range(0, len(input_point_list) - len(input_name_list)):
                parsed_adversary_list.append(Adversary("ghost1", "ghost"))

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

            parsed_point_list = []
            for point in input_point_list:
                parsed_point_list.append((point[1], point[0]))

            player_point_list = []
            adversary_point_list = []

            if len(parsed_point_list) <= len(parsed_player_list):
                player_point_list = parsed_point_list
            else:
                player_point_list = parsed_point_list[0: len(parsed_player_list)]
                adversary_point_list = parsed_point_list[len(parsed_player_list): len(parsed_point_list)]

            for player_i in range(0, len(parsed_player_list)):
                parsed_player_list[player_i].position = player_point_list[player_i]

            for adv_i in range(0, len(parsed_adversary_list)):
                parsed_adversary_list[adv_i].position = parsed_adversary_list[adv_i]

            parsed_actor_move_list_list = []

            for move_list in input_actor_move_list_list:
                temp_move_list = []
                for move in move_list:
                    if move["to"] is None:
                        temp_move_list.append(None)
                    else:
                        temp_move_list.append((move["to"][1], move["to"][0]))

                parsed_actor_move_list_list.append(temp_move_list)

            parsed_state = GameState(0, 0, False, [], [], 1)
            parsed_state.init_map(parsed_level)
            parsed_game_manager = GameManager([], [], parsed_state, None)
            for player in parsed_player_list:
                parsed_game_manager.register_player(player.player_name)
            for adversary in parsed_adversary_list:
                parsed_game_manager.adversary_list.append(adversary)
                parsed_game_manager.curr_state.adversaries.append(adversary)
            parsed_state = parsed_state.get_state(player_point_list, adversary_point_list, False)
            parsed_game_manager.curr_state = parsed_state

            parsed_game_manager.update()

            temp_aml_list = parsed_actor_move_list_list
            temp_natural = parsed_natural

            output_trace = []

            for player in parsed_game_manager.player_list:
                if not player.expelled:
                    parsed_game_manager.set_vision(player)
                    output_trace.append([player.player_name, {
                        "type": "player-update",
                        "position": [player.position[1], player.position[0]],
                        "layout": parsed_game_manager.get_layout(player),
                        "objects": parsed_game_manager.get_objects(player),
                        "actors": parsed_game_manager.get_actors(player)
                    }])

            round_count = 0

            # determine if the [[],[],...] array is empty
            def is_amll_empty(amll):
                for aml in amll:
                    if len(aml) != 0:
                        return False
                return True

            # update the move information and appened it into the output trace list.
            def output_trace_move(the_player, the_move):
                if the_move is None:
                    output_trace.append(
                        [parsed_game_manager.player_list[
                             parsed_game_manager.curr_state.turn].player_name,
                         {"type": "move", "to": None},
                         parsed_game_manager.move_result(the_player.position, the_player.position)])
                else:
                    output_trace.append(
                        [parsed_game_manager.player_list[
                             parsed_game_manager.curr_state.turn].player_name,
                         {"type": "move", "to": [the_move[1], the_move[0]]},
                         parsed_game_manager.move_result(the_player.position, the_move)])

            # update all the player informatiion and add them into the output trace list.
            def output_trace_players():
                for player in parsed_game_manager.player_list:
                    if not player.expelled:
                        parsed_game_manager.set_vision(player)
                        output_trace.append([player.player_name, {
                            "type": "player-update",
                            "position": [player.position[1], player.position[0]],
                            "layout": parsed_game_manager.get_layout(player),
                            "objects": parsed_game_manager.get_objects(player),
                            "actors": parsed_game_manager.get_actors(player)
                        }])

            # terminate if the round reached the maxium round or the move list is exhausted
            while parsed_natural > round_count and not is_amll_empty(parsed_actor_move_list_list):
                try:
                    the_move = parsed_actor_move_list_list[parsed_game_manager.curr_state.turn].pop(0)
                except IndexError:
                    pass

                the_player = parsed_game_manager.player_list[parsed_game_manager.curr_state.turn]

                if the_move is None:

                    output_trace_move(the_player, the_move)
                    parsed_game_manager.handle_move(the_player.position, the_player.position)
                    parsed_game_manager.update()
                    output_trace_players()
                    if parsed_game_manager.curr_state.turn == 0:
                        round_count += 1
                # if the move is "Invalid"
                elif parsed_game_manager.move_result(the_player.position, the_move) == "Invalid":
                    output_trace_move(the_player, the_move)
                # if the move is "Eject"
                elif parsed_game_manager.move_result(the_player.position, the_move) == "Eject":
                    output_trace_move(the_player, the_move)
                    temp_turn = parsed_game_manager.curr_state.turn
                    parsed_game_manager.handle_move(the_player.position, the_move)
                    parsed_game_manager.update()
                    output_trace_players()
                    if parsed_game_manager.curr_state.turn == 0:
                        round_count += 1
                    parsed_actor_move_list_list[temp_turn] = []
                # if the move is "Exit"
                elif parsed_game_manager.move_result(the_player.position, the_move) == "Exit":
                    output_trace_move(the_player, the_move)
                    parsed_game_manager.handle_move(the_player.position, the_move)
                    parsed_game_manager.update()
                    output_trace_players()
                    if parsed_game_manager.curr_state.turn == 0:
                        round_count += 1
                    parsed_actor_move_list_list = [[]]
                # if the move is "OK" or "Key"
                else:
                    output_trace_move(the_player, the_move)
                    parsed_game_manager.handle_move(the_player.position, the_move)
                    parsed_game_manager.update()
                    output_trace_players()
                    if parsed_game_manager.curr_state.turn == 0:
                        round_count += 1

            # a helper method to parse the state into a JSON object
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
                    if not player.expelled:
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

            print(json.dumps([cons_out_state(parsed_game_manager.curr_state), output_trace]))

        except (IndexError, TypeError):
            print("Parse failed, not a well-formed JSON.")


if __name__ == "__main__":
    main()
