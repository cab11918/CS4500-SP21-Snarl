import sys
import Snarl.local.levels_reader as lr
from Snarl.src.Game.game_manager import GameManager
from Snarl.src.game_state import GameState
from Snarl.src.level import Level
from Snarl.src.room import Room
from Snarl.src.hallway import Hallway
from Snarl.src.Game.Player.player_client import PlayerClient
from Snarl.src.Game.Observer.observer_client import ObserverClient


def main():
    """
    The main progarm of local snarl client. It takes arguments from the user and host a game by parsing the levels from
    the input file.
    :return: None
    """
    player_num = 1
    start_num = 1
    levels_file_name = None
    observe = False

    # parsing commandline argument
    for i in range(0, len(sys.argv)):
        try:
            if sys.argv[i].lower() == '--levels':
                levels_file_name = sys.argv[i + 1]
                i += 1
            if sys.argv[i].lower() == '--observe':
                observe = True
            if sys.argv[i].lower() == '--players':
                if int(sys.argv[i + 1]) > 1 or int(sys.argv[i + 1]) <= 0:
                    print("Invalid number of players!")
                    sys.exit()
            if sys.argv[i].lower() == '--start':
                start_num = sys.argv[i + 1]
                start_num = int(start_num)

        except IndexError:
            print("Invalid specs, try again.")

    # initializing game
    level_num, levels = lr.levels_reader(levels_file_name)
    state = GameState(start_num - 1, 0, False, [], [], level_num - start_num + 1)
    gm1 = GameManager([], [], state, None)
    gm1.preload_levels(levels)

    # starting with the correct level
    while start_num != 1:
        levels.pop(0)
        start_num -= 1

    # registering player
    player_count = 0
    while player_count < player_num:
        player_name = input("please enter your name: \n")
        gm1.register_player(player_name)
        player_count += 1

    gm1.set_level()
    gm1.update()

    # set the initial visioin for the first player
    gm1.set_vision(gm1.player_list[0])
    vision1 = gm1.player_list[0].vision

    # observer
    if observe:
        observer1 = ObserverClient()
        observer1.update((0, 0), gm1.curr_state.board)
        observer1.open_window()
        sys.exit()
    # client
    client1 = PlayerClient(gm1)
    client1.update(gm1.player_list[0].position, vision1)
    client1.open_window()


if __name__ == "__main__":
    main()
