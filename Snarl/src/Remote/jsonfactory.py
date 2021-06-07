from Snarl.src.tile import Tile
from Snarl.src.player import Player
from Snarl.src.key import Key
from Snarl.src.exit import Exit
from Snarl.src.adversary import Adversary

"""
This module provides the functionality to read and construct JSON server message referred to the Snarl game model.
The 'parse_...' functions for reading and 'output_...' functions for constructing.
"""


def parse_player_update_message(input_msg):
    """
    The function that takes a input message which is JSON format and parse it into the game model and return the model
    information for the player.
    :param input_msg: The JSON message of the model informatiion.
    :return: The player's position, the vision board and the expell status of the player.
    """
    expelled = False
    player_id = input_msg["id"]
    player_name = input_msg["name"]
    position = input_msg["position"]
    objects = input_msg["objects"]
    actors = input_msg["actors"]
    message = input_msg["message"]
    layout = input_msg["layout"]

    board = []
    for i in range(len(input_msg["layout"])):
        row = []
        for j in range(len(input_msg["layout"][0])):
            if layout[j][i] == 0:
                row.append(Tile("wall", []))
            if layout[j][i] == 1:
                row.append(Tile("floor", []))
            if layout[j][i] == 2:
                row.append(Tile("door", []))
            if layout[j][i] == 3:
                row.append(Tile("hallway", []))
            if layout[j][i] == 4:
                row.append(Tile("void", []))
        board.append(row)

    for obj in objects:
        if obj["type"] == "key":
            board[obj["position"][1] - position[1] + 2][obj["position"][0] - position[0] + 2].occupied_by.append(
                Key((obj["position"][1], obj["position"][0])))
        if obj["type"] == "exit":
            board[obj["position"][1] - position[1] + 2][obj["position"][0] - position[0] + 2].occupied_by.append(
                Exit((obj["position"][1], obj["position"][0])))

    for act in actors:
        if act["type"] == "player":
            board[act["position"][1] - position[1] + 2][act["position"][0] - position[0] + 2].occupied_by.append(
                Player(act["id"], act["name"])
            )
        if act["type"] == "zombie":
            board[act["position"][1] - position[1] + 2][act["position"][0] - position[0] + 2].occupied_by.append(
                Adversary(act["name"], "zombie", None)
            )
        if act["type"] == "ghost":
            board[act["position"][1] - position[1] + 2][act["position"][0] - position[0] + 2].occupied_by.append(
                Adversary(act["name"], "ghost", None)
            )

    the_player = Player(player_id, player_name)

    if not any(isinstance(obj, Adversary) for obj in board[2][2].occupied_by):
        board[2][2].occupied_by.append(the_player)
    else:
        expelled = True

    return (position[1], position[0]), board, expelled


def parse_adv_update_message(input_msg):
    """
    The function that takes a input message which is JSON format and parse it into the game model and return the model
    information for the adversary.
    :param input_msg: The JSON message of the model informatiion.
    :return: The adversary's position, and the vision board.
    """
    position = input_msg["position"]
    objects = input_msg["objects"]
    actors = input_msg["actors"]
    message = input_msg["message"]
    layout = input_msg["layout"]

    board = []
    for j in range(len(input_msg["layout"])):
        row = []
        for i in range(len(input_msg["layout"][0])):
            if layout[j][i] == 0:
                row.append(Tile("wall", []))
            if layout[j][i] == 1:
                row.append(Tile("floor", []))
            if layout[j][i] == 2:
                row.append(Tile("door", []))
            if layout[j][i] == 3:
                row.append(Tile("hallway", []))
            if layout[j][i] == 4:
                row.append(Tile("void", []))
        board.append(row)

    for obj in objects:
        if obj["type"] == "key":
            board[obj["position"][0]][obj["position"][1]].occupied_by.append(
                Key((obj["position"][1], obj["position"][0])))
        if obj["type"] == "exit":
            board[obj["position"][0]][obj["position"][1]].occupied_by.append(
                Exit((obj["position"][1], obj["position"][0])))

    for act in actors:
        if act["type"] == "player":
            print(act["position"][0], act["position"][1])
            print(len(board))
            print(len(board[0]))

            board[act["position"][0]][act["position"][1]].occupied_by.append(
                Player(act["id"], act["name"])
            )
        if act["type"] == "zombie":
            print(act["position"][0], act["position"][1])
            print(len(board))
            print(len(board[0]))
            board[act["position"][0]][act["position"][1]].occupied_by.append(
                Adversary(act["name"], "zombie", None)
            )
        if act["type"] == "ghost":
            print(act["position"][0], act["position"][1])
            print(len(board))
            print(len(board[0]))

            board[act["position"][0]][act["position"][1]].occupied_by.append(
                Adversary(act["name"], "ghost", None)
            )

    return (position[1], position[0]), board
