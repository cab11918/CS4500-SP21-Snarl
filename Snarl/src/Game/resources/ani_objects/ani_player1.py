import pygame
from Snarl.src.Remote.utils import resource_path


class AniPlayer1(pygame.sprite.Sprite):
    """
    A class to represent the spirte sheet that was used by pygame to draw the animated characters.
    """
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__()
        self.sprites = []
        img1 = pygame.image.load(resource_path(r'Snarl/src/Game/resources/player1/priest2_v1_1.png'))
        img2 = pygame.image.load(resource_path(r'Snarl/src/Game/resources/player1/priest2_v1_2.png'))
        img3 = pygame.image.load(resource_path(r'Snarl/src/Game/resources/player1/priest2_v1_3.png'))
        img4 = pygame.image.load(resource_path(r'Snarl/src/Game/resources/player1/priest2_v1_4.png'))
        img1 = pygame.transform.scale(img1, (width, height))
        img2 = pygame.transform.scale(img2, (width, height))
        img3 = pygame.transform.scale(img3, (width, height))
        img4 = pygame.transform.scale(img4, (width, height))
        self.sprites.append(img1)
        self.sprites.append(img2)
        self.sprites.append(img3)
        self.sprites.append(img4)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
