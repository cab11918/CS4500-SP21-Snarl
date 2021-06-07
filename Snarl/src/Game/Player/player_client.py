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
from Snarl.src.Game.resources.ani_objects.ani_zombie import AniZombie
from Snarl.src.Game.resources.ani_objects.ani_ghost import AniGhost
from Snarl.src.Game.resources.ani_objects.ani_locked_exit import AniLockedExit
from Snarl.src.Game.resources.ani_objects.ani_unlocked_exit import AniUnlockedExit
from Snarl.src.Common.abstract_player import AbstractPlayer


class PlayerClient(AbstractPlayer):
    """
    A class which represents the player client. It opens up a Pygame window and draw the corresponding information
    which were parsed from the game model. It also takes the controll from the player and calls the game manager to
    handle the move.
    """
    # temp plan for rendering
    gm = None
    # the 2D array of images of tiles
    tile_gui = []
    # the array of spirites for objects & characters
    obj_gui = []
    vis_board = None
    player_pos = (-1, -1)
    selected_target = pygame.image.load(r'Snarl/src/Game/resources/selected_target.png')
    selected_target = pygame.transform.scale(selected_target, (100, 100))

    selected_pos = (2, 2)

    player1_key_count = 0
    player1_exit_count = 0

    def __init__(self, gm):
        self.gm = gm

    def update(self, player_pos, vis_board):
        """
        The function to update the canvas by using the given vision information.
        :param player_pos: The position of the given player.
        :param vis_board: The vision of the player which is a 2D array of Tiles.
        :return: None
        """

        self.player_pos = player_pos
        # add tile layer and object images into the gui board
        self.tile_gui = []
        self.obj_gui = []

        for i in range(0, len(vis_board)):
            temp_row = []
            for j in range(0, len(vis_board[0])):
                # rendering tiles
                if vis_board[j][i].tile_type == "door":
                    temp_door = pygame.image.load(r'Snarl/src/Game/resources/door.png')
                    temp_door = pygame.transform.scale(temp_door, (100, 100))
                    temp_row.append(temp_door)
                if vis_board[j][i].tile_type == "floor":
                    temp_floor = pygame.image.load(r'Snarl/src/Game/resources/floor.png')
                    temp_floor = pygame.transform.scale(temp_floor, (100, 100))
                    temp_row.append(temp_floor)
                if vis_board[j][i].tile_type == "hallway":
                    temp_hallway = pygame.image.load(r'Snarl/src/Game/resources/hallway.png')
                    temp_hallway = pygame.transform.scale(temp_hallway, (100, 100))
                    temp_row.append(temp_hallway)
                if vis_board[j][i].tile_type == "void":
                    temp_void = pygame.image.load(r'Snarl/src/Game/resources/void.png')
                    temp_void = pygame.transform.scale(temp_void, (100, 100))
                    temp_row.append(temp_void)
                if vis_board[j][i].tile_type == "wall":
                    temp_wall = pygame.image.load(r'Snarl/src/Game/resources/wall.png')
                    temp_wall = pygame.transform.scale(temp_wall, (100, 100))
                    temp_row.append(temp_wall)
                # rendering objects
                for obj in vis_board[j][i].occupied_by:
                    if isinstance(obj, Player):
                        if obj.player_id == 0:
                            self.obj_gui.append(AniPlayer1(j * 100, i * 100, 100, 100))
                        if obj.player_id == 1:
                            self.obj_gui.append(AniPlayer2(j * 100, i * 100, 100, 100))
                        if obj.player_id == 2:
                            self.obj_gui.append(AniPlayer3(j * 100, i * 100, 100, 100))
                        if obj.player_id == 3:
                            self.obj_gui.append(AniPlayer4(j * 100, i * 100, 100, 100))
                    if isinstance(obj, Exit):
                        if obj.exit_unlocked:
                            self.obj_gui.append(AniUnlockedExit(j * 100, i * 100, 100, 100))
                        if not obj.exit_unlocked:
                            self.obj_gui.append(AniLockedExit(j * 100, i * 100, 100, 100))
                    if isinstance(obj, Key):
                        self.obj_gui.append(AniKey(j * 100, i * 100, 100, 100))
                    if isinstance(obj, Adversary):
                        if obj.adversary_type == "ghost":
                            self.obj_gui.append(AniGhost(j * 100, i * 100, 100, 100))
                        if obj.adversary_type == "zombie":
                            self.obj_gui.append(AniZombie(j * 100, i * 100, 100, 100))
            self.tile_gui.append(temp_row)

    def open_window(self):
        """
        The function that opens up a Pygame window and render the information stored in the class.
        :return: None
        """

        # intialize pygame
        pygame.init()
        clock = pygame.time.Clock()

        # window size
        screen_width = 500
        screen_height = 500
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Player Client")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.selected_pos[1] > 0:
                        self.selected_pos = (self.selected_pos[0], self.selected_pos[1] - 1)
                    if event.key == pygame.K_DOWN and self.selected_pos[1] < 4:
                        self.selected_pos = (self.selected_pos[0], self.selected_pos[1] + 1)
                    if event.key == pygame.K_LEFT and self.selected_pos[0] > 0:
                        self.selected_pos = (self.selected_pos[0] - 1, self.selected_pos[1])
                    if event.key == pygame.K_RIGHT and self.selected_pos[0] < 4:
                        self.selected_pos = (self.selected_pos[0] + 1, self.selected_pos[1])
                    if event.key == pygame.K_RETURN:
                        self.gm.update()
                        self.move()
                        self.selected_pos = (2, 2)

            screen.fill((255, 255, 255))

            for i in range(0, len(self.tile_gui)):
                for j in range(0, len(self.tile_gui[0])):
                    screen.blit(self.tile_gui[j][i], (i * 100, j * 100))

            moving_sprites = pygame.sprite.Group()
            for sprite in self.obj_gui:
                moving_sprites.add(sprite)

            # Drawing
            moving_sprites.draw(screen)
            moving_sprites.update(0.25)
            screen.blit(self.selected_target, (self.selected_pos[0] * 100, self.selected_pos[1] * 100))

            pygame.display.flip()
            clock.tick(15)

    def move(self):
        """
        The function used to handle the player's move by listening to the event that was triggered by the player.
        It calls the game manager to move the player if the given input is valid.
        :return: None
        """

        self.selected_pos = (
            self.player_pos[0] + self.selected_pos[0] - 2, self.player_pos[1] + self.selected_pos[1] - 2)

        if self.gm.move_result(self.player_pos, self.selected_pos) == "Key":
            print("Player " + self.gm.player_list[self.gm.curr_state.turn].player_name + " found the key")
            self.player1_key_count += 1

        if self.gm.move_result(self.player_pos, self.selected_pos) == "Eject":
            print("Player " + self.gm.player_list[self.gm.curr_state.turn].player_name + " was expelled")

        if self.gm.move_result(self.player_pos, self.selected_pos) == "Exit":
            print("Player " + self.gm.player_list[self.gm.curr_state.turn].player_name + " exited")
            self.player1_exit_count += 1

        if self.gm.rule_checker.is_valid_move(self.player_pos, self.selected_pos):

            self.gm.handle_move(self.player_pos, self.selected_pos)
            self.gm.update()
            self.gm.set_vision(self.gm.player_list[self.gm.curr_state.turn])
            self.update(self.gm.player_list[self.gm.curr_state.turn].position, self.gm.player_list[
                self.gm.curr_state.turn].vision)

            if self.gm.rule_checker.is_level_end(self.selected_pos):
                self.gm.set_level()
                if self.gm.rule_checker.is_game_over:
                    print("GAMEOVER, YOU WIN!")
                    print("Number of keys collected: " + str(self.player1_key_count))
                    print("Number of exits entered: " + str(self.player1_exit_count))

                    pygame.quit()
                    sys.exit()
                self.gm.update()
                self.gm.set_vision(self.gm.player_list[0])
                self.update(self.gm.player_list[0].position, self.gm.player_list[0].vision)
                return

            if self.gm.curr_state.turn == 0:
                for i in range(0, len(self.gm.curr_state.adversaries)):
                    temp_adv = self.gm.curr_state.adversaries[i]
                    self.gm.handle_move(temp_adv.position, temp_adv.return_move())
                    self.gm.update()
                self.gm.set_vision(self.gm.player_list[self.gm.curr_state.turn])
                self.update(self.gm.player_list[self.gm.curr_state.turn].position, self.gm.player_list[
                    self.gm.curr_state.turn].vision)
        else:
            pass
