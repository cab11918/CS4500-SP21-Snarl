import pygame
from Snarl.src.Remote.utils import resource_path


class AniLockedExit(pygame.sprite.Sprite):
    """
    A class to represent the spirte sheet that was used by pygame to draw the animated characters.
    """
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__()
        self.sprites = []
        img1 = pygame.image.load(resource_path(r'Snarl/src/Game/resources/locked_exit.png'))
        img1 = pygame.transform.scale(img1, (width, height))
        self.sprites.append(img1)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]
