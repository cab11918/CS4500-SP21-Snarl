#! /usr/bin/python3
import sys
import unittest

from Snarl.src.Game.rule_checker import RuleChecker
from Snarl.src.Game.game_manager import GameManager
from Snarl.src.game_state import GameState
from Snarl.src.level import Level
from Snarl.src.room import Room
from Snarl.src.hallway import Hallway
from Snarl.src.player import Player
from Snarl.src.adversary import Adversary

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


class GameManagerTestCase(unittest.TestCase):
    def test_register_player(self):
        state1 = GameState(0, 0, False, [], [], 1)
        state1.init_map(level3)
        gm1 = GameManager([], [], state1, None)
        self.assertEqual(len(gm1.player_list), 0)
        gm1.register_player("Bob")
        self.assertEqual(len(gm1.player_list), 1)

    def test_get_player(self):
        state1 = GameState(0, 0, False, [], [], 1)
        state1.init_map(level3)
        gm1 = GameManager([], [], state1, None)
        self.assertRaises(Exception, gm1.get_player, "12345")
        gm1.register_player("Bob")
        self.assertEqual(gm1.get_player(gm1.player_list[0].player_id), gm1.player_list[0])

    def test_handle_move(self):
        state1 = GameState(0, 0, False, [], [], 1)
        state1.init_map(level3)
        gm1 = GameManager([], [], state1, None)
        gm1.register_player("Bob")
        gm1.handle_move((4, 2), (5, 2))
        self.assertEqual(gm1.curr_state.board[2][5].occupied_by[0].player_name, "Bob")

    def test_update_pos(self):
        state1 = GameState(0, 0, False, [], [], 1)
        state1.init_map(level3)
        gm1 = GameManager([], [], state1, None)
        gm1.register_player("Bob")
        gm1.update()
        self.assertEqual(gm1.player_list[0].position, (4, 2))
        gm1.handle_move((4, 2), (5, 2))
        gm1.update()
        self.assertEqual(gm1.player_list[0].position, (5, 2))

    def test_set_vision(self):
        state1 = GameState(0, 0, False, [], [], 1)
        state1.init_map(level3)
        gm1 = GameManager([], [], state1, None)
        gm1.register_player("Bob")
        gm1.update()
        gm1.set_vision(gm1.player_list[0])
        vision1 = gm1.player_list[0].vision

        gm1.register_player("Catherine")
        gm1.curr_state = gm1.curr_state.get_state([(4, 2), (4, 20)], [], False)
        gm1.update()
        gm1.set_vision(gm1.player_list[1])
        vision2 = gm1.player_list[1].vision

        def render_vision(vision):
            vision_output = ""
            for i in range(0, 5):
                row = ""
                for j in range(0, 5):
                    tile = vision[j][i]
                    if tile.tile_type == "floor" or tile.tile_type == "hallway":
                        row += " 1 "
                    if tile.tile_type == "door":
                        row += " 2 "
                    if tile.tile_type == "wall":
                        row += " 0 "
                    if tile.tile_type == "void":
                        row += " x "
                vision_output += row
                vision_output += "\n"
            return vision_output

        self.assertEqual(render_vision(vision1), " x  x  x  x  x \n"
                                                 " x  0  0  0  0 \n"
                                                 " x  0  1  1  2 \n"
                                                 " x  0  1  1  0 \n"
                                                 " x  0  1  0  0 \n")
        self.assertEqual(render_vision(vision2), " 1  0  0  0  0 \n"
                                                 " 2  1  1  1  0 \n"
                                                 " 0  1  1  1  0 \n"
                                                 " 0  1  1  1  0 \n"
                                                 " x  x  x  x  x \n")


if __name__ == '__main__':
    unittest.main()
