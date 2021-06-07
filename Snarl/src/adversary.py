import sys
import random
from random import choice
import math
from Snarl.src.tile import Tile
from Snarl.src.player import Player
from Snarl.src.key import Key
from Snarl.src.exit import Exit
from Snarl.src.level import Level
from Snarl.src.room import Room


class Adversary:
    """
    The Adversary class is a representation of the enemies in our game.  The adversary will eventually be controlled by
    AI algorithms.  The moving ability and mechanism will be different from the player.

    adversary_name: The name of the adversary to represent its identity.
    adversary_type: The type of that adversary (Right now, it should be ghost or zombie).
    position: the current position of the adversary on the board in game_state.
    level: the initial current level information the adversary have in order to figure out the next move.
    move_state: the intermediate state for the adversary to figure out the next move.
    """
    adversary_name = None
    adversary_type = None
    position = (-1, -1)
    level = None
    ref_board = None
    visited = []

    def __init__(self, adversary_name, adversary_type, level):
        self.adversary_name = adversary_name
        self.adversary_type = adversary_type
        self.level = level

    def update_ref_board(self, ref_board):
        """
        The function takes a state information which was used when it is the turn to move
        :param ref_board: the intermediate state.
        :return: None
        """
        self.ref_board = ref_board

    def choose_tile(self, to_tiles):
        """
        The function takes a list of tiles position and return random position from the list

        :param to_tiles: list of tuple representing the tile position list
        :return: tuple representing a tile position
        """
        if len(to_tiles) == 0:
            return self.position
        return to_tiles[random.randrange(len(to_tiles))]

    def find_path(self, p, dist):
        """
        the function recursively modifying the visited tile
        :param p: a tuple
        :param dist: int representing the current move dist
        :return:
        """
        self.visited.append(p)
        if dist == 0:
            return
        if self.adversary_type == "zombie":
            if (p[0], p[1] - 1) not in self.visited and self.ref_board[p[1] - 1][p[0]].tile_type == "floor":
                self.find_path((p[0], p[1] - 1), dist - 1)
            if (p[0] - 1, p[1]) not in self.visited and self.ref_board[p[1]][p[0] - 1].tile_type == "floor":
                self.find_path((p[0] - 1, p[1]), dist - 1)
            if (p[0], p[1] + 1) not in self.visited and self.ref_board[p[1] + 1][p[0]].tile_type == "floor":
                self.find_path((p[0], p[1] + 1), dist - 1)
            if (p[0] + 1, p[1]) not in self.visited and self.ref_board[p[1]][p[0] + 1].tile_type == "floor":
                self.find_path((p[0] + 1, p[1]), dist - 1)
        if self.adversary_type == "ghost":
            if (p[0], p[1] - 1) not in self.visited and self.ref_board[p[1] - 1][p[0]].tile_type != "void" and \
                    self.ref_board[p[1] - 1][p[0]].tile_type != "wall":
                self.find_path((p[0], p[1] - 1), dist - 1)
            if (p[0] - 1, p[1]) not in self.visited and self.ref_board[p[1]][p[0] - 1].tile_type != "void" and \
                    self.ref_board[p[1]][p[0] - 1].tile_type != "wall":
                self.find_path((p[0] - 1, p[1]), dist - 1)
            if (p[0], p[1] + 1) not in self.visited and self.ref_board[p[1] + 1][p[0]].tile_type != "void" and \
                    self.ref_board[p[1] + 1][p[0]].tile_type != "wall":
                self.find_path((p[0], p[1] + 1), dist - 1)
            if (p[0] + 1, p[1]) not in self.visited and self.ref_board[p[1]][p[0] + 1].tile_type != "void" and \
                    self.ref_board[p[1]][p[0] + 1].tile_type != "wall":
                self.find_path((p[0] + 1, p[1]), dist - 1)

    def find_dist_help(self, pos1, pos2):
        """
        function for calculating the length of shortest path from pos1 to pos2
        :param pos1: a tuple representing the adversary position
        :param pos2: a tuple representing the player position
        :return: an int representing the distance
        """
        dist = 0
        while pos2 not in self.visited and dist < 999:
            self.visited = []
            self.find_path(pos1, dist)
            dist += 1
        return dist

    def teleport(self, curr_index):
        """
        function for returning a random position to teleport
        :param curr_index: an int presenting the current roome index
        :return: a tuple representing the position of destination
        """
        teleportable = []
        chosen_room = choice([i for i in range(0, len(self.level.rooms)) if i not in [curr_index]])
        for tile_pos in self.level.rooms[chosen_room].non_wall_tiles:
            if not any(isinstance(obj, Player) for obj in
                       self.ref_board[tile_pos[1]][tile_pos[0]].occupied_by) and not \
                    any(isinstance(obj, Adversary) for obj in self.ref_board[tile_pos[1]][tile_pos[0]].occupied_by):
                teleportable.append(tile_pos)
        return teleportable[random.randrange(len(teleportable))]

    def return_move(self):
        """
        The function will output a target move position based on the information an adversry has.
        :return: the position
        """

        self.visited = []
        self.visited.append(self.ref_board[self.position[1]][self.position[0]])
        to_tiles = []

        up = self.ref_board[self.position[1] - 1][self.position[0]]
        left = self.ref_board[self.position[1]][self.position[0] - 1]
        down = self.ref_board[self.position[1] + 1][self.position[0]]
        right = self.ref_board[self.position[1]][self.position[0] + 1]

        if self.adversary_type == "zombie":
            if up.tile_type == "floor":
                if not any(isinstance(obj, Adversary) for obj in up.occupied_by):
                    to_tiles.append((self.position[0], self.position[1] - 1))
            if left.tile_type == "floor":
                if not any(isinstance(obj, Adversary) for obj in left.occupied_by):
                    to_tiles.append((self.position[0] - 1, self.position[1]))
            if down.tile_type == "floor":
                if not any(isinstance(obj, Adversary) for obj in down.occupied_by):
                    to_tiles.append((self.position[0], self.position[1] + 1))
            if right.tile_type == "floor":
                if not any(isinstance(obj, Adversary) for obj in right.occupied_by):
                    to_tiles.append((self.position[0] + 1, self.position[1]))
        if self.adversary_type == "ghost":
            if up.tile_type != "void":
                if not any(isinstance(obj, Adversary) for obj in up.occupied_by):
                    to_tiles.append((self.position[0], self.position[1] - 1))
            if left.tile_type != "void":
                if not any(isinstance(obj, Adversary) for obj in left.occupied_by):
                    to_tiles.append((self.position[0] - 1, self.position[1]))
            if down.tile_type != "void":
                if not any(isinstance(obj, Adversary) for obj in down.occupied_by):
                    to_tiles.append((self.position[0], self.position[1] + 1))
            if right.tile_type != "void":
                if not any(isinstance(obj, Adversary) for obj in right.occupied_by):
                    to_tiles.append((self.position[0] + 1, self.position[1]))

        # return the minimum pos index
        def minimum(a):
            min_pos = a.index(min(a))
            return min_pos

        curr_room = -1
        for i in range(0, len(self.level.rooms)):
            if self.position in self.level.rooms[i].non_wall_tiles:
                curr_room = i
                break

        if self.ref_board is not None:
            if self.adversary_type == "zombie":

                player_pos = []
                for tile_pos in self.level.rooms[curr_room].non_wall_tiles:
                    for obj in self.ref_board[tile_pos[1]][tile_pos[0]].occupied_by:
                        if isinstance(obj, Player):
                            player_pos.append(tile_pos)

                # has player
                if len(player_pos) != 0:
                    to_player_dists = []
                    for tile_pos in to_tiles:
                        for a_player_pos in player_pos:
                            to_player_dists.append(self.find_dist_help(tile_pos, a_player_pos))
                            self.visited = []
                        self.visited = []
                    return to_tiles[math.floor((minimum(to_player_dists))/len(player_pos))]

                # random if no player in room
                else:
                    return self.choose_tile(to_tiles)
            if self.adversary_type == "ghost":
                chase_dist = 5

                player_pos = []
                for i in range(len(self.ref_board)):
                    for j in range(len(self.ref_board[0])):
                        if any(isinstance(obj, Player) for obj in self.ref_board[i][j].occupied_by):
                            player_pos.append((j, i))

                to_player_dists = []
                ghost_preference = None
                for a_player_pos in player_pos:
                    dist = self.find_dist_help(self.position, a_player_pos)
                    self.visited = []

                    if dist <= chase_dist:
                        for tile_pos in to_tiles:
                            if self.ref_board[tile_pos[1]][tile_pos[0]].tile_type != "wall":
                                to_player_dists.append(self.find_dist_help(tile_pos, a_player_pos))
                            elif self.ref_board[tile_pos[1]][tile_pos[0]].tile_type == "void":
                                pass
                            else:
                                to_player_dists.append(99999)
                            self.visited = []
                if len(to_player_dists) != 0:
                    ghost_preference = to_tiles[minimum(to_player_dists) % len(to_tiles)]
                if ghost_preference is not None:
                    return ghost_preference
                else:
                    chosen_tile = self.choose_tile(to_tiles)
                    return self.teleport(curr_room) if self.ref_board[chosen_tile[1]][
                                                           chosen_tile[0]].tile_type == "wall" else chosen_tile
