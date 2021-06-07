#! /usr/bin/python3
from Snarl.src.game_state import *
from Snarl.src.room import Room
from Snarl.src.level import Level
from Snarl.src.hallway import Hallway
from Snarl.src.player import Player
from Snarl.src.adversary import Adversary

import unittest

# level 1

room1 = Room((0, 0), 4, 3, [(1, 1), (2, 1)], [(3, 1)])
room2 = Room((6, 0), 3, 3, [(7, 1)], [(6, 1)])
hallway1 = Hallway((3, 1), (6, 1), [])
level1 = Level([room1, room2], [hallway1], (1, 1), (7, 1))

# level 2

room3 = Room((0, 0), 5, 5, [(1, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)],
             [(0, 1), (1, 4)])
room4 = Room((6, 0), 4, 5, [(8, 1), (8, 2), (7, 2), (8, 3), (7, 3)], [(9, 1)])
hallway2 = Hallway((1, 4), (9, 1), [(1, 5), (10, 5), (10, 1)])
level2 = Level([room3, room4], [hallway2], (2, 2), (7, 3))

# level 3

room5 = Room((12, 0), 3, 4, [(14, 0), (13, 1), (14, 1), (13, 2), (14, 2)], [(12, 2)])
room6 = Room((3, 1), 4, 5, [(4, 2), (5, 2), (4, 3), (5, 3), (4, 4)], [(6, 2)])
room7 = Room((7, 0), 5, 5,
             [(8, 1), (9, 1), (10, 1), (8, 2), (9, 2), (10, 2), (8, 3), (9, 3),
              (10, 3)], [(7, 2), (11, 2), (9, 4)])
room8 = Room((5, 7), 8, 8, [(9, 7), (9, 8), (8, 8), (7, 8), (7, 9), (8, 9), (9, 9),
                            (10, 9), (10, 10), (9, 10), (7, 10), (6, 10), (6, 11),
                            (8, 11), (9, 11), (6, 12), (7, 12), (6, 13), (7, 13)],
             [(9, 7), (5, 10)])
room9 = Room((0, 9), 3, 4, [(0, 10), (1, 10), (0, 11), (1, 11)], [(2, 10), (0, 12)])
room10 = Room((2, 18), 5, 4,
              [(3, 19), (4, 19), (5, 19), (3, 20), (4, 20), (5, 20), (3, 21), (4, 21),
               (5, 21)], [(2, 19)])

hallway3 = Hallway((9, 4), (9, 7), [])
hallway4 = Hallway((5, 10), (2, 10), [])
hallway5 = Hallway((0, 12), (2, 19), [(0, 17), (2, 17)])
level3 = Level([room5, room6, room7, room8, room9, room10], [hallway3, hallway4, hallway5], (0, 11), (4, 20))

# level4
room11 = Room((0, 0), 5, 4, [(1, 1), (2, 1), (3, 2), (1, 2), (2, 2)], [(3, 2)])
room12 = Room((5, 0), 3, 4, [(6, 1), (6, 2)], [(6, 1)])
room13 = Room((8, 0), 4, 4, [(9, 1), (10, 1), (9, 2), (10, 2), (8, 2)], [(8, 2)])
level4 = Level([room11, room12, room13], [], (3, 2), (10, 1))

player1 = Player(0, "Alice")
player2 = Player(1, "Bob")
player3 = Player(2, "Charlie")
player4 = Player(3, "Dylan")

adv1 = Adversary("Kayn", "ghost")
adv2 = Adversary("Nocture", "ghost")
adv3 = Adversary("Dr.Mundo", "zombie")


