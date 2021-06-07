from Snarl.src.Remote.utils import receive_msg, send_msg
import socket
import json
import sys
import threading
import pygame
import Snarl.src.Remote.jsonfactory as jf
from Snarl.src.Remote.utils import resource_path
from Snarl.src.player import Player
from Snarl.src.exit import Exit
from Snarl.src.key import Key
from Snarl.src.adversary import Adversary
from Snarl.src.Game.resources.ani_objects.ani_player1 import AniPlayer1
from Snarl.src.Game.resources.ani_objects.ani_player2 import AniPlayer2
from Snarl.src.Game.resources.ani_objects.ani_player3 import AniPlayer3
from Snarl.src.Game.resources.ani_objects.ani_player4 import AniPlayer4
from Snarl.src.Game.resources.ani_objects.ani_key import AniKey
from Snarl.src.Game.resources.ani_objects.ani_zombie import AniZombie
from Snarl.src.Game.resources.ani_objects.ani_ghost import AniGhost
from Snarl.src.Game.resources.ani_objects.ani_locked_exit import AniLockedExit
from Snarl.src.Game.resources.ani_objects.ani_unlocked_exit import AniUnlockedExit


class Client:
    """
    A remote adversary client available for user to register and play, the default ip and port are listed below

    """
    socket = None
    player_client = None
    IP = "127.0.0.1"
    PORT = 45678

    # GUI config
    # the 2D array of images of tiles
    tile_gui = []
    scale = 32
    # the array of sprites for objects & characters
    obj_gui = []
    vis_board = None
    player_pos = (-1, -1)
    selected_target = pygame.image.load(resource_path(r'Snarl/src/Game/resources/selected_target.png'))
    selected_target = pygame.transform.scale(selected_target, (scale, scale))
    selected_pos = (2, 2)
    player1_key_count = 0
    player1_exit_count = 0
    screen = None
    clock = None
    initial_updated = False
    receiver = None
    can_move = False
    is_exit_open = False
    is_expelled = False

    # check if the entire program is running
    is_running = True

    # constructor for Snarl client
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.IP = ip
        self.PORT = port
        # thread for receiving server reqs. Main thread should only be pygame.
        self.receiver = threading.Thread(target=self.server_listener, args=())
        self.receiver.setDaemon(True)

    @staticmethod
    def is_server_welcome(req):
        """
        check whether the req is server welcome
        :param req: dictionary representing the server welcome information
        :return: Boolean
        """
        return type(req) == dict and "type" in req and req["type"] == "welcome"

    @staticmethod
    def is_level_start(req):
        """
         check whether the req is level start message
        :param req: dictionary representing the level start message
        :return: Boolean
        """
        return type(req) == dict and "type" in req and req["type"] == "start-level"

    @staticmethod
    def is_adv_update_message(req):
        """
        check whether the req is player adversary update message
        :param req: dictionary representing the player update message
        :return: Boolean
        """
        return type(req) == dict and "type" in req and req["type"] == "adv-update"

    @staticmethod
    def is_level_end(req):
        """
        check whether the req is level end message
        :param req: dictionary representing the level end message
        :return: Boolean
        """
        return type(req) == dict and "type" in req and req["type"] == "end-level"

    @staticmethod
    def is_game_end(req):
        """
        check whether the req is game end message
        :param req: dictionary representing the game end message
        :return: Boolean
        """
        return type(req) == dict and "type" in req and req["type"] == "end-game"

    def send_name(self):
        """
        send player name to the server, player name is acquired from stdin
        :return: None
        """
        my_username = input("Enter your name and the hunt begins: ")
        username = json.dumps({"type": "adversary",
                               "name": my_username})
        self.send(username)

    def send_move(self):
        """
        send move to the server, player move is generated from player position and selected tile
        :return: None
        """
        move = self.selected_pos
        player_move = {"type": "move", "to": [move[1], move[0]]}
        player_move = json.dumps(player_move)
        self.send(player_move)

    def update(self, pos, board):
        """
        update the gui window with given position and vision
        :param pos: a tuple representing the player's position relative to the board
        :param board: [[Tile]] representing player's surrounding
        :return: None
        """
        self.player_pos = pos
        self.vis_board = board
        # add tile layer and object images into the gui board
        self.tile_gui = []
        self.obj_gui = []

        for j in range(0, len(self.vis_board)):
            temp_row = []
            for i in range(0, len(self.vis_board[0])):

                # rendering tiles
                if self.vis_board[j][i].tile_type == "door":
                    temp_door = pygame.image.load(resource_path(r'Snarl/src/Game/resources/door.png'))
                    temp_door = pygame.transform.scale(temp_door, (self.scale, self.scale))
                    temp_row.append(temp_door)
                if self.vis_board[j][i].tile_type == "floor":
                    temp_floor = pygame.image.load(resource_path(r'Snarl/src/Game/resources/floor.png'))
                    temp_floor = pygame.transform.scale(temp_floor, (self.scale, self.scale))
                    temp_row.append(temp_floor)
                if self.vis_board[j][i].tile_type == "hallway":
                    temp_hallway = pygame.image.load(resource_path(r'Snarl/src/Game/resources/hallway.png'))
                    temp_hallway = pygame.transform.scale(temp_hallway, (self.scale, self.scale))
                    temp_row.append(temp_hallway)
                if self.vis_board[j][i].tile_type == "void":
                    temp_void = pygame.image.load(resource_path(r'Snarl/src/Game/resources/void.png'))
                    temp_void = pygame.transform.scale(temp_void, (self.scale, self.scale))
                    temp_row.append(temp_void)
                if self.vis_board[j][i].tile_type == "wall":
                    temp_wall = pygame.image.load(resource_path(r'Snarl/src/Game/resources/wall.png'))
                    temp_wall = pygame.transform.scale(temp_wall, (self.scale, self.scale))
                    temp_row.append(temp_wall)

                # rendering objects
                for obj in self.vis_board[j][i].occupied_by:
                    if isinstance(obj, Player):
                        if obj.player_id == 0:
                            self.obj_gui.append(AniPlayer1(i * self.scale, j * self.scale, self.scale, self.scale))
                        if obj.player_id == 1:
                            self.obj_gui.append(AniPlayer2(i * self.scale, j * self.scale, self.scale, self.scale))
                        if obj.player_id == 2:
                            self.obj_gui.append(AniPlayer3(i * self.scale, j * self.scale, self.scale, self.scale))
                        if obj.player_id == 3:
                            self.obj_gui.append(AniPlayer4(i * self.scale, j * self.scale, self.scale, self.scale))
                    if isinstance(obj, Exit):
                        if self.is_exit_open:
                            self.obj_gui.append(AniUnlockedExit(i * self.scale, j * self.scale, self.scale, self.scale))
                        else:
                            self.obj_gui.append(AniLockedExit(i * self.scale, j * self.scale, self.scale, self.scale))
                    if isinstance(obj, Key):
                        self.obj_gui.append(AniKey(i * self.scale, j * self.scale, self.scale, self.scale))
                    if isinstance(obj, Adversary):
                        if obj.adversary_type == "ghost":
                            self.obj_gui.append(AniGhost(i * self.scale, j * self.scale, self.scale, self.scale))
                        if obj.adversary_type == "zombie":
                            self.obj_gui.append(AniZombie(i * self.scale, j * self.scale, self.scale, self.scale))
            self.tile_gui.append(temp_row)

    def open_window(self):
        """
        open the gui window, after game is initialized, open the pygame window
        :return: None
        """
        # the initial data wasn't received yet, wait.
        while not self.initial_updated:
            pass

        # initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # window size
        screen_width = 500
        screen_height = 500
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Snarl Adversary")

        while self.is_running:
            if self.can_move:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.selected_pos[1] > 0:
                            self.selected_pos = (self.selected_pos[0], self.selected_pos[1] - 1)
                        if event.key == pygame.K_DOWN and self.selected_pos[1] < len(self.vis_board) - 1:
                            self.selected_pos = (self.selected_pos[0], self.selected_pos[1] + 1)
                        if event.key == pygame.K_LEFT and self.selected_pos[0] > 0:
                            self.selected_pos = (self.selected_pos[0] - 1, self.selected_pos[1])
                        if event.key == pygame.K_RIGHT and self.selected_pos[0] < len(self.vis_board[0]) - 1:
                            self.selected_pos = (self.selected_pos[0] + 1, self.selected_pos[1])
                        if event.key == pygame.K_RETURN:
                            move_send = {"type": "move",
                                         "by": "adversary",
                                         "to": None if self.selected_pos == self.player_pos
                                         else [(self.selected_pos[1]),
                                               (self.selected_pos[0])]}
                            move_send = json.dumps(move_send)
                            self.send(move_send)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            self.screen.fill((0, 0, 0))

            for j in range(0, len(self.tile_gui)):
                for i in range(0, len(self.tile_gui[0])):
                    self.screen.blit(self.tile_gui[j][i], (i * self.scale, j * self.scale))

            moving_sprites = pygame.sprite.Group()
            for sprite in self.obj_gui:
                moving_sprites.add(sprite)

            # Drawing
            moving_sprites.draw(self.screen)
            moving_sprites.update(0.25)
            if self.can_move:
                self.screen.blit(self.selected_target,
                                 (self.selected_pos[0] * self.scale, self.selected_pos[1] * self.scale))

            # expelled screen filter
            if self.is_expelled:
                s = pygame.Surface((500, 500))
                s.set_alpha(200)
                s.fill((0, 0, 0))
                self.screen.blit(s, (0, 0))

            pygame.display.flip()
            self.clock.tick(15)

    def server_listener(self):
        """
        the listener for client that received message from server, and then provide update or send move to the server
        :return: None
        """
        while self.is_running:
            data = self.receive()
            if not data:
                break
            try:
                req = json.loads(data)
            except json.JSONDecodeError:
                continue

            if self.is_server_welcome(req):
                print(req["info"])
            if req == "name":
                self.send_name()
            if self.is_level_start(req):
                level_num = req["level"]
                player_list = req["players"]
                print(f"Game started. The dungeon has {level_num} levels. The players are {player_list}")
            if self.is_adv_update_message(req) and not self.initial_updated:
                print(req)
                pos, board = jf.parse_adv_update_message(req)
                self.update(pos, board)
                self.initial_updated = True
                self.selected_pos = (req["position"][1], req["position"][0])
                self.player_pos = (req["position"][1], req["position"][0])

            if self.is_adv_update_message(req) and self.initial_updated:
                print("not firtst time get update")
                print(req)
                if req["message"] == "Key":
                    self.is_exit_open = True
                if req["message"] == "Exit":
                    self.is_exit_open = False
                    self.is_expelled = False
                pos, board = jf.parse_adv_update_message(req)
                self.update(pos, board)
                self.selected_pos = (req["position"][1], req["position"][0])
                self.player_pos = (req["position"][1], req["position"][0])
                self.can_move = False

            if req == "move":
                self.update(pos, board)
                self.can_move = True

            if req == "OK":
                pass
            if req == "Key":
                print("You found the key.")
            if req == "Exit":
                print("You exited the current level.")
            if req == "Eject":
                print("You were ejected by an adversary.")
            if req == "Invalid":
                print("The move is invalid, please try again.")

            if self.is_level_end(req):
                print(
                    f"The level ended.\nPlayer: {req['key']} found the key.\nPlayers: {req['exits']} exited the "
                    f"level.\nPlayers: {req['ejects']} were expelled by adversary.")

            if self.is_game_end(req):
                print("Game Over! Here is the Leader Board.")
                print("============LEADERBOARD============")
                for score in req['scores']:
                    print("---------------" + score["name"] + "---------------")
                    print(f"Exits entered: {score['exits']}\nTimes being ejected: "
                          f"{score['ejects']}\nNumber of keys found: {score['keys']}")
                    self.is_running = False

    def run(self):
        """
        function control the start listener thread
        :return: None
        """
        # start server listener
        self.receiver.start()

    def send(self, msg):
        """
        send specific message to the socket
        :param msg: json representing the message
        :return: None
        """
        send_msg(self.socket, msg)

    def receive(self):
        """
        receive message from the socket
        :return: json representing the message
        """
        return receive_msg(self.socket)


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 45678
    # parsing commandline argument
    for i in range(0, len(sys.argv)):
        try:
            if sys.argv[i].lower() == '--address':
                ip = str(sys.argv[i + 1])
            if sys.argv[i].lower() == '--port':
                port = int(sys.argv[i + 1])

        except (IndexError, TypeError):
            print("Invalid specs, try again.")

    client = Client(ip, port)

    client.run()
    client.open_window()
