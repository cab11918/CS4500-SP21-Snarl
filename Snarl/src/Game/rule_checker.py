import sys

from Snarl.src.player import Player
from Snarl.src.adversary import Adversary
from Snarl.src.exit import Exit
from Snarl.src.tile import Tile


class RuleChecker:
    state = None
    is_game_over = False

    def __init__(self, state):
        """
        For the Rule Checker, it validates the movement and the interaction of players and adversaries. It also check
        if the level or the game is ended. Plus, it will check for invalid GameState and reject if needed.

        :param state: The state Rule Checker is checking which contains all information needed for validation. A state
        has all players and adversaries location, exit/turn/level status, and the game board, etc.

        :returns None
        """

        self.state = state

    def is_valid_move(self, from_pos, to_pos):
        """
        A top-level validity checker which will return true for the move if all the helper-function passed. The helpers
        ensure the distance of the movement, the target tile and the interactions happened after the move are all valid.

        :param from_pos: the start point of the movement represented by (x,y).
        :param to_pos: the end point of the movement represented by (x,y).

        :return: a Boolean which represent if the move is valid.
        """

        move_actor = None
        for obj in self.state.board[from_pos[1]][from_pos[0]].occupied_by:
            if isinstance(obj, Player) or isinstance(obj, Adversary):
                move_actor = obj

        if isinstance(move_actor, Player):
            return (self.is_valid_dist(from_pos, to_pos) and self.is_valid_tile(
                to_pos) and self.can_interact(from_pos, to_pos)) or from_pos == to_pos
        else:
            return True

    def is_valid_dist(self, from_pos, to_pos):
        """
        A helper function for is_valid_move(from,to) which ensure the move is under 2 cardinal moves away.

        :param from_pos: the start point of the movement represented by (x,y).
        :param to_pos: the end point of the movement represented by (x,y).

        :return: a Boolean which represent if the move is in a valid distance.
        """

        state_temp = self.state
        move_dist = 2

        visited = []

        def find_path(p, dist):
            nonlocal state_temp
            if dist < 0:
                return
            visited.append(p)

            if (p[1] > 0) and (p[0], p[1] - 1) not in visited and state_temp.board[p[1] - 1][
                p[0]].tile_type != "wall" and \
                    state_temp.board[p[1] - 1][p[0]].tile_type != "void":
                find_path((p[0], p[1] - 1), dist - 1)
            if (p[0] > 0) and (p[0] - 1, p[1]) not in visited and state_temp.board[p[1]][
                p[0] - 1].tile_type != "wall" and \
                    state_temp.board[p[1]][p[0] - 1].tile_type != "void":
                find_path((p[0] - 1, p[1]), dist - 1)
            if p[1] < self.state.board_row - 1:
                if (p[0], p[1] + 1) not in visited and state_temp.board[p[1] + 1][p[0]].tile_type != "wall" and \
                        state_temp.board[p[1] + 1][p[0]].tile_type != "void":
                    find_path((p[0], p[1] + 1), dist - 1)
            if p[0] < self.state.board_col - 1:
                if (p[0] + 1, p[1]) not in visited and state_temp.board[p[1]][p[0] + 1].tile_type != "wall" and \
                        state_temp.board[p[1]][p[0] + 1].tile_type != "void":
                    find_path((p[0] + 1, p[1]), dist - 1)

        find_path(from_pos, move_dist)

        return (abs(from_pos[0] - to_pos[0]) + abs(from_pos[1] - to_pos[1])) <= move_dist and to_pos in visited

    def is_valid_tile(self, to_pos):
        """
        A helper function for is_valid_move(from,to) which ensure the target Tile is a traversable Tile
        (e.g. floor, hallway, door).

        :param to_pos: the end point of the movement represented by (x,y).

        :return: a Boolean which represent if the target tile is either a floor, hallway or door .

        :throw: IndexError which indicates the failure of movement due to a non-traversable Tile (e.g. a wall).
        """
        try:
            to_tile = self.state.board[to_pos[1]][to_pos[0]]
        except IndexError:
            print("Unable to find the Tile in game board")

        return not (to_tile.tile_type == "wall" or to_tile.tile_type == "void")

    def can_interact(self, from_pos, to_pos):
        """
        A helper function for is_valid_move(from,to) which ensure the interaction that will happen after the movement
        would be valid. The Player can interact with Key, Adversary but not other Player.

        :param from_pos: the start point of the movement represented by (x,y).
        :param to_pos: the end point of the movement represented by (x,y).

        :return: a Boolean which represent if the interaction is either Player -> Object or Player -> Adversary.

        :throw: IndexError which indicates the failure of movement due to a invalid interaction which will happen
        after the move.
        """

        try:
            from_tile = self.state.board[from_pos[1]][from_pos[0]]
            to_tile = self.state.board[to_pos[1]][to_pos[0]]
        except IndexError:
            print("Unable to find the Tile in game board")

        can_interact = False

        for from_tile_obj in from_tile.occupied_by:
            if isinstance(from_tile_obj, Player):
                for tile_obj in to_tile.occupied_by:
                    if isinstance(tile_obj, Player):
                        return can_interact
                can_interact = True

        return can_interact

    def is_level_end(self, to_pos):
        """
        A function to check if the players can move to the next level.

        :return: a Boolean which represent if the level end either because all the players were expelled or because
        the key was found by players and they enter the exit.
        """

        return any(isinstance(obj, Exit) for obj in self.state.board[to_pos[1]][to_pos[0]].occupied_by) \
               and self.state.unlocked

    def are_all_expelled(self):
        """
        A function to check if the game is over.

        :return: a Boolean which represent if the game is over. The game is over if all the Players were expelled in
        the current level, or one of the player reach Exit of the final Level.
        """

        all_expelled = True
        for player in self.state.players:
            if not player.expelled:
                all_expelled = False
                break

        self.is_game_over = all_expelled
        return self.is_game_over
