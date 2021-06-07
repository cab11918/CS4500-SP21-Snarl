import sys
import pygame
from Snarl.src.player import Player
from Snarl.src.exit import Exit
from Snarl.src.key import Key
from Snarl.src.adversary import Adversary
from Snarl.src.Game.resources.ani_objects.ani_player1 import AniPlayer1
from Snarl.src.Game.resources.ani_objects.ani_player2 import AniPlayer2
from Snarl.src.Game.resources.ani_objects.ani_player3 import AniPlayer3
from Snarl.src.Game.resources.ani_objects.ani_player4 import AniPlayer4
from Snarl.src.Game.resources.ani_objects.ani_key import AniKey
from Snarl.src.Game.resources.ani_objects.ani_locked_exit import AniLockedExit
from Snarl.src.Game.resources.ani_objects.ani_unlocked_exit import AniUnlockedExit
from Snarl.src.Common.abstract_observer import AbstractObserver
from Snarl.src.Game.resources.ani_objects.ani_zombie import AniZombie
from Snarl.src.Game.resources.ani_objects.ani_ghost import AniGhost
from Snarl.src.Remote.utils import resource_path


class ObserverClient(AbstractObserver):
    """
    A class which represents the observer client. It opens up a Pygame window and draw the corresponding information
    which were parsed from the game model.
    """
    # the 2D array of images of tiles
    tile_gui = []
    # the array of spirites for objects & characters
    obj_gui = []
    vis_board = None
    player_pos = (-1, -1)
    screen_width = -1
    screen_height = -1
    scale = 32

    def __init__(self):
        pass

    def update(self, player_pos, vis_board):

        # add tile layer and object images into the gui board
        self.tile_gui = []
        self.obj_gui = []

        # make the window size adapt the board
        self.screen_height = len(vis_board) * self.scale
        self.screen_width = len(vis_board[0]) * self.scale

        for i in range(0, len(vis_board)):
            temp_row = []
            for j in range(0, len(vis_board[0])):
                # rendering tiles
                if vis_board[i][j].tile_type == "door":
                    temp_door = pygame.image.load(resource_path(r'Snarl/src/Game/resources/door.png'))
                    temp_door = pygame.transform.scale(temp_door, (self.scale, self.scale))
                    temp_row.append(temp_door)
                if vis_board[i][j].tile_type == "floor":
                    temp_floor = pygame.image.load(resource_path(r'Snarl/src/Game/resources/floor.png'))
                    temp_floor = pygame.transform.scale(temp_floor, (self.scale, self.scale))
                    temp_row.append(temp_floor)
                if vis_board[i][j].tile_type == "hallway":
                    temp_hallway = pygame.image.load(resource_path(r'Snarl/src/Game/resources/hallway.png'))
                    temp_hallway = pygame.transform.scale(temp_hallway, (self.scale, self.scale))
                    temp_row.append(temp_hallway)
                if vis_board[i][j].tile_type == "void":
                    temp_void = pygame.image.load(resource_path(r'Snarl/src/Game/resources/void.png'))
                    temp_void = pygame.transform.scale(temp_void, (self.scale, self.scale))
                    temp_row.append(temp_void)
                if vis_board[i][j].tile_type == "wall":
                    temp_wall = pygame.image.load(resource_path(r'Snarl/src/Game/resources/wall.png'))
                    temp_wall = pygame.transform.scale(temp_wall, (self.scale, self.scale))
                    temp_row.append(temp_wall)
                # rendering objects
                for obj in vis_board[i][j].occupied_by:
                    if isinstance(obj, Player):
                        if obj.player_id == 0:
                            self.obj_gui.append(AniPlayer1(j * self.scale, i * self.scale, self.scale, self.scale))
                        if obj.player_id == 1:
                            self.obj_gui.append(AniPlayer2(j * self.scale, i * self.scale, self.scale, self.scale))
                        if obj.player_id == 2:
                            self.obj_gui.append(AniPlayer3(j * self.scale, i * self.scale, self.scale, self.scale))
                        if obj.player_id == 3:
                            self.obj_gui.append(AniPlayer4(j * self.scale, i * self.scale, self.scale, self.scale))
                    if isinstance(obj, Exit):
                        if obj.exit_unlocked:
                            self.obj_gui.append(AniUnlockedExit(j * self.scale, i * self.scale, self.scale, self.scale))
                        if not obj.exit_unlocked:
                            self.obj_gui.append(AniLockedExit(j * self.scale, i * self.scale, self.scale, self.scale))
                    if isinstance(obj, Key):
                        self.obj_gui.append(AniKey(j * self.scale, i * self.scale, self.scale, self.scale))

                    if isinstance(obj, Adversary):
                        if obj.adversary_type == "ghost":
                            self.obj_gui.append(AniGhost(j * self.scale, i * self.scale, self.scale, self.scale))
                        if obj.adversary_type == "zombie":
                            self.obj_gui.append(AniZombie(j * self.scale, i * self.scale, self.scale, self.scale))

            self.tile_gui.append(temp_row)

    def open_window(self):

        # intialize pygame
        pygame.init()
        clock = pygame.time.Clock()

        # window size
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Observer Client")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((self.screen_width, self.screen_height),
                                            pygame.RESIZABLE)

            screen.fill((0, 0, 0))

            for i in range(0, len(self.tile_gui)):
                for j in range(0, len(self.tile_gui[0])):
                    screen.blit(self.tile_gui[i][j], (j * self.scale, i * self.scale))

            moving_sprites = pygame.sprite.Group()
            for sprite in self.obj_gui:
                moving_sprites.add(sprite)

            # Drawing
            moving_sprites.draw(screen)
            moving_sprites.update(0.25)
            pygame.display.flip()
            clock.tick(15)
