import sys

from Snarl.src.player import Player
from Snarl.src.adversary import Adversary
from Snarl.src.Game.rule_checker import RuleChecker
from Snarl.src.tile import Tile
from Snarl.src.key import Key
from Snarl.src.exit import Exit


class GameManager:
    player_list = []
    adversary_list = []
    curr_state = None
    rule_checker = None
    selected_tile = None
    levels = []

    def __init__(self, player_list, adversary_list, curr_state, selected_tile):
        """
        For the game manager, it is responsible for accepting registration from the users and add then as a Player to
        the game model. Game Manager should also keep track with all update, making sure the data from game state and
        data passed in Players component are consistent. In the aspect of event handling, Game Manager should have basic
        functionalities to accept queries of movement from users.

        Arguments:
        player_list - an array of Player components representing the collection of all player and data that users
        need. The players field in Game State is now modified as a list of position.
        adversary_list - an array of Adversary components representing all the data that adversaries need for future
        AI design
        curr_state - a GameState representing the ongoing game, storing all data that a Snarl game need.
        movement requests from users should be checked by this rule checker.
        selected_tile - a Tile representing which tile is being chosen by the user. This can be referred by the move
        request(i.e. destination).
        """

        self.player_list = player_list
        self.adversary_list = adversary_list
        self.curr_state = curr_state
        self.selected_tile = selected_tile
        self.rule_checker = RuleChecker(curr_state)

    def register_player(self, player_name):
        """
        A function that accepts the registration from a user. It takes the name provided by user and instantiate.
        a Player Object

        :param player_name: the name of the given player.
        """

        player_num = 4

        for player in self.player_list:
            if player.player_name == player_name:
                print("player: " + player_name + " is already there!")
                return

        sample_player = Player(len(self.player_list), player_name)
        if len(self.player_list) < player_num:
            self.player_list.append(sample_player)
            self.curr_state.players.append(sample_player)
        else:
            print("Can't add more players")

    def preload_levels(self, levels):
        """
        A function which takes the levels information and store them in the game manager.
        :param levels: The input levels.
        :return: None
        """
        self.levels = levels

    def set_level(self):
        """
        Set the Level in the GameState to be the given level representation and initiate the game state.
        :return: None
        """

        if len(self.levels) == 0:
            self.rule_checker.is_game_over = True
            return
        self.curr_state.advance_level(self.levels.pop(0))

    def handle_move(self, from_pos, to_pos):
        """
        Handle the move request from user. Apply the move to the game state and then update all data in curr_state
        and players if the movement is valid. Abort it if it is invalid.

        :param from_pos: the origin point.
        :param to_pos: the destination point.
        """

        if self.rule_checker.is_valid_move(from_pos, to_pos):
            self.curr_state.move(from_pos, to_pos)
            if self.rule_checker.are_all_expelled():
                return
            self.curr_state.switch_turn()

    def get_player(self, player_id):
        """
        Get the player from player_list with given id.

        :param player_id: the id of the player.

        :throw: TypeError when player is not found.
        """

        for player in self.player_list:
            if player.player_id == player_id:
                return player
        raise TypeError("player not found!")

    def update(self):
        """
        Update the position of all player in player_list and adversary_list according to curr_state. It also sets the
        vision of the players and the adversaries.
        """
        for i in range(self.curr_state.board_col):
            for j in range(self.curr_state.board_row):
                for gs_character in self.curr_state.board[j][i].occupied_by:
                    if isinstance(gs_character, Player):
                        for gm_player in self.player_list:
                            if gm_player.player_name == gs_character.player_name:
                                gm_player.position = (i, j)
                                self.set_vision(gm_player)
                    if isinstance(gs_character, Adversary):
                        for gm_adv in self.adversary_list:
                            if gm_adv.adversary_name == gs_character.adversary_name:
                                gm_adv.position = (i, j)

        for player in self.player_list:
            for gs_player in self.curr_state.players:
                if gs_player.player_name == player.player_name and gs_player.expelled:
                    player.expelled = gs_player.expelled
                    self.set_vision(player)
                    self.set_vision(gs_player)

        self.adversary_list = self.curr_state.adversaries
        for adv in self.adversary_list:
            adv.update_ref_board(self.curr_state.board)

    def get_vision(self, player_id):
        """
        Generate the 2d array representing the vision of the player with given id from the curr_state.

        :param player_id: the id of the player.
        """
        for player in self.player_list:
            if player.player_id == player_id:
                return player.vision

    def set_vision(self, player):
        """
        Update the vision of the given player in player_list.

        :param player: the player that needs to update the vision.
        """
        player.vision = []
        player_pos = player.position
        vis_dist = 5
        vis_temp = []

        for i in range(0, vis_dist):
            temp_row = []
            for j in range(0, vis_dist):
                if 0 <= player_pos[1] + j - 2 < self.curr_state.board_row and 0 <= \
                        player_pos[0] + i - 2 < self.curr_state.board_col:
                    temp_row.append(self.curr_state.board[player_pos[1] + j - 2][player_pos[0] + i - 2])
                else:
                    temp_row.append(Tile("void", []))
            vis_temp.append(temp_row)
        player.vision = vis_temp

    def move_result(self, from_pos, to_pos):
        """
        Output a String representation of a move status.

        :param from_pos: the from point of the move.
        :param to_pos: the to point of the move.

        :return the move status result.
        """
        if not self.rule_checker.is_valid_move(from_pos, to_pos):
            return "Invalid"
        elif self.rule_checker.is_valid_move(from_pos, to_pos) and any(
                isinstance(tile_obj, Key) for tile_obj in
                self.curr_state.board[to_pos[1]][to_pos[0]].occupied_by):
            return "Key"
        elif self.rule_checker.is_valid_move(from_pos, to_pos) and any(
                isinstance(tile_obj, Exit) for tile_obj in
                self.curr_state.board[to_pos[1]][to_pos[0]].occupied_by) and self.curr_state.unlocked:
            return "Exit"
        elif self.rule_checker.is_valid_move(from_pos, to_pos) and any(
                isinstance(tile_obj, Adversary) for tile_obj in
                self.curr_state.board[to_pos[1]][to_pos[0]].occupied_by):
            return "Eject"
        elif self.rule_checker.is_valid_move(from_pos, to_pos):
            return "OK"

    @staticmethod
    def get_layout(player):
        """
        The function that takes a player as an input and render the vision of the given player as ASCII value.

        :param player: the player that needs to be rendered for vision.

        :return: the ASCII layout of the player's vision.

        """

        vision = player.vision
        layout = []
        for i in range(0, len(vision)):
            layout_row = []
            for j in range(0, len(vision[0])):
                if vision[j][i].tile_type == "wall":
                    layout_row.append(0)
                if vision[j][i].tile_type == "door":
                    layout_row.append(2)
                if vision[j][i].tile_type == "floor":
                    layout_row.append(1)
                if vision[j][i].tile_type == "hallway":
                    layout_row.append(3)
                if vision[j][i].tile_type == "void":
                    layout_row.append(4)
            layout.append(layout_row)
        return layout

    @staticmethod
    def get_objects(player):
        """
        The function takes a player as the input and return a list of the objects dictionary the player can see

        :param player: the player that needs to be rendered for returning the object list.

        :return The object list.

        """
        vision = player.vision
        objects = []
        for i in range(0, len(vision)):
            for j in range(0, len(vision[0])):
                occupied_by = vision[i][j].occupied_by
                for obj in occupied_by:
                    if isinstance(obj, Key):
                        objects.append({"type": "key", "position": [obj.position[1], obj.position[0]]})
                    if isinstance(obj, Exit):
                        objects.append({"type": "exit", "position": [obj.position[1], obj.position[0]]})

        return objects

    @staticmethod
    def get_actors(player):
        """
        The function takes a player as the input and return a list of the characters dictionary the player can see

        :param player: the player that needs to be rendered for returning the character list.

        :return The character list.

        """
        vision = player.vision
        characters = []
        for i in range(0, len(vision)):
            for j in range(0, len(vision[0])):

                occupied_by = vision[i][j].occupied_by
                for actor in occupied_by:
                    if isinstance(actor, Player):
                        if not actor.expelled:
                            characters.append({"type": "player",
                                               "id": actor.player_id,
                                               "name": actor.player_name,
                                               "position": [actor.position[1], actor.position[0]]})
                    if isinstance(actor, Adversary):
                        if actor.adversary_type == "ghost":
                            characters.append({"type": "ghost", "name": actor.adversary_name,
                                               "position": [actor.position[1], actor.position[0]]})
                        if actor.adversary_type == "zombie":
                            characters.append({"type": "zombie", "name": actor.adversary_name,
                                               "position": [actor.position[1], actor.position[0]]})

        for char in characters:
            if char["name"] == player.player_name:
                characters.remove(char)
        return characters

    def get_adv_layout(self):
        """
        The function that takes an adversary as an input and render the vision of the given adversary as ASCII value.

        :return: the ASCII layout of the player's vision.

        """

        vision = self.curr_state.board
        layout = []
        for j in range(0, len(vision)):
            layout_row = []
            for i in range(0, len(vision[0])):
                if vision[j][i].tile_type == "wall":
                    layout_row.append(0)
                if vision[j][i].tile_type == "door":
                    layout_row.append(2)
                if vision[j][i].tile_type == "floor":
                    layout_row.append(1)
                if vision[j][i].tile_type == "hallway":
                    layout_row.append(3)
                if vision[j][i].tile_type == "void":
                    layout_row.append(4)
            layout.append(layout_row)
        return layout

    def get_adv_objects(self):
        """
        The function takes an adversary as the input and return a list of the objects dictionary the adversary can see

        :return The object list.

        """
        vision = self.curr_state.board
        objects = []
        for i in range(0, len(vision)):
            for j in range(0, len(vision[0])):
                occupied_by = vision[i][j].occupied_by
                for obj in occupied_by:
                    if isinstance(obj, Key):
                        objects.append({"type": "key", "position": [obj.position[1], obj.position[0]]})
                    if isinstance(obj, Exit):
                        objects.append({"type": "exit", "position": [obj.position[1], obj.position[0]]})
        return objects

    def get_adv_actors(self):
        """
        The function takes an adversary as the input and return a list of the characters dictionary the adversary can see

        :return The character list.

        """
        vision = self.curr_state.board
        characters = []
        for i in range(0, len(vision)):
            for j in range(0, len(vision[0])):

                occupied_by = vision[i][j].occupied_by
                for actor in occupied_by:
                    if isinstance(actor, Player):
                        if not actor.expelled:
                            characters.append({"type": "player",
                                               "id": actor.player_id,
                                               "name": actor.player_name,
                                               "position": [actor.position[1], actor.position[0]]})
                    if isinstance(actor, Adversary):
                        if actor.adversary_type == "ghost":
                            characters.append({"type": "ghost", "name": actor.adversary_name,
                                               "position": [actor.position[1], actor.position[0]]})
                        if actor.adversary_type == "zombie":
                            characters.append({"type": "zombie", "name": actor.adversary_name,
                                               "position": [actor.position[1], actor.position[0]]})

        return characters
