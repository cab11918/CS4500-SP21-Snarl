import socket
import json
import threading
import sys
from Snarl.src.Remote.utils import send_msg, receive_msg
import Snarl.local.levels_reader as lr
from Snarl.src.Game.game_manager import GameManager
from Snarl.src.game_state import GameState
from Snarl.src.player import Player
from Snarl.src.Game.Observer.observer_client import ObserverClient
from Snarl.src.adversary import Adversary


class Server:
    """
    A Snarl Server class which host the game with game manager through TCP connection, send the requests to the client
    for interactions with the game, and receive the requests made by plyaer through Snarl Client.
    """
    socket = None
    player_sockets = []
    game_mng = None
    levels_file_name = "./Snarl/src/Remote/snarl.levels"
    observe = False
    client_num = 4
    reg_timeout = 60
    IP = "127.0.0.1"
    PORT = 45678

    level_num = -1
    levels = None
    players = []
    adversaries = []
    game_initiated = False
    observer = ObserverClient()

    # level-end info
    pick_key_player = ""
    exits_stat = []
    ejects_stat = []

    # game-end info
    players_score = []

    # check if the entire program is running
    is_running = True

    def __init__(self, levels_file_name, observe, client_num, reg_timeout, ip, port):
        self.levels_file_name = levels_file_name
        self.observe = observe
        self.client_num = int(client_num)
        self.reg_timeout = int(reg_timeout)
        self.IP = ip
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.IP, self.PORT))
        self.level_num, self.levels = lr.levels_reader(levels_file_name)
        # thread for sending server reqs. Main thread should only be pygame.
        self.sender = threading.Thread(target=self.client_sender, args=())

    # received start-level confirmation from clients, initialize the game.
    def init_game(self):
        """
        Initialize the game in the model and set the first level.
        :return: None
        """
        # initializing game
        state = GameState(0, 0, False, [], [], self.level_num)
        self.game_mng = GameManager([], [], state, None)
        self.game_mng.preload_levels(self.levels)

        # register players
        for name in self.players:
            self.game_mng.register_player(name)

        self.game_mng.set_level()
        self.game_mng.update()

    def notify_players(self, notification):
        """
        Put the notification to the message field of player-update and send it to every Snarl Client.
        :param notification: The message of player-update.
        :return: None
        """
        for i in range(0, len(self.players)):
            player_update_msg = json.dumps({
                "type": "player-update",
                "id": self.game_mng.player_list[i].player_id,
                "name": self.game_mng.player_list[i].player_name,
                "layout": self.game_mng.get_layout(self.game_mng.player_list[i]),
                "position": [self.game_mng.player_list[i].position[1],
                             self.game_mng.player_list[i].position[0]],
                "objects": self.game_mng.get_objects(self.game_mng.player_list[i]),
                "actors": self.game_mng.get_actors(self.game_mng.player_list[i]),
                "message": f"{notification}"
            })
            send_msg(self.player_sockets[i], player_update_msg)

    def notify_adversaries(self, notification):
        """
        Put the notification to the message field of player-update and send it to every Snarl Client.
        :param notification: The message of player-update.
        :return: None
        :except: IndexError: when the index exceed the number of adversaries connected.
        """
        for i in range(0, len(self.adversaries)):
            try:
                adv_update_msg = json.dumps({
                    "type": "adv-update",
                    "layout": self.game_mng.get_adv_layout(),
                    "position": [self.game_mng.adversary_list[i].position[1],
                                 self.game_mng.adversary_list[i].position[0]],
                    "objects": self.game_mng.get_adv_objects(),
                    "actors": self.game_mng.get_adv_actors(),
                    "message": f"{notification}"
                })
                print("hi." + adv_update_msg)
                send_msg(self.player_sockets[i + len(self.players)], adv_update_msg)
            except IndexError:
                pass

    def update_observer(self):
        """
        Update the GUI rendering board information with the board in current state.
        :return: None
        """
        if self.observe:
            self.observer.update((-1, -1), self.game_mng.curr_state.board)

    def proceed_game(self, s, player_pos, try_point, move_result):
        """
        The function takes a valid move, then it handles the move by calling the functions in the game model. After that
         it notifies every Snarl Client and update both GUI.
        :param s: The socket it wants to send.
        :param player_pos: The position of the player.
        :param try_point: The point the player trying to move.
        :param move_result: The result of moving to the point.
        :return: None
        """
        send_msg(s, json.dumps(move_result))
        self.game_mng.handle_move(player_pos, try_point)
        self.game_mng.update()

        self.notify_players(move_result)
        self.notify_adversaries(move_result)
        if self.game_mng.curr_state.turn < len(self.player_sockets):
            send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("move"))
            self.update_observer()

    def run(self):
        """
        The function keep the pygame GUI running. It also keeps the client sender (which is a separated thread) running
        so that it can respond to clients simultaneously.
        :return: None
        """
        self.sender.start()
        while self.is_running:
            if self.game_initiated:
                if self.observe:
                    self.observer.update((-1, -1), self.game_mng.curr_state.board)
                    self.observer.open_window()

    def send_end_game(self):
        """
        The helper function send the end-game message to every Snarl Clients
        :return: None
        """
        end_game = {"type": "end-game",
                    "scores": self.players_score}
        for s in self.player_sockets:
            send_msg(s, json.dumps(end_game))
        self.update_observer()

        for conn in self.player_sockets:
            conn.close()
        self.is_running = False

    def client_sender(self):
        """
        The client sender is a function running on a separated thread. During the game is progressing, it will accept
        Clients to send request, process them, and send the corresponding requests to the Player Clients.
        :return: None
        :throw: sock.timeout when the waiting time was exhausted.
                IndexError when it's the adversary turn but still trying to get the index of client sockets.
        """
        self.socket.listen(self.client_num)
        print("Waiting for initial players.")
        self.wait_for_players(1)

        print("Waiting for additional players.")
        self.socket.settimeout(self.reg_timeout)

        try:
            self.wait_for_players(self.client_num - 1)
        except socket.timeout:
            print("No additional players, game started.")

        self.init_game()
        self.game_initiated = True

        # send start-level
        for s in self.player_sockets:
            level_start = json.dumps({"type": "start-level",
                                      "level": self.level_num,
                                      "players": self.players})
            send_msg(s, level_start)

        # send player-update
        for i in range(0, len(self.players)):
            self.notify_players(
                f"hey {self.players[i]}, game started")
        for j in range(0, len(self.adversaries)):
            self.notify_adversaries(f"hey {self.adversaries[j]['name']}, game started")

        # send move
        for s in self.player_sockets:
            s_idx = self.player_sockets.index(s)
            if s_idx == self.game_mng.curr_state.turn:
                send_msg(s, json.dumps("move"))
        while not self.game_mng.rule_checker.are_all_expelled() and self.is_running:
            try:
                s = self.player_sockets[self.game_mng.curr_state.turn]
                req = receive_msg(s)
                req = json.loads(req)
                if req["by"] == "player":
                    if req["type"] == "move":
                        try_point = self.game_mng.player_list[self.game_mng.curr_state.turn].position if req[
                                                                                                             "to"] is None \
                            else (req["to"][1], req["to"][0])
                        player_pos = self.game_mng.player_list[self.game_mng.curr_state.turn].position
                        move_result = self.game_mng.move_result(player_pos, try_point)
                        if move_result == "Invalid":
                            send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("Invalid"))
                        elif move_result == "Exit":
                            # update player score
                            temp = {"exits": self.players_score[self.game_mng.curr_state.turn]["exits"] + 1}
                            self.players_score[self.game_mng.curr_state.turn].update(temp)
                            for player in self.game_mng.curr_state.players:
                                if player.expelled:
                                    self.ejects_stat.append(player.player_name)
                                else:
                                    self.exits_stat.append(player.player_name)

                            # send end level
                            end_level = {"type": "end-level",
                                         "key": self.pick_key_player,
                                         "exits": self.exits_stat,
                                         "ejects": self.ejects_stat}
                            for s in self.player_sockets:
                                send_msg(s, json.dumps(end_level))
                            self.exits_stat, self.ejects_stat = [], []
                            self.game_mng.set_level()
                            self.update_observer()

                            # send game over
                            if self.game_mng.rule_checker.is_game_over:
                                print("GAME OVER!")
                                self.send_end_game()
                                self.is_running = False

                            # send move result
                            self.game_mng.update()
                            self.notify_players(move_result)
                            self.notify_adversaries(move_result)

                            # send move to next player
                            send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("move"))
                            self.update_observer()

                        elif move_result == "Key":
                            # update level info
                            self.pick_key_player = self.players[self.game_mng.curr_state.turn]
                            # update player score
                            temp = {"keys": self.players_score[self.game_mng.curr_state.turn]["keys"] + 1}
                            self.players_score[self.game_mng.curr_state.turn].update(temp)

                            self.proceed_game(s, player_pos, try_point, move_result)

                        elif move_result == "Eject":
                            temp = {"ejects": self.players_score[self.game_mng.curr_state.turn]["ejects"] + 1}
                            self.players_score[self.game_mng.curr_state.turn].update(temp)
                            self.proceed_game(s, player_pos, try_point, move_result)

                        else:
                            self.proceed_game(s, player_pos, try_point, move_result)

                if req["by"] == "adversary":
                    adv = self.game_mng.adversary_list[self.game_mng.curr_state.turn - len(self.players)]
                    parsed_to = (req["to"][1], req["to"][0]) if req["to"] else adv.position
                    top = (adv.position[0], adv.position[1] - 1)
                    bot = (adv.position[0], adv.position[1] + 1)
                    lft = (adv.position[0] - 1, adv.position[1])
                    rt = (adv.position[0] + 1, adv.position[1])

                    def can_zb_move(pt):
                        return (not any(isinstance(obj, Adversary) for obj in
                                        self.game_mng.curr_state.board[pt[1]][pt[0]].occupied_by)) and \
                               self.game_mng.curr_state.board[pt[1]][pt[0]].tile_type == "floor"

                    def can_gst_move(pt):
                        return (not any(isinstance(obj, Adversary) for obj in
                                        self.game_mng.curr_state.board[pt[1]][pt[0]].occupied_by)) and \
                               self.game_mng.curr_state.board[pt[1]][pt[0]].tile_type != "void"

                    if adv.adversary_type == "zombie":
                        if can_zb_move(top) or can_zb_move(bot) or can_zb_move(
                                lft) or can_zb_move(rt):
                            if parsed_to in [top, bot, lft, rt] and can_zb_move(parsed_to):
                                self.proceed_game(s, adv.position, parsed_to, "OK")
                            else:
                                send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("Invalid"))
                        else:
                            if parsed_to is None:
                                self.proceed_game(s, adv.position, adv.position, "OK")
                            else:
                                send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("Invalid"))
                    if adv.adversary_type == "ghost":
                        if can_gst_move(top) or can_gst_move(bot) or can_gst_move(
                                lft) or can_gst_move(rt):
                            if parsed_to in [top, bot, lft, rt] and can_gst_move(parsed_to):
                                if self.game_mng.curr_state.board[parsed_to[1]][parsed_to[0]].tile_type == "wall":
                                    idx = -1
                                    cur_level = self.game_mng.curr_state.adversaries[0].level
                                    for i in range(0, len(cur_level.rooms)):
                                        if adv.position in cur_level.rooms[i].non_wall_tiles:
                                            idx = i
                                    to_pt = self.game_mng.curr_state.characters[self.game_mng.curr_state.turn]. \
                                        teleport(idx)
                                    self.proceed_game(s, adv.position, to_pt, "OK")
                                else:
                                    self.proceed_game(s, adv.position, parsed_to, "OK")
                            else:
                                send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("Invalid"))
                        else:
                            if parsed_to is None:
                                self.proceed_game(s, adv.position, adv.position, "OK")
                            else:
                                send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("Invalid"))

            except IndexError:
                # time for adversary to move
                first_survival = 0

                adv = self.game_mng.curr_state.characters[self.game_mng.curr_state.turn]
                for obj in self.game_mng.curr_state.board[adv.return_move()[1]][adv.return_move()[0]].occupied_by:
                    if isinstance(obj, Player):
                        for player_score in self.players_score:
                            if player_score["name"] == obj.player_name:
                                temp = {"ejects": player_score["ejects"] + 1}
                                player_score.update(temp)
                                break

                self.game_mng.handle_move(adv.position, adv.return_move())
                self.game_mng.update()

                for player in self.game_mng.curr_state.players:
                    if not player.expelled:
                        break
                    else:
                        first_survival += 1

                if self.game_mng.curr_state.turn == first_survival and first_survival < len(self.player_sockets):
                    self.notify_players("adversaries moved")
                    self.notify_adversaries("adv moved")
                    send_msg(self.player_sockets[self.game_mng.curr_state.turn], json.dumps("move"))
                    self.update_observer()
            except json.JSONDecodeError:
                self.is_running = False
        self.send_end_game()
        self.is_running = False

    def wait_for_players(self, count):
        """
        This function takes the count of players it should wait and try to receive their user name by sending the
         request. Once the players are full or the wait time exhausted, the server will stop waiting and host the game.
        :param count: the number of players it should wait.
        :return: None
        """

        for i in range(count):
            conn, addr = self.socket.accept()

            print("connected to", addr[0], addr[1])

            server_welcome = json.dumps({"type": "welcome",
                                         "info": "  _________                   .__    ________               \n"
                                                 " /   _____/ ____ _____ _______|  |   \______ \   _______  __\n"
                                                 " \_____  \ /    \\\\__  \\\\_  __ \  |    |    |  \_/ __ \  \/ /\n"
                                                 " /        \   |  \/ __ \|  | \/  |__  |    `   \  ___/\   / \n"
                                                 "/_______  /___|  (____  /__|  |____/ /_______  /\___  >\_/  \n"
                                                 "        \/     \/     \/                     \/     \/      \n"
                                                 "Hi from Snarl dev team. You've already connected to Snarl server. "
                                                 "For more information, please visit https:"
                                                 "//github.ccs.neu.edu/CS4500-S21/Londolond"})

            send_msg(conn, server_welcome)
            send_msg(conn, json.dumps("name"))

            self.player_sockets.append(conn)
            user_name = json.loads(receive_msg(conn))
            if user_name["type"] == "player":
                while user_name["name"] in self.players:
                    send_msg(conn, json.dumps("name"))
                    user_name = json.loads(receive_msg(conn))["name"]
                self.players.append(user_name["name"])
                self.players_score.append({"type": "player-score",
                                           "name": user_name["name"],
                                           "exits": 0,
                                           "ejects": 0,
                                           "keys": 0})
            if user_name["type"] == "adversary":
                while user_name["name"] in self.adversaries:
                    send_msg(conn, json.dumps("name"))
                    user_name = json.loads(receive_msg(conn))["name"]
                self.adversaries.append(user_name)

    def send(self, msg):
        """
        The function to call the send message function in utils.
        :param msg: The message server want to send
        :return: None
        """
        send_msg(self.socket, msg)

    def receive(self):
        """
        The function to call the receive message function in utils.
        :return: None
        """
        return receive_msg(self.socket)


if __name__ == '__main__':
    # configs
    client_num = 4
    levels_file_name = "./Snarl/src/Remote/snarl.levels"
    observe = False
    reg_timeout = 60
    ip = "127.0.0.1"
    port = 45678
    game_start = False

    # parsing commandline argument
    for i in range(0, len(sys.argv)):
        try:
            if sys.argv[i].lower() == '--levels':
                levels_file_name = sys.argv[i + 1]
            if sys.argv[i].lower() == '--observe':
                observe = True
            if sys.argv[i].lower() == '--clients':
                if not 1 <= int(sys.argv[i + 1]) <= 4:
                    print("Invalid number of players!")
                    sys.exit()
                else:
                    client_num = sys.argv[i + 1]
            if sys.argv[i].lower() == '--wait':
                reg_timeout = int(sys.argv[i + 1])
            if sys.argv[i].lower() == '--address':
                ip = str(sys.argv[i + 1])
            if sys.argv[i].lower() == '--port':
                port = int(sys.argv[i + 1])

        except (IndexError, TypeError):
            print("Invalid specs, try again.")

    server = Server(levels_file_name, observe, client_num, reg_timeout, ip, port)
    server.run()