class TestGameState(unittest.TestCase):
    def test_init_game(self):
        """
        test whether init_game() successfully initialized the game with given level
        :return:
        """
        game1 = GameState(0, 0, False, [player1, player2, player3, player4], [adv1, adv2, adv3], 5)

        game1.init_map(level3)
        board_output = ""
        for i in range(len(game1.board)):
            row = ""
            for j in range(len(game1.board[0])):
                tile = game1.board[i][j]
                if tile.tile_type == "floor" or tile.tile_type == "hallway":
                    row += " 1 "
                if tile.tile_type == "door":
                    row += " 2 "
                if tile.tile_type == "wall":
                    row += " 0 "
                if tile.tile_type == "void":
                    row += " x "
            board_output += row
            board_output += "\n"
        self.assertEqual(
            " x  x  x  x  x  x  x  0  0  0  0  0  0  0  1 \n"
            " x  x  x  0  0  0  0  0  1  1  1  0  0  1  1 \n"
            " x  x  x  0  1  1  2  2  1  1  1  2  2  1  1 \n"
            " x  x  x  0  1  1  0  0  1  1  1  0  0  0  0 \n"
            " x  x  x  0  1  0  0  0  0  2  0  0  x  x  x \n"
            " x  x  x  0  0  0  0  x  x  1  x  x  x  x  x \n"
            " x  x  x  x  x  x  x  x  x  1  x  x  x  x  x \n"
            " x  x  x  x  x  0  0  0  0  2  0  0  0  x  x \n"
            " x  x  x  x  x  0  0  1  1  1  0  0  0  x  x \n"
            " 0  0  0  x  x  0  0  1  1  1  1  0  0  x  x \n"
            " 1  1  2  1  1  2  1  1  0  1  1  0  0  x  x \n"
            " 1  1  0  x  x  0  1  0  1  1  0  0  0  x  x \n"
            " 2  0  0  x  x  0  1  1  0  0  0  0  0  x  x \n"
            " 1  x  x  x  x  0  1  1  0  0  0  0  0  x  x \n"
            " 1  x  x  x  x  0  0  0  0  0  0  0  0  x  x \n"
            " 1  x  x  x  x  x  x  x  x  x  x  x  x  x  x \n"
            " 1  x  x  x  x  x  x  x  x  x  x  x  x  x  x \n"
            " 1  1  1  x  x  x  x  x  x  x  x  x  x  x  x \n"
            " x  x  1  0  0  0  0  x  x  x  x  x  x  x  x \n"
            " x  x  2  1  1  1  0  x  x  x  x  x  x  x  x \n"
            " x  x  0  1  1  1  0  x  x  x  x  x  x  x  x \n"
            " x  x  0  1  1  1  0  x  x  x  x  x  x  x  x \n", board_output)

    def test_curr_level_1(self):
        """
        test if the curr_level field is initialized correctly
        :return:
        """
        game2 = GameState(1, 0, False, [player1, player2, player3, player4], [adv1, adv2, adv3], 5)
        game2.init_map(level1)
        expected = game2.curr_level
        self.assertEqual(1, expected)
        game3 = GameState(3, 0, False, [player1], [adv1], 5)
        game3.init_map(level1)
        expected = game3.curr_level
        self.assertEqual(3, expected)

    def test_advance_level(self):
        """
        test if advance_level() correctly increment the curr_level and update the board
        :return:
        """
        game4 = GameState(4, 0, False, [player1, player2, player3], [adv1, adv2, adv3], 5)
        game4.init_map(level1)
        game5 = GameState(4, 0, False, [player1, player2, player3], [adv1, adv2, adv3], 5)
        game5.init_map(level3)
        game4.advance_level(level4)
        game4.advance_level(level3)
        expected = game4.curr_level
        self.assertEqual(6, expected)
        for i in range(game5.board_col):
            for j in range(game5.board_row):
                self.assertEqual(game5.board[j][i].tile_type, game4.board[j][i].tile_type)

    def test_get_board(self):
        """
        test if get_board return the expected board
        :return:
        """
        game7 = GameState(1, 0, False, [player1, player2, player3], [adv1, adv2, adv3], 5)
        game7.init_map(level3)
        game8 = GameState(1, 0, False, [player1, player2, player3], [adv1, adv2, adv3], 5)
        game8.init_map(level2)
        game8.advance_level(level3)
        for i in range(game7.board_col):
            for j in range(game7.board_row):
                self.assertEqual(game7.board[j][i].tile_type, game8.board[j][i].tile_type)

    def test_move(self):
        """
        test if move(from, to) successfully remove and place the character on the board
        :return:
        """
        game9 = GameState(0, 0, False, [player1, player2, player3, player4], [adv1, adv2, adv3], 5)
        game9.init_map(level3)
        game9.move((4, 2), (4, 4))
        self.assertEqual(game9.board[2][4].occupied_by, [])
        self.assertEqual(game9.board[4][4].occupied_by, [player1])
        game9.move((5, 2), (4, 2))
        self.assertEqual(game9.board[2][4].occupied_by, [player2])

    def test_switch(self):
        """
        test the functionality of switch_turn() whether it successfully switches among non-expelled players,
        switches between players and adversaries.
        :return:
        """
        game10 = GameState(0, 0, False, [player1, player2, player3, player4], [adv1, adv2, adv3], 5)
        game10.init_map(level3)
        self.assertEqual(game10.characters[game10.turn], player1)
        game10.switch_turn()
        self.assertEqual(game10.characters[game10.turn], player2)
        game10.characters[2].expelled = True
        game10.switch_turn()
        self.assertEqual(game10.characters[game10.turn], player4)
        game10.switch_turn()
        self.assertEqual(game10.characters[game10.turn], adv1)
        for i in range(3):
            game10.switch_turn()
        self.assertEqual(game10.characters[game10.turn], player1)

    def test_get_state(self):
        """
        test the functionality of get_state(player_pos, adv_pos, exit status) successfully set the intermediate state
        :return:
        """
        game11 = GameState(0, 0, False, [player1, player2, player3, player4], [adv1, adv2, adv3], 5)
        game11.init_map(level2)
        game11 = game11.get_state([(2, 3), (3, 3), (1, 1), (1, 3)], [(8, 2), (8, 1), (7, 3)], False)
        self.assertEqual(game11.board[3][2].occupied_by, [player1])
        self.assertEqual(game11.board[3][3].occupied_by, [player2])
        #self.assertEqual(game11.board[3][7].occupied_by, [adv3])
        game11 = game11.get_state([(2, 3), (3, 3), (1, 1), (1, 3)], [(8, 2), (8, 1), (7, 3)], True)
        self.assertEqual(game11.unlocked, True)


if __name__ == '__main__':
    unittest.main()
